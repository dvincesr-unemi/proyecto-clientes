
from models import Cliente, CAMPOS_CLIENTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

# Crea el gestor encargado de leer y guardar el archivo JSON.
gestor = GestorJSON("data/clientes.json")

# Tupla con los campos que siempre deben tener informacion.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email")

# Tupla con los campos donde se permitira realizar busquedas.
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):

    # Crea un conjunto con todos los emails registrados.
    # Los conjuntos permiten buscar duplicados rapidamente.
    return {

        # Convierte el email a minusculas para evitar diferencias
        # entre mayusculas y minusculas.
        registro["email"].lower()

        # Recorre todos los registros almacenados.
        for registro in gestor.leer()

        # Si se esta editando un cliente, ignora su propio email.
        if registro["id"] != excepto_id
    }


def siguiente_id():

    # Crea una lista con todos los id existentes.
    ids = [registro["id"] for registro in gestor.leer()]

    # max() obtiene el mayor id.
    # Si no existen registros, comienza desde 1.
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_cliente(datos):

    # datos es un diccionario con la informacion del cliente.

    try:

        # Crea un nuevo diccionario con todos los campos.
        # str() convierte cualquier dato en texto.
        # .get() evita errores si falta una clave.
        # .strip() elimina espacios al inicio y final.
        valores = {
            campo: str(datos.get(campo, "")).strip()
            for campo in CAMPOS_CLIENTE
        }

        # Busca los campos obligatorios vacios.
        faltantes = [
            campo
            for campo in CAMPOS_OBLIGATORIOS
            if not valores[campo]
        ]

        # Si existen campos vacios devuelve un mensaje.
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # Verifica que el email tenga un formato valido.
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato valido"

        # Comprueba que el email no este repetido.
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya esta registrado"

        # ** desempaqueta el diccionario y envia cada
        # elemento como argumento del constructor.
        cliente = Cliente(siguiente_id(), **valores)

        # Lee todos los registros actuales.
        registros = gestor.leer()

        # Agrega el nuevo cliente al final de la lista.
        registros.append(cliente.a_diccionario())

        # Guarda nuevamente el archivo JSON.
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        # Devuelve un mensaje indicando que todo salio bien.
        return True, (
            f"Cliente {cliente.obtener_nombre_completo()} "
            f"creado con id {cliente.id}"
        )

    # Captura cualquier error inesperado.
    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():

    # Convierte cada diccionario del JSON en un objeto Cliente.
    return [
        Cliente.desde_diccionario(registro)
        for registro in gestor.leer()
    ]


def obtener_por_id(id_cliente):

    # Recorre todos los clientes.
    for cliente in obtener_todos():

        # Si encuentra el id devuelve el objeto.
        if cliente.id == id_cliente:
            return cliente

    # Si no existe devuelve None.
    return None


# ===================== S · SEARCH =====================

def buscar_clientes(termino):

    # Elimina espacios y convierte el texto a minusculas.
    termino = termino.strip().lower()

    # Si el termino esta vacio devuelve una lista vacia.
    if not termino:
        return []

    # Lista donde se guardaran los resultados.
    encontrados = []

    # Recorre todos los registros.
    for registro in gestor.leer():

        # Recorre cada campo permitido para buscar.
        for campo in CAMPOS_BUSCABLES:

            # .get() evita errores si el campo no existe.
            # lower() hace la comparacion sin importar mayusculas.
            if termino in str(registro.get(campo, "")).lower():

                # Convierte el diccionario en un objeto Cliente.
                encontrados.append(
                    Cliente.desde_diccionario(registro)
                )

                # Sale del ciclo interno porque ya encontro
                # una coincidencia para ese cliente.
                break

    # Devuelve todos los clientes encontrados.
    return encontrados
# ===================== U · UPDATE =====================

def actualizar_cliente(id_cliente, cambios):

    # cambios es un diccionario con los campos a modificar.

    try:

        # Convierte las claves del diccionario y la tupla en conjuntos.
        # La diferencia entre conjuntos devuelve los campos
        # que no existen en CAMPOS_CLIENTE.
        desconocidos = set(cambios) - set(CAMPOS_CLIENTE)

        # Si existen campos no validos devuelve un mensaje.
        if desconocidos:
            return False, (
                f"Campos no validos: {', '.join(sorted(desconocidos))}"
            )

        # Si no se recibio ningun cambio.
        if not cambios:
            return False, "No se indico ningun cambio"

        # Si se desea modificar el email.
        if "email" in cambios:

            # Valida el formato del nuevo email.
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato valido"

            # Comprueba que el email no pertenezca a otro cliente.
            if cambios["email"].lower() in emails_registrados(excepto_id=id_cliente):
                return False, "Ese email ya lo usa otro cliente"

        # Lee todos los registros almacenados.
        registros = gestor.leer()

        # Guardara la posicion del cliente encontrado.
        posicion = None

        # enumerate() devuelve el indice y el elemento al mismo tiempo.
        for indice, registro in enumerate(registros):

            # Busca el cliente por id.
            if registro["id"] == id_cliente:
                posicion = indice
                break

        # Si no encontro el cliente.
        if posicion is None:
            return False, f"No existe un cliente con id {id_cliente}"

        # update() modifica solamente las claves recibidas
        # sin eliminar las demas.
        registros[posicion].update(cambios)

        # Guarda nuevamente el archivo JSON.
        gestor.guardar(registros)

        # Devuelve mensaje de exito.
        return True, (
            f"Cliente {id_cliente} actualizado "
            f"({len(cambios)} campo/s)"
        )

    # Captura cualquier error inesperado.
    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_cliente(id_cliente):

    # Lee todos los registros.
    registros = gestor.leer()

    # Crea una nueva lista excluyendo el cliente indicado.
    # Es mas seguro crear una lista nueva que eliminar
    # elementos mientras se recorre la original.
    quedan = [
        registro
        for registro in registros
        if registro["id"] != id_cliente
    ]

    # Si ambas listas tienen el mismo tamano,
    # significa que el cliente no existia.
    if len(quedan) == len(registros):
        return False, f"No existe un cliente con id {id_cliente}"

    # Guarda la nueva lista.
    gestor.guardar(quedan)

    # Devuelve mensaje de exito.
    return True, f"Cliente {id_cliente} eliminado"


# ===================== EXTRA: ESTADISTICAS =====================

def estadisticas():

    # Lee todos los registros almacenados.
    registros = gestor.leer()

    # Crea un conjunto con las ciudades.
    # title() coloca la primera letra de cada palabra en mayuscula.
    # Los conjuntos eliminan automaticamente los repetidos.
    ciudades = {
        r.get("ciudad", "").title()
        for r in registros
        if r.get("ciudad")
    }

    # Obtiene los dominios de los correos.
    # split("@") divide el correo en usuario y dominio.
    dominios = {
        r["email"].split("@")[1].lower()
        for r in registros
        if "@" in r["email"]
    }

    # Lista con los clientes que no tienen telefono registrado.
    sin_telefono = [
        r["nombre"]
        for r in registros
        if not r.get("telefono")
    ]

    # Devuelve un diccionario con todas las estadisticas.
    return {
        "total": len(registros),

        # sorted() ordena alfabeticamente las ciudades.
        "ciudades": sorted(ciudades),

        # Ordena los dominios antes de devolverlos.
        "dominios": sorted(dominios),

        # Lista de clientes sin telefono.
        "sin_telefono": sin_telefono,
    }




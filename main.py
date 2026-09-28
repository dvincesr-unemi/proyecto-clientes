
from models import CAMPOS_CLIENTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error,
    imprimir_info, confirmar
)
from views import (
    crear_cliente, obtener_todos, obtener_por_id,
    buscar_clientes, actualizar_cliente,
    eliminar_cliente, estadisticas
)


# Espera a que el usuario presione Enter.
def pausa():
    input("\nPresione Enter para continuar...")


# Muestra una lista de clientes en forma de tabla.
def mostrar_tabla(clientes):

    # Los simbolos < indican alineacion a la izquierda.
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CIUDAD':<15}{'TELEFONO':<12}")

    print("-" * 85)

    # Recorre todos los clientes.
    for cliente in clientes:

        # Muestra la informacion de cada cliente.
        print(
            f"{cliente.id:<5}"
            f"{cliente.obtener_nombre_completo():<25}"
            f"{cliente.email:<28}"
            f"{cliente.ciudad:<15}"
            f"{cliente.telefono:<12}"
        )

    print("-" * 85)

    # len() cuenta la cantidad de clientes.
    imprimir_info(f"Total: {len(clientes)} cliente(s)")


# ===================== C · CREAR =====================

def opcion_crear():

    imprimir_titulo("CREAR NUEVO CLIENTE")

    # Diccionario donde se guardaran los datos ingresados.
    datos = {}

    # Recorre la tupla de campos para crear el formulario.
    for campo in CAMPOS_CLIENTE:

        # capitalize() convierte la primera letra en mayuscula.
        datos[campo] = input(f"{campo.capitalize()}: ")

    # La funcion devuelve una tupla:
    # (True o False, mensaje)
    exito, mensaje = crear_cliente(datos)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ===================== R · LEER TODOS =====================

def opcion_ver_todos():

    imprimir_titulo("LISTA DE CLIENTES")

    # Obtiene todos los clientes registrados.
    clientes = obtener_todos()

    if not clientes:
        imprimir_info(
            "Todavia no hay clientes. Use la opcion 1 para crear el primero."
        )
    else:
        mostrar_tabla(clientes)

    pausa()


# ===================== S · BUSCAR =====================

def opcion_buscar():

    imprimir_titulo("BUSCAR CLIENTE")

    termino = input("Nombre, email, telefono o ciudad: ")

    # Busca clientes que coincidan con el termino.
    encontrados = buscar_clientes(termino)

    if not encontrados:
        imprimir_info(f"Ningun cliente coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)

    pausa()


# ===================== R · LEER UNO =====================

def opcion_ver_por_id():

    imprimir_titulo("VER CLIENTE POR ID")

    try:

        # int() convierte el texto en numero entero.
        id_cliente = int(input("Id del cliente: "))

    # ValueError ocurre cuando el usuario escribe texto.
    except ValueError:
        imprimir_error("El id debe ser un numero entero")
        return pausa()

    # Busca el cliente por su id.
    cliente = obtener_por_id(id_cliente)

    if not cliente:
        imprimir_error(f"No existe un cliente con id {id_cliente}")

    else:

        # items() devuelve la clave y el valor del diccionario.
        for clave, valor in cliente.a_diccionario().items():

            print(f"  {clave.capitalize():<12}: {valor}")

    pausa()


# ===================== U · ACTUALIZAR =====================

def opcion_actualizar():

    imprimir_titulo("ACTUALIZAR CLIENTE")

    try:
        id_cliente = int(input("Id del cliente: "))

    except ValueError:
        imprimir_error("El id debe ser un numero entero")
        return pausa()

    cliente = obtener_por_id(id_cliente)

    if not cliente:
        imprimir_error(f"No existe un cliente con id {id_cliente}")
        return pausa()

    imprimir_info(f"Editando a {cliente.obtener_nombre_completo()}")

    print("Deje en blanco el campo que no quiera cambiar.\n")

    # Diccionario con los cambios realizados.
    cambios = {}

    # Recorre todos los campos del cliente.
    for campo in CAMPOS_CLIENTE:

        # getattr() obtiene el valor de un atributo usando su nombre.
        actual = getattr(cliente, campo)

        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        # Solo guarda el dato si el usuario escribio algo.
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_cliente(id_cliente, cambios)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ===================== D · ELIMINAR =====================

def opcion_eliminar():

    imprimir_titulo("ELIMINAR CLIENTE")

    try:
        id_cliente = int(input("Id del cliente: "))

    except ValueError:
        imprimir_error("El id debe ser un numero entero")
        return pausa()

    cliente = obtener_por_id(id_cliente)

    if not cliente:
        imprimir_error(f"No existe un cliente con id {id_cliente}")
        return pausa()

    # Muestra el cliente que sera eliminado.
    imprimir_info(f"Se eliminara: {cliente}")

    # confirmar() devuelve True o False.
    if confirmar("Confirma la eliminacion?"):

        exito, mensaje = eliminar_cliente(id_cliente)

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    else:
        imprimir_info("Operacion cancelada")

    pausa()


# ===================== EXTRA · ESTADISTICAS =====================

def opcion_estadisticas():

    imprimir_titulo("ESTADISTICAS")

    # Obtiene el diccionario de estadisticas.
    datos = estadisticas()

    print(f"  Clientes registrados : {datos['total']}")

    # join() une todos los elementos de una lista en un solo texto.
    print(
        f"  Ciudades distintas   : "
        f"{len(datos['ciudades'])} -> "
        f"{', '.join(datos['ciudades'])}"
    )

    print(
        f"  Dominios de email    : "
        f"{', '.join(datos['dominios'])}"
    )

    print(
        f"  Sin telefono         : "
        f"{len(datos['sin_telefono'])}"
    )

    pausa()


# Finaliza el programa.
def salir():

    imprimir_info("Hasta luego!")

    return "salir"


# Diccionario donde cada tecla tiene asociada una funcion.
OPCIONES = {
    "1": ("Crear cliente", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Estadisticas", opcion_estadisticas),
    "0": ("Salir", salir),
}


# Muestra el menu principal.
def mostrar_menu():

    imprimir_titulo("SISTEMA DE GESTION DE CLIENTES")

    # items() devuelve la clave y el valor del diccionario.
    for tecla, (texto, _funcion) in OPCIONES.items():

        print(f"  {tecla}. {texto}")

    print()


# Funcion principal del programa.
def main():

    # Ciclo infinito hasta seleccionar la opcion salir.
    while True:

        mostrar_menu()

        # strip() elimina espacios sobrantes.
        tecla = input("Seleccione una opcion: ").strip()

        # Verifica si la opcion existe en el diccionario.
        if tecla not in OPCIONES:

            imprimir_error("Opcion no valida")

            pausa()

            continue

        # Obtiene la funcion asociada a la opcion.
        _texto, funcion = OPCIONES[tecla]

        # Ejecuta la funcion seleccionada.
        if funcion() == "salir":
            break


# Ejecuta main() solo si este archivo se ejecuta directamente.
if __name__ == "__main__":

    try:
        main()

    # KeyboardInterrupt ocurre cuando el usuario presiona Ctrl + C.
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")


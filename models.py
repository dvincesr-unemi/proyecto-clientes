
import json

# ==========================================================
# TUPLA DE CAMPOS
# ==========================================================
# Contiene los nombres de los campos de un cliente.
# Se usa una tupla porque estos valores son fijos
# y no deben modificarse durante la ejecucion.
CAMPOS_CLIENTE = (
    "nombre",
    "apellido",
    "email",
    "telefono",
    "ciudad",
    "direccion"
)


class Cliente:
    """
    Modelo que representa a un cliente.
    """

    def __init__(self, id_cliente, nombre, apellido, email, telefono, ciudad, direccion):

        # Se usa id_cliente para no sobrescribir la funcion id() de Python.
        self.id = id_cliente

        # Atributos del cliente.
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad
        self.direccion = direccion

    def obtener_nombre_completo(self):
        """
        Une el nombre y apellido en una sola cadena.
        """
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        """
        Convierte el objeto Cliente en un diccionario.
        Este formato puede guardarse facilmente en JSON.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """
        Crea un objeto Cliente a partir de un diccionario.

        @classmethod permite llamar este metodo desde la clase
        sin necesidad de crear un objeto previamente.
        """

        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["telefono"],

            # .get() evita errores si la clave no existe.
            datos.get("ciudad", ""),
            datos.get("direccion", ""),
        )

    def a_json(self):
        """
        Convierte el objeto a una cadena en formato JSON.
        """

        # json.dumps() transforma un objeto de Python en texto JSON.
        return json.dumps(self.a_diccionario(), ensure_ascii=False)

    def __str__(self):
        """
        Define como se mostrara el objeto al usar print().
        """
        return f"[{self.id}] {self.obtener_nombre_completo()} - {self.email}"


class Estudiante:
    """
    Modelo que representa a un estudiante.
    """

    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):

        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet

        # Diccionario donde cada materia almacena una lista de notas.
        # Ejemplo:
        # {"Matematica": [18, 19], "Fisica": [17]}
        self.notas = notas if notas else {}

        # set() elimina automaticamente elementos repetidos.
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        """
        Devuelve el nombre completo del estudiante.
        """
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        """
        Agrega una materia al conjunto.
        """

        # add() agrega un elemento.
        # Si ya existe, no lo repite.
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        """
        Agrega una nota a una materia.
        """

        # Primero asegura que la materia exista.
        self.inscribir_materia(materia)

        # setdefault() crea una lista vacia si la materia aun no existe.
        # Luego append() agrega la nueva nota.
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        """
        Calcula el promedio general del estudiante.
        """

        todas = []

        # values() devuelve todas las listas de notas.
        for lista_notas in self.notas.values():

            # extend() agrega todos los elementos de otra lista.
            todas.extend(lista_notas)

        # Si no existen notas, devuelve cero.
        if not todas:
            return 0

        # sum() suma las notas.
        # len() cuenta cuantas notas existen.
        # round() redondea el resultado a dos decimales.
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante):
        """
        Devuelve las materias que comparten dos estudiantes.
        """

        # "&" realiza la interseccion entre dos conjuntos.
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        """
        Convierte el objeto en un diccionario.
        """

        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,

            # sorted() convierte el conjunto en una lista ordenada,
            # ya que JSON no puede guardar conjuntos.
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls,datos):
        """
        Crea un objeto Estudiante desde un diccionario.
        """

        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],

            # .get() devuelve un diccionario vacio si no existe.
            notas=datos.get("notas", {}),

            # Convierte nuevamente la lista en un conjunto.
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        """
        Define como se mostrara el objeto al imprimirlo.
        """

        return (
            f"[{self.carnet}] "
            f"{self.obtener_nombre_completo()} - "
            f"Promedio: {self.obtener_promedio()}"
        )


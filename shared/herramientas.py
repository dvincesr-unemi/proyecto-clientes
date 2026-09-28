
import os

# ==========================================================
# DICCIONARIO DE COLORES
# ==========================================================
# Cada clave representa un color y su valor es el codigo ANSI
# utilizado por la consola para cambiar el color del texto.
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",

    # Regresa el color normal de la consola.
    "RESET": "\033[0m",
}

# Tupla con las respuestas consideradas como afirmativas.
# Se usa una tupla porque estos valores no cambian.
RESPUESTAS_SI = ("si", "si", "s", "yes", "y")


def limpiar_pantalla():
   #Limpia la consola segun el sistema operativo.

    # os.name identifica el sistema operativo.
    # posix -> Linux o macOS
    # nt -> Windows
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    #Imprime un texto usando un color.

    # .get() busca una clave en el diccionario.
    # Si el color no existe, usa BLANCO por defecto.
    codigo = COLORES.get(color, COLORES["BLANCO"])

    # RESET evita que el siguiente texto conserve el color.
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    
    #Muestra un titulo decorado.
    

    # Limpia la pantalla antes de mostrar el titulo.
    limpiar_pantalla()

    # "=" * 60 repite el caracter "=" sesenta veces.
    imprimir_color("=" * 60, "AZUL")

    # .center() centra el texto en 60 espacios.
    print(f"  {texto}".center(60))

    imprimir_color("=" * 60, "AZUL")

    # Deja una linea en blanco.
    print()


def imprimir_exito(mensaje):
    
    #Muestra un mensaje de exito.
    

    # Reutiliza la funcion imprimir_color().
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    
    #Muestra un mensaje de error.
    

    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    
    #Muestra un mensaje informativo.
    

    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    
    #Solicita una respuesta al usuario.
    #Devuelve True si la respuesta es afirmativa.


    # .strip() elimina espacios al inicio y al final.
    # .lower() convierte el texto a minusculas.
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()

    # "in" verifica si la respuesta esta dentro de la tupla.
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    
    #Realiza una validacion basica de un correo.
    

    # Elimina espacios innecesarios.
    texto = texto.strip()

    # .count() cuenta cuantas veces aparece el simbolo @.
    if texto.count("@") != 1:
        return False

    # .split() divide el texto en usuario y dominio.
    usuario, dominio = texto.split("@")

    # len(usuario) verifica que exista texto antes del @.
    # "." in dominio verifica que exista un punto.
    # .endswith() comprueba que el dominio no termine en punto.
    return (
        len(usuario) > 0
        and "." in dominio
        and not dominio.endswith(".")
    )


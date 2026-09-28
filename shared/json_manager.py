
import json
import os


class GestorJSON:
    
    #Clase encargada de leer y guardar informacion en un archivo JSON.
    

    def __init__(self, ruta):
        # Guarda la ruta del archivo JSON.
        self.ruta = ruta

        # Obtiene el nombre de la carpeta donde estara el archivo.
        carpeta = os.path.dirname(ruta)

        # Si la carpeta no existe, la crea automaticamente.
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self):
        
       #Lee el archivo JSON y devuelve una lista.
        

        # Si el archivo aun no existe, devuelve una lista vacia.
        if not os.path.exists(self.ruta):
            return []

        try:
            # Abre el archivo en modo lectura.
            # encoding="utf-8" permite leer caracteres especiales.
            with open(self.ruta, "r", encoding="utf-8") as archivo:

                # Convierte el contenido del JSON a objetos de Python.
                datos = json.load(archivo)

            # isinstance() verifica que los datos sean una lista.
            # Si no lo son, devuelve una lista vacia.
            return datos if isinstance(datos, list) else []

        # Captura errores si el JSON esta mal escrito
        # o si ocurre un problema al abrir el archivo.
        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        
       # Guarda una lista dentro del archivo JSON.
        

        try:
            # Abre el archivo en modo escritura.
            with open(self.ruta, "w", encoding="utf-8") as archivo:

                # json.dump() convierte objetos de Python a formato JSON.
                # ensure_ascii=False conserva caracteres especiales.
                # indent=2 mejora la legibilidad del archivo.
                json.dump(datos, archivo, ensure_ascii=False, indent=2)

            # Indica que el guardado fue exitoso.
            return True

        # TypeError ocurre cuando JSON no puede convertir un dato.
        # OSError ocurre por problemas con el archivo o permisos.
        except (TypeError, OSError):
            return False

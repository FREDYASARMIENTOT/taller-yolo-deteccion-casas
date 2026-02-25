
import os
import shutil

def copiar_archivo(origen, destino):
    """
    Copia un archivo de una ruta a otra.
    """
    if not os.path.exists(origen):
        raise FileNotFoundError(f"No existe el archivo: {origen}")
    
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy(origen, destino)
    print(f"Archivo copiado correctamente a {destino}")


def listar_archivos(ruta):
    """
    Lista archivos dentro de una carpeta.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"La ruta no existe: {ruta}")
    
    archivos = os.listdir(ruta)
    print("Archivos encontrados:")
    for archivo in archivos:
        print("-", archivo)

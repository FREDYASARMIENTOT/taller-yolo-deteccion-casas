import requests
import os
from pathlib import Path

# Configuración
API_URL = "http://127.0.0.1:8000/detect"
INPUT_FOLDER = "data/test_images"  # Carpeta con tus fotos originales
OUTPUT_FOLDER = "predict/results"  # Donde se guardarán las detecciones

def run_batch_inference():
    # Crear carpetas si no existen
    Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    
    # Listar archivos de imagen
    images = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        print(f"No se encontraron imágenes en {INPUT_FOLDER}")
        return

    print(f"🚀 Iniciando inferencia masiva sobre {len(images)} imágenes...")

    for img_name in images:
        img_path = os.path.join(INPUT_FOLDER, img_name)
        
        # Preparar el archivo para el envío
        with open(img_path, "rb") as f:
            files = {"file": (img_name, f, "image/jpeg")}
            # Solicitamos el formato 'image' para recibir la foto anotada
            params = {"format": "image"}
            
            try:
                response = requests.post(API_URL, files=files, params=params)
                
                if response.status_code == 200:
                    # Guardar la imagen recibida
                    save_path = os.path.join(OUTPUT_FOLDER, f"detected_{img_name}")
                    with open(save_path, "wb") as out_file:
                        out_file.write(response.content)
                    print(f"✅ Procesada: {img_name} -> {save_path}")
                else:
                    print(f"❌ Error en {img_name}: {response.status_code} - {response.text}")
            
            except Exception as e:
                print(f"⚠️ Error de conexión: {e}")

if __name__ == "__main__":
    run_batch_inference()
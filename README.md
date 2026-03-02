
# 🏠 Taller YOLOv8 - Detección de Casas

## 👥 Integrantes

- Jorge Enrique Bravo Rojas
- Fredy Alejandro Sarmiento Torres
- Manuel Alonso Caro Ospina

---

## 📌 Descripción

Proyecto de detección de objetos utilizando YOLOv8 para identificar casas en imágenes. Este taller implementa un modelo de aprendizaje automático basado en YOLOv8 para la detección automática de casas en fotografías.

---

## 📂 Estructura del Proyecto

```
taller-yolo-deteccion-casas/
│
├── src/
│   ├── train_yolo.py          # Script para entrenar el modelo YOLOv8
│   ├── inferencia.py          # Script para realizar inferencia con el modelo entrenado
│   └── utils.py               # Utilidades para manejo de archivos
│
├── models/
│   └── best.pt                # Modelo entrenado (pesos del mejor modelo)
│
├── predict/                   # Carpeta para guardar resultados de predicciones
│
├── data.yaml                  # Configuración del dataset (rutas y clases)
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Este archivo
```

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- GPU recomendada para entrenamiento (opcional, pero acelera significativamente el proceso)

### Pasos de Instalación

1. **Clona o descarga el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd taller-yolo-deteccion-casas
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

   Las dependencias principales incluyen:
   - `ultralytics>=8.0.0`: Biblioteca oficial de YOLOv8
   - `torch` y `torchvision`: PyTorch para deep learning
   - `opencv-python`: Para procesamiento de imágenes
   - `matplotlib`: Para visualización

3. **Verifica la instalación:**
   ```bash
   python -c "import ultralytics; print('YOLOv8 instalado correctamente')"
   ```

---

## 📊 Preparación de Datos

### Formato del Dataset

El proyecto utiliza el formato YOLO para el dataset:

- **data.yaml**: Archivo de configuración que especifica:
  - Rutas a las carpetas de entrenamiento y validación
  - Número de clases (nc: 1)
  - Nombres de las clases (names: ['house'])

- **Estructura esperada del dataset:**
  ```
  dataset/
  ├── train/
  │   ├── images/     # Imágenes de entrenamiento
  │   └── labels/     # Etiquetas en formato YOLO (.txt)
  ├── valid/
  │   ├── images/     # Imágenes de validación
  │   └── labels/     # Etiquetas en formato YOLO (.txt)
  ```

### Archivo data.yaml

Asegúrate de que `data.yaml` tenga las rutas correctas a tu dataset local. Ejemplo:

```yaml
train: ./dataset/train/images
val: ./dataset/valid/images

nc: 1
names: ['house']
```

---

## 🏃‍♂️ Entrenamiento del Modelo

### Uso del Script de Entrenamiento

Para entrenar el modelo, utiliza el script `src/train_yolo.py`:

```bash
python src/train_yolo.py --data data.yaml --epochs 50 --imgsz 640 --batch 16 --name mi_experimento
```

### Parámetros del Entrenamiento

- `--data`: Ruta al archivo `data.yaml` (requerido)
- `--epochs`: Número de épocas de entrenamiento (default: 50)
- `--imgsz`: Tamaño de las imágenes (default: 640)
- `--batch`: Tamaño del batch (default: 16)
- `--name`: Nombre del experimento (default: "yolo_experiment")

### Ejemplo de Entrenamiento

```bash
python src/train_yolo.py --data data.yaml --epochs 100 --batch 8 --name casas_v1
```

El modelo entrenado se guardará en la carpeta `runs/detect/<name>/weights/best.pt`.

---

## 🔍 Inferencia y Predicción

### Uso del Script de Inferencia

Para realizar predicciones con el modelo entrenado, utiliza `src/inferencia.py`:

```bash
python src/inferencia.py --model models/best.pt --source ruta/a/imagen.jpg --conf 0.5 --save
```

### Parámetros de Inferencia

- `--model`: Ruta al modelo entrenado (.pt) (requerido)
- `--source`: Ruta a imagen, carpeta o video (requerido)
- `--conf`: Umbral de confianza (default: 0.25)
- `--save`: Guardar resultados en carpeta `runs/detect/predict/`

### Ejemplos de Inferencia

**Predicción en una imagen:**
```bash
python src/inferencia.py --model models/best.pt --source test_image.jpg --save
```

**Predicción en una carpeta de imágenes:**
```bash
python src/inferencia.py --model models/best.pt --source ./test_images/ --save
```

Los resultados se guardarán en la carpeta `predict/` si se usa `--save`.

---

## � Integración con FastAPI

### Descripción

Se ha integrado **FastAPI** para proporcionar una API REST que permite realizar detecciones de casas a través de peticiones HTTP. Esta integración facilita el despliegue y la integración con aplicaciones web y móviles.

### Instalación de FastAPI

FastAPI se incluye en `requirements.txt`. Para instalarlo explícitamente:

```bash
pip install fastapi uvicorn python-multipart pillow
```

Dependencias principales:
- **fastapi**: Framework web moderno para construir APIs
- **uvicorn**: Servidor ASGI para ejecutar la aplicación
- **python-multipart**: Para manejo de formularios multipart
- **pillow**: Para procesamiento de imágenes

### Uso del API

#### Iniciar el Servidor

```bash
python src/main.py
```

O usando uvicorn directamente:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en `http://localhost:8000`

#### Endpoint: Detección de Imagen

**POST** `/detect`

**Descripción:** Realiza detección de casas en una imagen enviada.

**Parámetros:**
- `file` (form-data, multipart/form-data): Archivo de imagen (JPG, PNG, etc.)
- `confidence` (query, opcional): Umbral de confianza (0.0 - 1.0, default: 0.25)

**Ejemplo con curl:**

```bash
curl -X POST "http://localhost:8000/detect" \
  -F "file=@ruta/a/imagen.jpg" \
  -F "confidence=0.5"
```

**Ejemplo con Python requests:**

```python
import requests

with open("imagen.jpg", "rb") as img:
    files = {"file": img}
    params = {"confidence": 0.5}
    response = requests.post("http://localhost:8000/detect", files=files, params=params)
    result = response.json()
    print(result)
```

**Respuesta (JSON):**

```json
{
  "detected_objects": [
    {
      "class": "house",
      "confidence": 0.95,
      "bbox": [x1, y1, x2, y2]
    }
  ],
  "image_size": [width, height],
  "num_detections": 1
}
```

#### Endpoint: Health Check

**GET** `/health`

**Descripción:** Verifica el estado del servidor y del modelo.

**Respuesta:**

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### Endpoint: Documentación Interactiva

**GET** `/docs`

Accede a la documentación interactiva de Swagger UI en: `http://localhost:8000/docs`

**GET** `/redoc`

Accede a la documentación alternativa ReDoc en: `http://localhost:8000/redoc`

### Características del API

- ✅ Carga automática del modelo entrenado (`models/best.pt`)
- ✅ Validación de imágenes
- ✅ Procesamiento asincrónico
- ✅ Documentación automática (Swagger/OpenAPI)
- ✅ Manejo de errores robusto
- ✅ Soporte para múltiples formatos de imagen

### Ejemplo de Cliente Web

```python
import requests
from pathlib import Path

def detect_house(image_path, confidence=0.5):
    """Realiza detección en una imagen"""
    url = "http://localhost:8000/detect"
    
    with open(image_path, "rb") as img:
        files = {"file": img}
        params = {"confidence": confidence}
        
        try:
            response = requests.post(url, files=files, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la detección: {e}")
            return None

# Usar la función
result = detect_house("test_image.jpg", confidence=0.6)
if result:
    print(f"Casas detectadas: {result['num_detections']}")
    for obj in result['detected_objects']:
        print(f"  - {obj['class']}: {obj['confidence']:.2%} confianza")
```

---

## �🛠️ Utilidades

El archivo `src/utils.py` contiene funciones auxiliares:

### Copiar Archivos

```python
from src.utils import copiar_archivo

copiar_archivo("origen/archivo.txt", "destino/archivo.txt")
```

### Listar Archivos

```python
from src.utils import listar_archivos

listar_archivos("ruta/a/carpeta")
```

---

## 📊 Resultados

### Métricas del Modelo Entrenado

#### Desempeño de Detección

| Métrica | Valor | Porcentaje |
|---------|-------|-----------|
| **mAP@50** | 0.995 | 99.50% |
| **mAP@50-95** | 0.94 | 94.00% |
| **Precision** | 0.99 | 99.00% |
| **Recall** | 1.00 | 100.00% |

**Resumen:** ✅ **Excelente** - El modelo presenta métricas muy altas en todos los indicadores, mostrando un desempeño excepcional en la detección de casas. Precisión general: **98.75%**

#### Descripción de Métricas

- **mAP@50**: Mean Average Precision evaluada a IoU threshold de 0.50
- **mAP@50-95**: Mean Average Precision promedio entre IoU thresholds de 0.50 a 0.95
- **Precision**: Proporción de predicciones positivas correctas en relación a todas las predicciones
- **Recall**: Proporción de casos positivos reales identificados correctamente por el modelo

### Detalles del Entrenamiento

| Parámetro | Valor |
|-----------|-------|
| **Modelo Base** | YOLOv8n (nano) |
| **Hardware** | GPU T4 en Google Colab |
| **Épocas** | Variable (depende del entrenamiento) |
| **Dataset** | Imágenes de casas con anotaciones |
| **Clases** | 1 (house) |
| **Ruta del Modelo** | `models/best.pt` |

### Configuración de Inferencia

- **Confianza por Defecto**: 0.25
- **Formatos Soportados**: JPG, JPEG, PNG, BMP, TIFF
- **Velocidad de Inferencia**: Fast (YOLOv8n)
- **Formato de Salida**: YOLO format con bounding boxes

### Exportar Métricas

Para generar un reporte detallado de métricas, ejecuta:

```bash
python metrics_reporter.py
```

Este comando generará:
- Reporte formateado en consola
- Archivo `metrics_report.txt` con todas las métricas
- Acceso programático a métricas individuales mediante la clase `MetricsReporter`

---

## 🔧 Solución de Problemas

### Errores Comunes

1. **Error de CUDA/GPU:**
   - Asegúrate de tener PyTorch con soporte CUDA instalado
   - Si no tienes GPU, el entrenamiento será más lento pero funcionará en CPU

2. **Rutas incorrectas en data.yaml:**
   - Verifica que las rutas en `data.yaml` apunten a carpetas existentes
   - Usa rutas absolutas si es necesario

3. **Dependencias faltantes:**
   - Ejecuta `pip install -r requirements.txt` nuevamente
   - Verifica la versión de Python (3.8+)

4. **Modelo no encontrado:**
   - Asegúrate de que `models/best.pt` exista
   - Si entrenaste un modelo nuevo, actualiza la ruta

### Consejos de Optimización

- Para datasets pequeños, reduce el batch size
- Aumenta las épocas para mejores resultados (hasta 100-200)
- Usa GPU para acelerar el entrenamiento
- Ajusta el confidence threshold según tus necesidades

---

## 📚 Referencias

- [Documentación oficial de YOLOv8](https://docs.ultralytics.com/)
- [PyTorch](https://pytorch.org/)
- [OpenCV](https://opencv.org/)

---

## 📄 Licencia

Este proyecto es parte de un taller académico. Consulta con los autores para uso comercial.

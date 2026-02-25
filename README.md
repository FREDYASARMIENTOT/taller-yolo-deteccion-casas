
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

## 🛠️ Utilidades

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

- **mAP@50**: 0.995
- **mAP@50-95**: 0.94
- **Precision**: 0.99
- **Recall**: 1.00

### Detalles del Entrenamiento

- Modelo base: YOLOv8n (nano)
- Hardware: GPU T4 en Google Colab
- Épocas: Variable (depende del entrenamiento)
- Dataset: Imágenes de casas con anotaciones

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

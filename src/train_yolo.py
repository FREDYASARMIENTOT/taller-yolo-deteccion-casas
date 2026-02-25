
from ultralytics import YOLO
import argparse

def main():
    parser = argparse.ArgumentParser(description="Entrenamiento YOLOv8")
    parser.add_argument("--data", type=str, required=True, help="Ruta al data.yaml")
    parser.add_argument("--epochs", type=int, default=50, help="Número de épocas")
    parser.add_argument("--imgsz", type=int, default=640, help="Tamaño de imagen")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--name", type=str, default="yolo_experiment", help="Nombre del experimento")

    args = parser.parse_args()

    model = YOLO("yolov8n.pt")

    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        name=args.name
    )

    print("Entrenamiento completado correctamente.")

if __name__ == "__main__":
    main()

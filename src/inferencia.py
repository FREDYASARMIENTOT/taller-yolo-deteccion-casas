
from ultralytics import YOLO
import argparse

def main():
    parser = argparse.ArgumentParser(description="Inferencia con modelo YOLOv8 entrenado")
    parser.add_argument("--model", type=str, required=True, help="Ruta al modelo .pt")
    parser.add_argument("--source", type=str, required=True, help="Ruta a imagen o carpeta")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--save", action="store_true", help="Guardar resultados")

    args = parser.parse_args()

    model = YOLO(args.model)

    results = model.predict(
        source=args.source,
        conf=args.conf,
        save=args.save
    )

    print("Inferencia completada correctamente.")

if __name__ == "__main__":
    main()

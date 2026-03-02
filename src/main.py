from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import StreamingResponse, JSONResponse
from ultralytics import YOLO
from PIL import Image
import io
import uvicorn

app = FastAPI()

# Carga el modelo una sola vez al iniciar
model = YOLO("models/best.pt")

@app.post("/detect")
async def detect(
    file: UploadFile = File(...),
    format: str = Query("image", pattern="^(image|json)$")
):  # <--- Aquí faltaba cerrar el paréntesis y los dos puntos
    
    # 1. Leer el contenido del archivo subido
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    # 2. Ejecutar la inferencia
    results = model.predict(source=img, conf=0.25)
    res = results[0]

    # 3. Preparar la imagen anotada (con cajas y scores)
    annotated = res.plot()  # Devuelve un array de numpy
    pil_img = Image.fromarray(annotated)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)

    # 4. Extraer la lista de detecciones para el JSON o Headers
    det_list = []
    for box in res.boxes:
        xyxy = box.xyxy.tolist()[0] if hasattr(box.xyxy, "tolist") else []
        det_list.append({
            "xyxy": xyxy,
            "cls": int(box.cls),
            "conf": float(box.conf)
        })

    headers = {"X-Detections": str(det_list)}

    # 5. Retornar según el formato solicitado
    if format == "json":
        return JSONResponse(content={"detections": det_list}, headers=headers)

    return StreamingResponse(buf, media_type="image/png", headers=headers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
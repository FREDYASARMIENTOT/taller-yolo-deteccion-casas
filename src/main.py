from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import StreamingResponse, JSONResponse
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()

# load the model once
model = YOLO("models/best.pt")

@app.post("/detect")
async def detect(
    file: UploadFile = File(...),
    format: str = Query("image", regex="^(image|json)$")
):
    # read uploaded contents
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    # run inference
    results = model.predict(source=img, conf=0.25)
    res = results[0]

    # prepare annotated image
    annotated = res.plot()  # numpy array
    pil_img = Image.fromarray(annotated)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)

    # extract detections
    det_list = []
    for box in res.boxes:
        xyxy = box.xyxy.tolist()[0] if hasattr(box.xyxy, "tolist") else []
        det_list.append({
            "xyxy": xyxy,
            "cls": int(box.cls),
            "conf": float(box.conf)
        })

    headers = {"X-Detections": str(det_list)}

    if format == "json":
        return JSONResponse(content={"detections": det_list}, headers=headers)

    return StreamingResponse(buf, media_type="image/png", headers=headers)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

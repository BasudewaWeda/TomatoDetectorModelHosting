from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from ultralytics import YOLO

app = FastAPI()
model = YOLO("best.pt")

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.post('/predict')
async def predict(image: UploadFile = File(...)):
    if image.filename == "":
        return {"message": "No image file uploaded!"}, 400

    image_bytes = await image.read()
    opencv_image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    results = model(opencv_image)  # Replace with your model call

    fresh_count = 0
    rotten_count = 0

    for result in results:
        for box in result.boxes:
            if box.conf >= 0.4:
                if box.cls[0] == 0 or box.cls[0] == 2:
                    fresh_count += 1
                else:
                    rotten_count += 1

    response_data = {
        "fresh": fresh_count,
        "rotten": rotten_count,
    }

    return response_data

from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
from ultralytics import YOLO
import io

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
    pillow_image = Image.open(io.BytesIO(image_bytes))
    opencv_image = np.array(pillow_image)

    results = model(opencv_image)

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

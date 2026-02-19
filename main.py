from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uuid
import os
from PIL import Image, ImageEnhance

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Photo Enhance API Running"}

@app.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):
    
    unique_id = str(uuid.uuid4())
    input_path = f"input_{unique_id}.jpg"
    output_path = f"output_{unique_id}.jpg"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = Image.open(input_path)

    sharp = ImageEnhance.Sharpness(image)
    image = sharp.enhance(2.5)

    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(1.5)

    brightness = ImageEnhance.Brightness(image)
    image = brightness.enhance(1.2)

    image.save(output_path)

    os.remove(input_path)

    return FileResponse(output_path, media_type="image/jpeg")

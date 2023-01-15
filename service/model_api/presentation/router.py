from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile

from presentation.dependencies import container

router = APIRouter(prefix="")


@router.post("/predict")
async def process_image(image: UploadFile):
    with NamedTemporaryFile() as file:
        file.write(await image.read())
        prediction = container.ml_service.predict(file.name)
        return {"prediction": float(prediction)}

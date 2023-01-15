import ujson
from fastapi import APIRouter, HTTPException, Request, UploadFile, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

import cv2
import numpy as np
from core.base import logger
from presentation.logs_utils import LoggerRouteHandler
from schemas.markup import Markup, Prediction

router = APIRouter(prefix="", route_class=LoggerRouteHandler)


@router.post("/predict", response_model=Prediction)
async def process_image(request: Request, image: UploadFile, markup: UploadFile):
    markup_content = await markup.read()
    try:
        markup_content_json = ujson.loads(markup_content)
        markup_obj = Markup.parse_obj(markup_content_json)

        jpg_as_np = np.frombuffer(await image.read(), dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        assert img.shape[0] > 5 and img.shape[1] > 5, "image size should be greater than 5x5"
    except ujson.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="markup.should.be.json.parsable")
    except ValidationError as exc:
        raise RequestValidationError(errors=exc.raw_errors)
    except AssertionError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="image.size.should.be.greater.than.5x5"
        )
    except Exception:
        logger.warning({"status": "unknown.image.parsing.error"}, exc_info=True)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="unknown.image.parsing.error")

    prediction = await request.app.processing_service.process_image(img, markup_obj)
    return Prediction(prediction=prediction)

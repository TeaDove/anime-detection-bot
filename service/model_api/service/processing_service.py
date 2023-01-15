from typing import Dict

import numpy as np
from schemas.markup import Markup
from service.ml_service import MlService


class ProcessingService:
    ml_service = MlService()

    async def process_image(self, image: np.ndarray, markup: Markup) -> Dict[str, bool]:
        return self.ml_service.predict(image, markup.markup)

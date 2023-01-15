from pathlib import Path
from typing import List, Tuple

import numpy as np
from core.settings import model_settings
from inference.inference import ParkfinderYOLOv4
from service.weights_service import WeightsService


class MlService:
    weights_service = WeightsService()

    def __init__(self):
        weights_files = self.weights_service.safe_weights_file()
        self.model = ParkfinderYOLOv4(path_to_weights=weights_files, path_to_cfg=Path("core/yolov4-obj.cfg"))

    def predict(self, image: np.ndarray, image_markup: List[Tuple[float, float]]):
        return self.model.predict(image, image_markup, th=model_settings.threshold, nms_th=model_settings.nms_threshold)

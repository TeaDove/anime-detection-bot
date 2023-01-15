from dataclasses import dataclass

from inference.inference import AnimePredictor
from supplier.s3_supplier import S3Supplier


@dataclass
class MlService:
    s3_supplier: S3Supplier

    def __post_init__(self):
        weights_files = self.s3_supplier.safe_weights_file()
        self.model = AnimePredictor(weights_files=weights_files)

    def predict(self, image: str):
        return self.model.make_prediction(image)

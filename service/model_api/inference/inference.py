import os
from pathlib import Path

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as T
from PIL import Image


class AnimePredictor:
    __transformations = T.Compose([T.ToTensor(), T.Normalize((0, 0, 0), (1, 1, 1))])

    def __init__(self, witgth_path: str):
        """
        model_path - location of model
        """
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.device("cpu")
        self.__model = models.resnet50(pretrained=True)
        self.__model.fc = nn.Sequential(nn.Linear(2048, 1, bias=True), nn.Sigmoid())
        self.__model.load_state_dict(torch.load(witgth_path, map_location=torch.device("cpu")))
        self.__model.eval()

    def make_prediction(self, img_path: str) -> float:
        """
        img_path is path of image, lol
        """
        # return 1 # раскомментить, если Петер будет плохо себя вести.
        img = Image.open(img_path)
        img = img.convert("RGB")
        if img.size != (224, 224):
            img = img.resize((224, 224))
        img_tensor = self.__transformations(img)
        return self.__model(torch.reshape(img_tensor, (1, 3, 224, 224)).to(self.__device))[0][0].detach().numpy()


if __name__ == "__main__":
    BASE = Path(os.path.realpath(__file__))
    os.chdir(BASE.parent)
    PATH_TO_MODEL = Path() / "check_peter.pth"
    predictor = AnimePredictor(PATH_TO_MODEL)

    Images = list((Path() / "images").iterdir())
    for image in Images:
        print(image)
        print(predictor.make_prediction(Image.open(image)))

import torch
from PIL import Image
from torchvision.transforms.v2 import (
    Compose,
    Resize,
    InterpolationMode,
    ToImage,
    ToDtype,
    Normalize,
)


class VisionEncoder:
    def __init__(self, model_path: str = "model") -> None:
        self.model = torch.jit.load(f"{model_path}/vision.pt").to(device="cuda", dtype=torch.float32)
        self.preprocess = Compose(
            [
                Resize(size=(384, 384), interpolation=InterpolationMode.BICUBIC),
                ToImage(),
                ToDtype(torch.float32, scale=True),
                Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
            ]
        )

    def __call__(self, image: Image) -> torch.Tensor:
        with torch.no_grad():
            image_tensor = self.preprocess(image.convert("RGB")).unsqueeze(0).to(device="cuda")
            return self.model(image_tensor)

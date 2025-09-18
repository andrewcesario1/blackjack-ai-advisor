import torch

data = torch.load("../models/expert_pretrained.pth", map_location="cpu", weights_only=False)
preprocessor = data["preprocessor"]
scaler = preprocessor.named_transformers_["num"]
print("numMean =", scaler.mean_)
print("numStd  =", scaler.scale_)

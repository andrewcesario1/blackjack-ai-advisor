import torch

# 1) Load checkpoint
data = torch.load("expert_pretrained.pth", map_location="cpu", weights_only=False)

# 2) Pull out the ColumnTransformer
preprocessor = data["preprocessor"]

# 3) Grab the StandardScaler under the name "num"
scaler = preprocessor.named_transformers_["num"]

# 4) Print its mean_ and scale_ arrays
print("numMean =", scaler.mean_)    # e.g. [13.2, 0.5]
print("numStd  =", scaler.scale_)   # e.g. [ 4.1, 7.8]

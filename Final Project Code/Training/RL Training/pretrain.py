# pretrain.py

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1) Load expert CSV
df = pd.read_csv("expert_strategy.csv")

# Data Cleaning Step for 'dealerUp':
# If '11' in the 'dealerUp' column from the CSV represents an Ace,
# map it to 1.0 to be consistent with the environment's card value (Ace=1).
# Also ensure the column is float type.
if 'dealerUp' in df.columns:
    df['dealerUp'] = df['dealerUp'].replace(11, 1.0)
    df['dealerUp'] = df['dealerUp'].astype(float) # Ensure it's float

X_df = df[["playerTotal","isSoft","dealerUp","runningCount","canDouble"]]
y    = df["action"].map({"H":0,"S":1,"D":2}).values

# 2) Build and fit the preprocessing transformer

# Define categories explicitly based on game rules
is_soft_categories = [0.0, 1.0]
dealer_up_categories = [float(i) for i in range(1, 11)] # Should now match cleaned data
can_double_categories = [0.0, 1.0]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["playerTotal","runningCount"]),
    ("cat", OneHotEncoder(
                categories=[is_soft_categories, dealer_up_categories, can_double_categories],
                drop="first",
                sparse_output=False,
                handle_unknown='error'
             ),
             ["isSoft","dealerUp","canDouble"]),
])
X_proc = preprocessor.fit_transform(X_df)

# 3) Train/validation split on processed features
X_tr, X_val, y_tr, y_val = train_test_split(
    X_proc, y, stratify=y, test_size=0.2, random_state=42
)

# 4) Wrap in PyTorch datasets (float32 / long)
train_ds = TensorDataset(
    torch.from_numpy(X_tr).float(),
    torch.from_numpy(y_tr).long()
)
val_ds   = TensorDataset(
    torch.from_numpy(X_val).float(),
    torch.from_numpy(y_val).long()
)
tr_loader  = DataLoader(train_ds, batch_size=256, shuffle=True)
val_loader = DataLoader(val_ds,   batch_size=256)

# 5) Define the MLP
class ExpertMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64), nn.ReLU(),
            nn.Linear(64, 64),         nn.ReLU(),
            nn.Linear(64, 3)
        )
    def forward(self, x):
        return self.net(x)

model = ExpertMLP(X_proc.shape[1]).to(device)
opt   = torch.optim.Adam(model.parameters(), lr=1e-3)
lossf = nn.CrossEntropyLoss()

# 6) Train until ≥99.5% val acc
for epoch in range(1, 101):
    model.train()
    for xb, yb in tr_loader:
        xb, yb = xb.to(device), yb.to(device)
        pred   = model(xb)
        loss   = lossf(pred, yb)
        opt.zero_grad()
        loss.backward()
        opt.step()

    # Eval
    model.eval()
    correct = 0
    total   = 0
    with torch.no_grad():
        for xb, yb in val_loader:
            xb, yb = xb.to(device), yb.to(device)
            correct += (model(xb).argmax(1) == yb).sum().item()
            total   += yb.size(0)
    acc = correct / total
    print(f"Epoch {epoch:3d}: Val Acc = {acc:.4%}")
    if acc >= 0.995:
        break

# 7) Save transformer + model
torch.save({
    "preprocessor": preprocessor,
    "model_state":  model.state_dict()
}, "expert_pretrained.pth")
print("✔ Saved expert_pretrained.pth with transformer + weights")

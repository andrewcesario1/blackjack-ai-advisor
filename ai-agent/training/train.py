# train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1) Load expert CSV
df = pd.read_csv("expert_strategy.csv")
X = df[["playerTotal","isSoft","dealerUp","runningCount","canDouble"]]
y = df["action"]

# 2) Build a preprocessing pipeline:
#    - Scale the continuous features (playerTotal, runningCount)
#    - One-hot the discrete ones (isSoft, dealerUp, canDouble)
preprocessor = ColumnTransformer([
    ("num", StandardScaler(),      ["playerTotal","runningCount"]),
    ("cat", OneHotEncoder(drop="first"), ["isSoft","dealerUp","canDouble"]),
])

# 3) Create a full pipeline: preprocess → MLP
clf = Pipeline([
    ("pre", preprocessor),
    ("mlp", MLPClassifier(
        hidden_layer_sizes=(64,64),
        activation="relu",
        solver="lbfgs",       # better for small/medium data
        max_iter=1000,        # allow full convergence
        random_state=42
    )),
])

# 4) Train/validation split (stratify to keep class balance)
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5) Fit the model
clf.fit(X_train, y_train)

# 6) Evaluate
y_pred = clf.predict(X_val)
val_acc = accuracy_score(y_val, y_pred)
print(f"Validation accuracy: {val_acc:.4%}\n")
print("Classification Report:")
print(classification_report(y_val, y_pred))

# 7) Save the pipeline (preprocessor + model)
joblib.dump(clf, "policy_pretrained.pkl")
print("\nSaved pretrained policy to policy_pretrained.pkl")

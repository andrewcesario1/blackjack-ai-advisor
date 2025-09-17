import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

df = pd.read_csv("expert_strategy.csv")
X = df[["playerTotal","isSoft","dealerUp","runningCount","canDouble"]]
y = df["action"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["playerTotal","runningCount"]),
    ("cat", OneHotEncoder(drop="first"), ["isSoft","dealerUp","canDouble"]),
])

clf = Pipeline([
    ("pre", preprocessor),
    ("mlp", MLPClassifier(
        hidden_layer_sizes=(64,64),
        activation="relu",
        solver="lbfgs",
        max_iter=1000,
        random_state=42
    )),
])

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_val)
val_acc = accuracy_score(y_val, y_pred)
print(f"Validation accuracy: {val_acc:.4%}\n")
print("Classification Report:")
print(classification_report(y_val, y_pred))

joblib.dump(clf, "policy_pretrained.pkl")
print("\nSaved pretrained policy to policy_pretrained.pkl")

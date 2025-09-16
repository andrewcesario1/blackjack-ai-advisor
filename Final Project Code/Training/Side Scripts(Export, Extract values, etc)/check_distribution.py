import pandas as pd

df = pd.read_csv("sim_data.csv")
df = df[df["action"].isin(["Hit","Stand","Double"])]
print(df["action"].value_counts(normalize=True))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Chargement des données
df = pd.read_csv("data/raw/admission.csv")

# Suppression de la colonne Serial No.
df = df.drop(columns="Serial No.", axis=1)

# Définition X, y
y = df["Chance of Admit"]
X= df.drop(columns="Chance of Admit", axis=1)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)

# Enregistrement des données
X_train.to_csv("data/processed/X_train.csv", index=False)
X_test.to_csv("data/processed/X_test.csv", index=False)
y_train.to_csv("data/processed/y_train.csv", index=False)
y_test.to_csv("data/processed/y_test.csv", index=False)

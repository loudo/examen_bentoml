import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import bentoml
from bentoml.io import NumpyNdarray

# Chargement des données
X_train = pd.read_csv("data/processed/X_train.csv")
X_test = pd.read_csv("data/processed/X_test.csv")
y_train = pd.read_csv("data/processed/y_train.csv")
y_test = pd.read_csv("data/processed/y_test.csv")

# Standardisation des données
scaler = StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Création d'une régression linéaire
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)

print('score train :',lr.score(X_train_scaled, y_train))
print('score test :',lr.score(X_test_scaled, y_test))

pred_train = lr.predict(X_train_scaled)
pred_test = lr.predict(X_test_scaled)

print('rmse train :', np.sqrt(mean_squared_error(y_train, pred_train)))
print('rmse test : ', np.sqrt(mean_squared_error(y_test, pred_test)))

# Sauvegarde des modèles
model_ref = bentoml.sklearn.save_model("admission_lr", lr)
print(f"Modèle enregistré sous : {model_ref}")



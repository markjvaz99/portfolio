import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

cwd = os.getcwd()

df = pd.read_csv(f"{cwd}/data/processed/cleaned.csv")

X = df[['GrLivArea', 'BedroomAbvGr', 'FullBath']]
y = df['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

models = {
    "linear": LinearRegression(),
    "ridge": Ridge(),
    "lasso": Lasso()
}

for name, model in models.items():
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    
    print(f"{name} RMSE:", mean_squared_error(y_test, preds))
    print(f"{name} R2:", r2_score(y_test, preds))
    
    joblib.dump(model, f"models/{name}.pkl")

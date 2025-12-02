import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("train (1).csv")
df.head()
df.info()
df.describe()

df.isnull().sum().sort_values(ascending=False).head(20)

sns.histplot(df['SalePrice'],kde=True)
plt.title("SalePrice Distribution")

df["SalePrice_log"]=np.log1p(df["SalePrice"])

features = [
    "OverallQual","GrLivArea","GarageCars",
    "TotalBsmtSF","Fullbath","YearBuilt","Neighborhood"
]

X=df[features]
y=df["SalePrice_log"]

from sklearn.model_selection import train_test_split
X_train , X_valid , Y_train , Y_valid = train_test_split(X,y,test_size=0.2,random_state=42)

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

numeric_features = ["GrzlivArea","TotalBsmtSF","YearBuilt"]

numeric_transformer = Pipeline(steps=[("imputer",SimpleImputer(strategy="median")),("scaler",StandardScaler())])

categorial_features = ["Neighborhood"]

categorial_transformer = Pipeline(steps=[("imputer",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore"))])

preprocessor = ColumnTransformer(
    transformers=[
        ("num",numeric_transformer,numeric_features),
        ("cat",categorial_transformer,categorial_features)
])

from sklearn.linear_model import LinearRegression

pipeline = Pipeline(steps=[
    ("preprocessor",preprocessor),
    ("model",LinearRegression())
])
pipeline.fit(X_train,Y_train)

from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score

y_pred = pipeline.predict(X_valid)

rmse = np.sqrt(mean_squared_error(Y_valid,y_pred))
mae=mean_absolute_error(Y_valid)
r2=r2_score(Y_valid,y_pred)

print(f"RMSE:{rmse}")
print(f"mae:{mae}")
print(f"R2 Score:{r2}")

from sklearn.model_selection import cross_val_score,KFold

kf=KFold(n_splits=5,shuffle=True,random_state=42)
scores=-cross_val_score(pipeline,X,y,scoring="neg_root_mean_squared_error",cv=kf)
print("Cross-Validation RMSE:",scores.mean())

from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

ridge = Pipeline(steps=[
    ("preprocessor",preprocessor),
    ("ridge",Ridge())
])

params = {"ridge__alpha":[0.1,1,10,50,100]}

grid=GridSearchCV(ridge,params,cv=5,scoring="neg_root_mean_squared_error")
grid.fit(X,y)

print(grid.best_params_)
print(-grid.best_score_)

y_valid_orig = np.expm1(Y_valid)
y_pred_orig=np.expm1(y_pred)

rmse_original=np.sqrt(mean_squared_error(y_valid_orig,y_pred_orig))
print("RMSE (Actual Prices):",rmse_original)

import joblib
joblib.dump(pipeline,"house_price_model.pkl")

test_df=pd.read_csv("test(1).csv")
X_test=test_df[features]

preds_log = pipeline.predict(X_test)
preds = np.expm1(preds_log)
import pandas as pd 

df = pd.read_csv("titanic_data.csv")
pd.set_option('display.max_rows', 1000) 

print(df.head(10))
print(df.info())

del df["Cabin"]
print(df.info())

dfTitanic = df.dropna(subset=["Survived", "Pclass", "Age", "Sex"]).copy()
print(dfTitanic.info())

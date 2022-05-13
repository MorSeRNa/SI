import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from sklearn import linear_model


with open("users_IA_clases.json", "r") as file:
    data = json.load(file)


df = pd.DataFrame(data['usuarios'])

for index, row in df.iterrows():
    if row["emails_phishing_recibidos"] == 0:
        df._set_value(index, "prob_click", 0)
    else:
        df._set_value(index, "prob_click", row["emails_phishing_clicados"] / row["emails_phishing_recibidos"])
df_data = df.to_numpy()


##linear regression##

df_data = df_data[:, np.newaxis, 2]


regr = linear_model.LinearRegression()
regr.fit(df_data, df["prob_click"].to_numpy())

df_vuln_pred = regr.predict(df_data)


################################################################################################################

with open("users_IA_predecir.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data['usuarios'])

for index, row in df.iterrows():
    if row["emails_phishing_recibidos"] == 0:
        df._set_value(index, "prob_click", 0)
    else:
        df._set_value(index, "prob_click", row["emails_phishing_clicados"] / row["emails_phishing_recibidos"])
df_data = df.to_numpy()



df_data=df_data[:,np.newaxis,2]
regresion = regr.predict(df_data)

plt.scatter(df_data, regresion, color="black")
plt.plot(df_data, regresion, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()
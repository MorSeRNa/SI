import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
import graphviz


with open("users_IA_clases.json", "r") as file:
    data = json.load(file)


df = pd.DataFrame(data['usuarios'])

for index, row in df.iterrows():
    if row["emails_phishing_recibidos"] == 0:
        df._set_value(index, "prob_click", 0)
    else:
        df._set_value(index, "prob_click", row["emails_phishing_clicados"] / row["emails_phishing_recibidos"])
df_data = df.to_numpy()



## Decisión tree ##
X = df.iloc[:, 4].values
X, y = X.reshape(-1,1), df["vulnerable"].to_numpy()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)


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

clf.predict(df["prob_click"].values.reshape(-1, 1))

dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("decisiontree")
dot_data = tree.export_graphviz(clf, out_file=None,filled=True, rounded=True,special_characters=True)
graph = graphviz.Source(dot_data)
graph.render('decisiontree.gv', view=True).replace('\\', '/')

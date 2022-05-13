import pandas as pd
import json
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


X = df.iloc[:, 4].values
X, y = X.reshape(-1,1), df["vulnerable"].to_numpy()
clf = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
clf.fit(X, y)

################################################################################################################

with open("users_IA_predecir.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data['usuarios'])
for index, row in df.iterrows():
    if row["emails_phishing_recibidos"] == 0:
        df._set_value(index, "prob_click", 0)
    else:
        df._set_value(index, "prob_click", row["emails_phishing_clicados"] / row["emails_phishing_recibidos"])



print(clf.predict(df["prob_click"].values.reshape(-1, 1)))

for i in range(len(clf.estimators_)):
    estimator = clf.estimators_[i]
    dot_data= export_graphviz(estimator,out_file=None,rounded=True, proportion=False,precision=2, filled=True)
    graph = graphviz.Source(dot_data)
    graph.render('randomforest'+str(i)+'.gv', view=True).replace('\\', '/')

import sqlite3
import pandas as pd
from ast import literal_eval
import statistics
import numpy as np
import math
import matplotlib.pyplot as plt
import hashlib

def esPasswordSegura(password):
    with open("10k-most-common.txt", encoding='utf8') as f:
        for i in f.read().splitlines():
            linea = hashlib.md5(bytes(i, encoding='utf8'))
            if linea.hexdigest() == password:
                return 1
    return 0

def usuarios_vulnerables(con):
    df = pd.read_sql_query("SELECT * from usuarios", con)
    for index, row in df.iterrows():
        if(literal_eval(row["emails"])["phishing"] != 0):
            df._set_value(index, "probabilidad", (literal_eval(row["emails"])["cliclados"]/literal_eval(row["emails"])["phishing"])*100)
        else:
            df._set_value(index, "probabilidad", 0)
        df._set_value(index, "secure_pass", esPasswordSegura(row["contrasena"]))
    
    df = df[df["secure_pass"] == 0]
    df = df.sort_values(["probabilidad"], ascending=[False])

    print(df)
    df = df.head(10)
    plt.bar(np.arange(len(df)), df['probabilidad'], width=0.4, color='r', label='cookies')
    plt.xticks(np.arange(len(df))+0.4, df["id_usuario"])
    plt.xlabel('Usuarios')
    plt.ylabel('Probabilidad de click')
    plt.title('Top 10 usuarios críticos')
    plt.show()

def politicas_desactualizadas():
    df = pd.read_sql_query("SELECT * from legal ORDER BY url", con)
    df["Politicas"] = 3 - df["cookies"] - df["aviso"] - df["proteccion_de_datos"]
    df = df.sort_values(["Politicas","creacion"], ascending=[False, True])
    df = df.head(5)

    indice = np.arange(len(df))
    ancho = 0.4
    plt.bar(indice, df['Politicas'], width=ancho, color='b', label='cookies')
    plt.xticks(indice + ancho, df["url"])
    plt.xlabel('webs')
    plt.title('Top 5 webs desactualizadas')
    plt.show()

def comparar_webs_creacion(con, ano):
    df = pd.read_sql_query("SELECT * from legal WHERE creacion="+str(ano)+" ORDER BY url", con)
    df["Politicas"] = 3 - df["cookies"] - df["aviso"] - df["proteccion_de_datos"]
    print("-----------------------")
    print("Paginas del "+str(ano)+" que cumplen politicas")
    print("-----------------------")
    print(df[df["Politicas"] == 0])
    print("-----------------------")
    print("Paginas del "+str(ano)+" que NO cumplen politicas")
    print("-----------------------")
    print(df[df["Politicas"] != 0])
    

def comparar_passwords_comprometidas(con):
    df = pd.read_sql_query("SELECT * from usuarios", con)
    comprometidos = []
    no_comprometidos = []
    for index, row in df.iterrows():
        if(esPasswordSegura(row["contrasena"])):
            no_comprometidos.append(row)
        else:
            comprometidos.append(row)
    print("Passwords comprometidas: "+str(len(comprometidos)))
    print("Passwords no comprometidas: "+str(len(no_comprometidos)))
    
    
   

con = sqlite3.connect('example.db')
usuarios_vulnerables(con)
politicas_desactualizadas(con)
comparar_webs_creacion(con, 2001)
comparar_passwords_comprometidas(con)
con.close()
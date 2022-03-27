import sqlite3
import pandas as pd
from ast import literal_eval
import statistics
import numpy as np
import math


def sql_show_table(con, table):
   df = pd.read_sql_query("SELECT * from "+str(table), con)
   return df








def observaciones(df):
    sum = 0
    for index, row in df.iterrows():
        sum+=literal_eval(row["emails"])["phishing"]
    return sum


def valores_vacios_3(df):
    vacios = 0
    for index, row in df.iterrows():
        if literal_eval(row["emails"])["phishing"] is None or math.isnan(literal_eval(row["emails"])["phishing"]):
            vacios += 1
    return vacios

def mediana(df):
    lista = []
    for index, row in df.iterrows():
            if row["emails"] != "None":
                    lista.append(literal_eval(row["emails"])["phishing"])
            else:
                lista.append(0)
    return np.median(lista)
def media(df):
    sum = 0
    for index, row in df.iterrows():
            if row["emails"] != "None":
                    sum+=literal_eval(row["emails"])["phishing"]
    return sum/len(df)
def varianza(df):
    lista = []
    for index, row in df.iterrows():
            if row["emails"] != "None":
                    lista.append(literal_eval(row["emails"])["phishing"])
            else:
                lista.append(0)
    return np.var(lista)

def valorminmax_3(df):
    lista = []
    for index, row in df.iterrows():
            if row["emails"] != "None":
                    lista.append(literal_eval(row["emails"])["phishing"])
            else:
                lista.append(0)
    return str(np.amin(np.array(lista)))+"/"+str(np.amax(np.array(lista)))


def agrupacion_rol(con, permisos):
    df = pd.read_sql_query("SELECT * from usuarios WHERE permisos = "+str(permisos), con)
    estadisticas_ej3(df)

def agrupacion_correos(con, cantidad):
    df = pd.read_sql_query("SELECT * from usuarios", con)
    for index, row in df.iterrows():
        if(cantidad == 200):
            if(literal_eval(row["emails"])["total"] < 200):
                df = df.drop(index)
        elif(cantidad == -200):
            if(literal_eval(row["emails"])["total"] >= 200):
                df = df.drop(index)
    estadisticas_ej3(df)


def estadisticas_ej3(df):
    print("Numero de observaciones:", observaciones(df))
    print("Numero de valores ausentes:", valores_vacios_3(df))
    print("Mediana:", mediana(df))
    print("Media:", media(df))
    print("Varianza:", varianza(df))
    print("Valor minimo/maximo:", valorminmax_3(df))    

def print_ejercicio3(con):

    print("-----------------------")
    print("Agrupacion por Usuario")
    print("-----------------------")
    agrupacion_rol(con, 0)
    print("-----------------------")
    print("Agrupacion por Administrador")
    print("-----------------------")
    agrupacion_rol(con, 1)
    print("-----------------------")
    print("Agrupacion por +200 correos")
    print("-----------------------")

    agrupacion_correos(con, 200)
    print("-----------------------")
    print("Agrupacion por -200 correos")
    print("-----------------------")
    agrupacion_correos(con, -200)

    
   








con = sqlite3.connect('example.db')
print_ejercicio3(con)

con.close()
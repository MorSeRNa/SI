import sqlite3
import pandas as pd
from ast import literal_eval
import statistics
import numpy as np
import math


def sql_show_table(con, table):
   df = pd.read_sql_query("SELECT * from "+str(table), con)
   return df

def sql_delete(con):
    cursorObj = con.cursor()
    cursorObj.execute('DELETE FROM usuarios where dni = "X"')
    con.commit()

def sql_delete_table(con):
    cursorObj = con.cursor()
    cursorObj.execute('drop table if exists usuarios')
    con.commit()

def sql_create_table_legal(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS legal (url text, cookies boolean, aviso boolean, proteccion_de_datos boolean, creacion integer)")
    con.commit()

def sql_create_table_users(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS usuarios (id_usuario text, telefono text, contrasena text, provincia text, permisos boolean, emails text, fechas text, ips text)")
    con.commit()

def sql_insert_row_legal(con, url, cookies, aviso, proteccion_de_datos, creacion):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO legal VALUES ('"+url+"', "+str(cookies)+", "+str(aviso)+", "+str(proteccion_de_datos)+", "+str(creacion)+") ")
    con.commit()

def sql_insert_row_users(con, id_usuario, telefono, contrasena, provincia, permisos, emails, fechas, ips):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO usuarios VALUES ('"+id_usuario+"', '"+str(telefono)+"', '"+str(contrasena)+"' , '"+str(provincia)+"', "+str(permisos)+", \""+str(emails)+"\", \""+str(fechas)+"\", \""+str(ips)+"\") ")
    con.commit()

def sql_read_from_legal(con):
    df = pd.read_json('legal.json')
    for row in df.iterrows():
        s = row[1][0]
        for v in s:
            url = v
            cookies = s[v]["cookies"]
            aviso = s[v]["aviso"]
            proteccion_de_datos = s[v]["proteccion_de_datos"]
            creacion = s[v]["creacion"]
            sql_insert_row_legal(con, url, cookies, aviso, proteccion_de_datos, creacion)

def sql_read_from_users(con):
    df = pd.read_json('users.json')
    for row in df.iterrows():
        s = row[1][0]
        for v in s:
            id_usuario = v
            telefono = s[v]["telefono"]
            contrasena = s[v]["contrasena"]
            provincia = s[v]["provincia"]
            permisos = s[v]["permisos"]
            emails = s[v]["emails"]
            fechas = s[v]["fechas"]
            ips = s[v]["ips"]
            sql_insert_row_users(con, id_usuario, telefono, contrasena, provincia, permisos, emails, fechas, ips)

def calcular_media(df, column):
    sum = 0
    for index, row in df.iterrows():
            if row[column] != "None":
                if column != "emails":
                    sum += len(literal_eval(row[column]))
                else:
                    sum += literal_eval(row[column])["total"]
    return sum/df.shape[0]

def desviacion_estandar(df, column):
    lista = []
    for index, row in df.iterrows():
            if row[column] != "None":
                if column != "emails":
                    lista.append(len(literal_eval(row[column])))
                else:
                    lista.append(literal_eval(row[column])["total"])
            else:
                lista.append(0)
    return statistics.stdev(lista)
def valorminmax(df, column):
    lista = []
    for index, row in df.iterrows():
            if row[column] != "None":
                if column != "emails":
                    lista.append(len(literal_eval(row[column])))
                else:
                    lista.append(literal_eval(row[column])["total"])
            else:
                lista.append(0)
    return str(np.amin(np.array(lista)))+"/"+str(np.amax(np.array(lista)))

def valores_vacios(df):
    vacios = 0
    for index, row in df.iterrows():
        if row["telefono"] == "None":
            vacios += 1
        if row["provincia"] == "None":
            vacios += 1
        if row["ips"] == "None":
            vacios += 1
        if row["fechas"] == "None":
            vacios += 1
    return vacios

def print_ejercicio2(df):
    print("Total de muestras: " +str(len(df) * len(df.columns) - valores_vacios(df)))
    print("Media fechas : " +str(calcular_media(df, "fechas")))
    print("Desviacion estandar fechas: " +str(desviacion_estandar(df, "fechas")))
    print("Media ips : "  +str(calcular_media(df, "ips")))
    print("Desviacion estandar ips: " +str(desviacion_estandar(df, "ips")))

    print("Media emails recibidos : " +str(calcular_media(df, "emails")))
    print("Desviacion estandar emails recibidos: " +str(desviacion_estandar(df, "emails")))

    print("Valor minimo / maximo de fechas que han iniciado sesion : " +valorminmax(df, "fechas"))
    print("Valor minimo / maximo del numero de emails recibidos: " +valorminmax(df, "emails"))








con = sqlite3.connect('example.db')
#sql_create_table_legal(con)
#sql_create_table_users(con)

#sql_read_from_legal(con)
#sql_read_from_users(con)

df_legal = sql_show_table(con, "legal")
df_usuarios = sql_show_table(con, "usuarios")
print_ejercicio2(df_usuarios)

con.close()

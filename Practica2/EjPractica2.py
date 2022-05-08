import pandas as pd
import sqlite3
from flask import Flask, render_template, request, redirect
import altair as alt
import requests
import hashlib
from ast import literal_eval
import pdfkit

con = sqlite3.connect('example.db', check_same_thread=False)
cursorObj = con.cursor()
app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/users/")
def users():
    args = request.args
    df = get_df_user_critics_tops(int(args.get("amount", default=10)))
    chart = alt.Chart(df).mark_bar().encode(x="id_usuario", y="probabilidad")
    df2 = get_df_spam(int(args.get("limit", default=0)))
    return render_template('users.html', graphJSON=chart.to_json(), click=df2.to_html(), amount=int(args.get("amount", default=10)), limit=int(args.get("limit", default=0)))

@app.route("/pdf/")
def pdf_generate():
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    args = request.args
    print(args.get("users"))
    if(args.get("users") == "1"):
        df2 = get_df_spam(int(args.get("limit", default=0)))
        html = render_template('users_pdf.html', click=df2.to_html())
        pdfkit.from_string(html, 'static/pdf/out.pdf',configuration = config)
    else:
        response = requests.get("https://cve.circl.lu/api/last")
        if response.status_code == 200:
            json = response.text
            df = pd.DataFrame()
            df["id"] = pd.read_json(json)["id"]
            df["summary"] = pd.read_json(json)["summary"]
            html = render_template('vulnerabilities_pdf.html', vulns=df.head(10).to_html())
            pdfkit.from_string(html, 'static/pdf/out.pdf',configuration = config)
        else:
            raise Exception
    
    return redirect("../static/pdf/out.pdf")

@app.route("/pages/")
def vuln_webs():
    args = request.args
    df = get_df_vuln_webs_tops(int(args.get("amount", default=5)))
    chart = alt.Chart(df).mark_bar().encode(x="url", y="Politicas")
    return render_template('pages.html', graphJSON=chart.to_json(), amount=int(args.get("amount", default=5)))

@app.route("/vulnerabilities/")
def vulns():
    return render_template('vulnerabilities.html', vulns=get_cve_api())


def esPasswordSegura(password):
    with open("10k-most-common.txt", encoding='utf8') as f:
        for i in f.read().splitlines():
            linea = hashlib.md5(bytes(i, encoding='utf8'))
            if linea.hexdigest() == password:
                return 0
    return 1

def get_df_user_critics_tops(top: int):
    df = pd.read_sql_query("SELECT * from usuarios", con)
    for index, row in df.iterrows():
        if(literal_eval(row["emails"])["phishing"] != 0):
            df._set_value(index, "probabilidad", (literal_eval(row["emails"])["cliclados"]/literal_eval(row["emails"])["phishing"])*100)
        else:
            df._set_value(index, "probabilidad", 0)
        df._set_value(index, "secure_pass", esPasswordSegura(row["contrasena"]))
    
    df = df[df["secure_pass"] == 0]
    df = df.sort_values(["probabilidad"], ascending=[False])
    df = df.head(top)
    return df


def get_df_vuln_webs_tops(top: int):
    df = pd.read_sql_query("SELECT url, cookies, aviso, proteccion_de_datos FROM legal ORDER BY url", con)
    df["Politicas"] = df["cookies"] + df["aviso"] + df["proteccion_de_datos"]
    df = df.sort_values("Politicas").head(top)
    return df


def get_df_spam(limit: int):

    df = pd.read_sql_query("SELECT * from usuarios", con)
    if bool(limit):
        for index, row in df.iterrows():
            if(literal_eval(row["emails"])["phishing"] != 0):
                if(literal_eval(row["emails"])["cliclados"] > literal_eval(row["emails"])["phishing"]/2):
                    df._set_value(index, "spam_clicked", 1)
                    df._set_value(index, "spam_porcentaje", str(round(literal_eval(row["emails"])["cliclados"]/literal_eval(row["emails"])["phishing"], 2)*100)+"%")
                else:
                    df._set_value(index, "spam_clicked", 0)
            else:
                df._set_value(index, "spam_clicked", 0)       
    else:
        for index, row in df.iterrows():
            if(literal_eval(row["emails"])["phishing"] != 0):
                if(literal_eval(row["emails"])["cliclados"] <= literal_eval(row["emails"])["phishing"]/2):
                    df._set_value(index, "spam_clicked", 1)
                    df._set_value(index, "spam_porcentaje", str(round(literal_eval(row["emails"])["cliclados"]/literal_eval(row["emails"])["phishing"], 2)*100)+"%")
                else:
                    df._set_value(index, "spam_clicked", 0)
            else:
                df._set_value(index, "spam_clicked", 0)
    df = df[df["spam_clicked"] == 1]
    return df


def get_cve_api():
    response = requests.get("https://cve.circl.lu/api/last")
    if response.status_code == 200:
        json = response.text
        df = pd.DataFrame()
        df["id"] = pd.read_json(json)["id"]
        df["summary"] = pd.read_json(json)["summary"]
        return df.head(10).to_html()
    else:
        raise Exception


def df_emails_order_by_email_phising(top: int, admin: bool):
    df = pd.read_sql_query("SELECT id_usuario, emails FROM usuarios WHERE permisos == 1", con)
    if admin:
        for index, row in df.iterrows():
            if(literal_eval(row["emails"])["phishing"] != 0):
                df._set_value(index, "emails_phishing", literal_eval(row["emails"])["phishing"])      
            else:
                df._set_value(index, "emails_phishing", 0)      
        return df.sort_values("emails_phishing", ascending=False).head(top)
    else:
        for index, row in df.iterrows():
            if(literal_eval(row["emails"])["phishing"] != 0):
                df._set_value(index, "emails_phishing", literal_eval(row["emails"])["phishing"])      
            else:
                df._set_value(index, "emails_phishing", 0)   
        return df.sort_values("emails_phishing", ascending=False).head(top)


if __name__ == '__main__':
    app.run()
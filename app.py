import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs where source = 'local' ;"""
    cur.execute(sql_all)
    localAll = cur.fetchone()[0]
    # Get number of all succesful requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\' and source='local' ;"""
    cur.execute(sql_success)
    localSuccess = cur.fetchone()[0]


    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs where source = 'remote' ;"""
    cur.execute(sql_all)
    remoteAll = cur.fetchone()[0]
    # Get number of all succesful requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\' and source='remote' ;"""
    cur.execute(sql_success)
    remoteSuccess = cur.fetchone()[0]


    # Determine rate if there was at least one request
    localRate = "No entries yet!"
    if localAll != 0:
        localRate = str(localSuccess / localAll)
    remoteRate = "No entries yet!"
    if remoteAll != 0:
        remoteRate = str(remoteSuccess / remoteAll)

    return render_template('index.html', remoteRate = remoteRate, localRate=localRate)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

# learning flask for web development

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql.cursors
from flask_mysqldb import MySQL
from config import * #import all from config file


app = Flask(__name__)
mysql = MySQL(app)
# connection = pymysql.connect(host='127.0.0.1',
#                              user='root',
#                              password='',
#                              database='test',
#                              cursorclass=pymysql.cursors.DictCursor)
app.config['MYSQL_HOST'] = ENDPOINT
app.config['MYSQL_USER'] = USERNAME
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = DBNAME



@app.route('/')
def main_page():
    cur = mysql.connection.cursor()
    # sql = "INSERT INTO student(fname, lname, address) VALUES (%s, %s, %s)", ('Avinash', 'Kshirsagar', 'Pune')
    cur.execute("INSERT INTO student(fname, lname, address) VALUES (%s, %s, %s)", ('Avinash', 'Kshirsagar', 'Pune'))
    mysql.connection.commit()
    # connection.commit()
    return "record inserted successfully"

@app.route('/records')
def getRecords():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    # cur.execute(sql, ('webmaster@python.org',))
    result = cur.fetchall()
    return jsonify({"studentdata":result})


@app.route('/login')
def login_page():
    return render_template("index.html")
    
if __name__ == '__main__':
    app.run(debug = True)
# learning flask for web development

from flask import Flask, jsonify, render_template, request
import pymysql.cursors
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from config import * #import all from config file


app = Flask(__name__)
mysql = MySQL(app)
bcrypt = Bcrypt(app)
# connection = pymysql.connect(host='127.0.0.1',
#                              user='root',
#                              password='',
#                              database='test',
#                              cursorclass=pymysql.cursors.DictCursor)
app.config['MYSQL_HOST'] = ENDPOINT
app.config['MYSQL_USER'] = USERNAME
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = DBNAME



@app.route('/api/registerUser',methods = ['POST'])
def main_page():
    if request.method == 'POST':
        _json = request.json
        fname = _json['fname']
        lname = _json['lname']
        address = _json['address']
        password = _json['password']
        confirmpassword = _json['confirmpassword']
        _password_hashed = generate_password_hash(password)
        _confirm_password_hashed = generate_password_hash(confirmpassword)
        cur = mysql.connection.cursor()
        # sql = "INSERT INTO student(fname, lname, address) VALUES (%s, %s, %s)", ('Avinash', 'Kshirsagar', 'Pune')
        cur.execute("INSERT INTO student(fname, lname, address, password, confirmpassword) VALUES (%s, %s, %s, %s, %s)", (fname , lname, address, _password_hashed, _confirm_password_hashed))
        mysql.connection.commit()
        # connection.commit()
        return jsonify({"message" : "record inserted successfully"}),200
    elif request.method == 'GET': 
        return jsonify({"message" : "invalid method."}),405

@app.route('/signup')
def signUpPage():
    return render_template("signup.html")


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
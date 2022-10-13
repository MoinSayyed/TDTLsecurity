#My PHPmyAdmin String
import pymysql
USERNAME = 'root'  # Replace with your master username 
PASSWORD = ''  # Replace with your RDS instance password
ENDPOINT = "localhost"  # Replace with your RDS endpoint
PORT = 3306   # Replace with the RDS instance port
# REGION = "us-east-2a"  # Replace with your AWS region
DBNAME = 'test'  # Replace with the name of your SCHEMA in MySQL workbench
# SSL_CA = "mysql-ssl-ca-cert.pem"  # Replace with the folder location of your SSL bundle
CURSORCLASS = pymysql.cursors.DictCursor  # No need to modify this
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="mqtt_admin",
        password="masadmin_masadmin#1234",
        database="mysensor_db"
    )

# database.py
import mysql.connector

def conectar_banco():
    conn = mysql.connector.connect(
        host="localhost",  # ou o endereço do seu servidor MySQL
        user="root",  # seu nome de usuário MySQL
        password="1045",  # sua senha MySQL
        database="academia",  # nome do banco de dados que você criou
        port=3306
    )
    return conn
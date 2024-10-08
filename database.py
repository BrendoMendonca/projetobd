
import mysql.connector

def conectar_banco():
    conn = mysql.connector.connect(
        host="localhost",  #endereço do servidor MySQL
        user="root",  #nome de usuário MySQL
        password="1045",  #senha MySQL
        database="decademia",  # nome do banco de dados
        #port=3306
    )
    return conn
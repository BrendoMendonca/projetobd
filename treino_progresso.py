

from datetime import datetime
from database import conectar_banco

class Progresso:
    def __init__(self, data, peso, altura):#registra progresso do aluno
        self.data = self.validar_data(data)
        self.peso = peso
        self.altura = altura
        self.imc = self.calcular_imc()
    
    

    def salvar_no_banco(self, aluno_id):
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO progresso (aluno_id, data, peso, imc) 
                          VALUES (%s, %s, %s, %s)''',
                       (aluno_id, self.data, self.peso, self.imc))
        
        conn.commit()
        conn.close()
        
    def listar_progresso(aluno):#lista progresso de um aluno
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''SELECT data, peso, imc 
                          FROM progresso WHERE aluno_id = %s''', (aluno.id,))
        progresso = cursor.fetchall()

        conn.close()

        if progresso:
            print(f"Progresso do aluno {aluno.nome} - {aluno.matricula}:")
            for p in progresso:
                print(f"- Data: {p[0]}, Peso: {p[1]} kg, IMC: {p[2]}")
        else:
            print(f"Não há progresso registrado para o aluno {aluno.nome}.")       
        
    def validar_data(self, data): #valida data do progresso
        try:
            # converte a data para o formato YYYY-MM-DD
            data_formatada = datetime.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')
            return data_formatada
        except ValueError:
            raise ValueError("Data inválida! Certifique-se de que está no formato dd/mm/aaaa e que o dia do mês é válido.")

    def calcular_imc(self):#caqlcula o IMC do aluno
        return round(self.peso / (self.altura ** 2), 2)

    def __str__(self):
        return f"Data: {self.data}, Peso: {self.peso}kg, IMC: {self.imc}"


class Treino:
    def __init__(self, nome, grupo_muscular, dificuldade, qnt_exercicios, matricula):#insere um treino para o aluno
        self.nome = nome
        self.grupo_muscular = grupo_muscular
        self.dificuldade = dificuldade
        self.qnt_exercicios = qnt_exercicios
        self.matricula = matricula


    def listar_treinos(aluno):#lista treino do aluno
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute('''SELECT nome, grupo_muscular, dificuldade, qnt_exercicios
                      FROM treinos WHERE aluno_id = %s''', (aluno.id,))
        treinos = cursor.fetchall()

        conn.close()

        if treinos:
            print(f"Treinos do aluno {aluno.nome} - {aluno.matricula}:")
            for treino in treinos:
                print(f"- {treino[0]} ({treino[1]}, {treino[2]}, {treino[3]} exercícios)")
        else:
            print(f"Não há treinos registrados para o aluno {aluno.nome}.")

    def salvar_no_banco(self, aluno_id):
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO treinos (aluno_id, nome, grupo_muscular, dificuldade, qnt_exercicios) 
                          VALUES (%s, %s, %s, %s, %s)''',
                       (aluno_id, self.nome, self.grupo_muscular, self.dificuldade, self.qnt_exercicios))
        
        conn.commit()
        conn.close()

    def __str__(self):
        return (f"Treino: {self.nome}, Grupo Muscular: {self.grupo_muscular}, Dificuldade: {self.dificuldade}, "
                f"Exercícios: {self.qnt_exercicios}")
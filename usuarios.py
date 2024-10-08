
from database import conectar_banco

class Pessoa:
    def __init__(self, nome, telefone, sexo, id):
        self.nome = nome
        self.telefone = telefone
        self.sexo = sexo
        self.id = id

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Telefone: {self.telefone}, Sexo: {self.sexo}"

class Aluno(Pessoa):
    def __init__(self, nome, telefone, sexo, matricula, altura, idade, peso, id = None):
        super().__init__(nome, telefone, sexo, id)
        self.matricula = matricula
        self.altura = altura
        self.idade = idade
        self.peso = peso
        self.imc = self.calcular_imc()
        self.treinos = []  # Inicializa a lista de treinos
        self.progresso = []  # Inicializa a lista de progresso 
    
    def adicionar_progresso(self, progresso):
        self.progresso.append(progresso)
        self.peso = progresso.peso
        self.imc = self.calcular_imc()
        print(f"Progresso do dia {progresso.data} adicionado ao aluno {self.nome} - {self.matricula}.")

    def calcular_imc(self):
        return round(self.peso / (self.altura ** 2), 2)

    def salvar_no_banco(self):
        conn = conectar_banco()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute('''INSERT INTO alunos (nome, telefone, sexo, matricula, altura, idade, peso) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           (self.nome, self.telefone, self.sexo, self.matricula, self.altura, self.idade, self.peso))
            self.id = cursor.lastrowid  #atualiza o ID do objeto após inserção
        else:
            cursor.execute('''UPDATE alunos SET nome = %s, telefone = %s, sexo = %s, matricula = %s, altura = %s, idade = %s, peso = %s 
                              WHERE id = %s''',
                           (self.nome, self.telefone, self.sexo, self.matricula, self.altura, self.idade, self.peso, self.id))

        conn.commit()
        conn.close()

    def __str__(self):
        return (f"{super().__str__()}, Matrícula: {self.matricula}, Altura: {self.altura}m, "
                f"Idade: {self.idade}, Peso: {self.peso}kg, IMC: {self.imc}")

class Personal(Pessoa):
    def __init__(self, nome, telefone, sexo, cref):
        super().__init__(nome, telefone, sexo, None)
        self.cref = cref

    def salvar_no_banco(self):
        conn = conectar_banco()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute('''INSERT INTO personais (nome, telefone, sexo, cref) 
                              VALUES (%s, %s, %s, %s)''',
                           (self.nome, self.telefone, self.sexo, self.cref))
            self.id = cursor.lastrowid  #atualiza o ID do objeto após inserção
        else:
            cursor.execute('''UPDATE personais SET nome = %s, telefone = %s, sexo = %s, cref = %s 
                              WHERE id = %s''',
                           (self.nome, self.telefone, self.sexo, self.cref, self.id))

        conn.commit()
        conn.close()

    def __str__(self):
        return f"{super().__str__()}, CREF: {self.cref}"
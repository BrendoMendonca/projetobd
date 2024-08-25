
from usuarios import Aluno, Personal
from treino_progresso import Progresso, Treino
from database import conectar_banco

class SistemaCadastro:
    def __init__(self):
        self.pessoas = []
        self.proximo_id = 1
        self.total_cadastradas = 0
        self.progresso = Progresso()  # Instância da classe Progresso para gerenciar o progresso
        self.treino = Treino()  # Instância da classe Treino para gerenciar os treinos

    def inserir(self, pessoa):
        pessoa.id = self.proximo_id
        self.pessoas.append(pessoa)
        pessoa.salvar_no_banco()
        self.proximo_id += 1
        self.total_cadastradas += 1
        print(f"\nUsuário {pessoa.nome} inserido com sucesso!")

    def alterar(self, id):
        for pessoa in self.pessoas:
            if pessoa.id == id:
                pessoa.nome = input("Novo nome: ")
                pessoa.telefone = input("Novo telefone: ")
                pessoa.sexo = self.validar_sexo(input("Novo sexo (M/F): "))
                print(f"\nDados alterados com sucesso!")
                return
        print(f"\nUsuário com id {id} não encontrado.")

    def pesquisar(self, nome):
        usuario = False
        for pessoa in self.pessoas:
            if pessoa.nome == nome:
                if not usuario:
                    print("\nUsuário encontrado:")
                    usuario = True
                print(pessoa)
                usuario = True
        if not usuario:
            print(f"\nUsuário {nome} não encontrado.")

    def remover(self, id):
        for pessoa in self.pessoas:
            if pessoa.id == id:
                self.pessoas.remove(pessoa)
                self.total_cadastradas -= 1
                print(f"\nUsuário removido com sucesso!")
                return
        print(f"\nUsuário com ID {id} não encontrado.")

    def listar_todos(self):
        if not self.pessoas:
            print("\nNenhuma pessoa cadastrada.")
        else:
            print("\nLista de todas os usuários:")
            for pessoa in self.pessoas:
                print(pessoa)

    def exibir_um(self, id):
        for pessoa in self.pessoas:
            if pessoa.id == id:
                print("\nDados do usuário:")
                print(pessoa)
                return
        print(f"\nPessoa com id não encontrada.")

    def validar_sexo(self, sexo):
        while sexo.upper() not in ['M', 'F']:
            print("Erro: Sexo inválido. Digite 'M' para Masculino ou 'F' para Feminino.")
            sexo = input("Sexo (M/F): ")
        return sexo.upper()

    def relatorio_final(self):
        alunos = [p for p in self.pessoas if isinstance(p, Aluno)]
        personais = [p for p in self.pessoas if isinstance(p, Personal)]
        
        print(f"\nRelatório Final:")
        print(f"Total de pessoas cadastradas: {self.total_cadastradas}")
        
        print("\nAlunos Cadastrados:")
        if alunos:
            for aluno in alunos:
                print(f"ID: {aluno.id}, Nome: {aluno.nome}, Sexo: {aluno.sexo}, Telefone: {aluno.telefone}, Matrícula: {aluno.matricula}")
        else:
            print("Nenhum aluno cadastrado.")

        print("\nPersonais Cadastrados:")
        if personais:
            for personal in personais:
                print(f"ID: {personal.id}, Nome: {personal.nome}, Sexo: {personal.sexo}, Telefone: {personal.telefone}, CREF: {personal.cref}")
        else:
            print("Nenhum personal cadastrado.")

    def carregar_do_banco(self):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM alunos")
        for row in cursor.fetchall():
            aluno = Aluno(nome=row[1], telefone=row[2], sexo=row[3], matricula=row[4], altura=row[5], idade=row[6], peso=row[7], id=row[0])
            self.pessoas.append(aluno)

        conn.close()
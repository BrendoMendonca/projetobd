class Pessoa:
    def __init__(self, nome, telefone, sexo):
        self.nome = nome
        self.telefone = telefone
        self.sexo = sexo

    def __str__(self):
        return f"Nome: {self.nome}, Telefone: {self.telefone}, Sexo: {self.sexo}"


class Aluno(Pessoa):
    def __init__(self, nome, telefone, sexo, id_aluno, altura, idade, peso):
        super().__init__(nome, telefone, sexo)
        self.id_aluno = id_aluno
        self.altura = altura
        self.idade = idade
        self.peso = peso
        self.imc = self.calcular_imc()
        self.treinos = [] #lista que armazena os treinos do aluno
        self.progresso = [] #lista que armazena o progresso do aluno

    def calcular_imc(self):
        return round(self.peso / (self.altura ** 2), 2)
    
    def adicionar_treino(self, treino):
        self.treinos.append(treino)
        print(f"Treino {treino.nome} adicionado ao aluno {self.nome}.")
        
    def listar_treinos(self):
        print(f"Treinos do aluno {self.nome}:")
        for treino in self.treinos:
            print(f"- {treino.nome} ({treino.grupo_muscular}, {treino.dificuldade}, {treino.qnt_exercicios} exercícios)")
            
    def adicionar_progresso(self, progresso):
        self.progresso.append(progresso)
        print(f"Progresso do dia {progresso.data} adicionado ao aluno {self.nome}.")
    
    def listar_processo(self):
        print(f"Progresso do aluno {self.nome}:")
        for prog in self.progresso:
            print(f"- Data: {prog.data}, Peso: {prog.peso}kg")

    def __str__(self):
        return (f"{super().__str__()}, ID Aluno: {self.id_aluno}, Altura: {self.altura}m, "
                f"Idade: {self.idade}, Peso: {self.peso}kg, IMC: {self.imc}")
class Personal(Pessoa):
    def __init__(self, nome, telefone, sexo, cref):
        super().__init__(nome, telefone, sexo)
        self.cref = cref

    def __str__(self):
        return f"{super().__str__()}, CREF: {self.cref}"


class SistemaCadastro:
    def __init__(self):
        self.pessoas = []
        self.total_cadastradas = 0

    def inserir(self, pessoa):
        self.pessoas.append(pessoa)
        self.total_cadastradas += 1
        print(f"\nUsuário {pessoa.nome} inserido com sucesso!")

    def alterar(self, nome):
        for pessoa in self.pessoas:
            if pessoa.nome == nome:
                pessoa.nome = input("Novo nome: ")
                pessoa.telefone = input("Novo telefone: ")
                pessoa.sexo = self.validar_sexo(input("Novo sexo (M/F): "))
                print(f"\nDados da pessoa {nome} alterados com sucesso!")
                return
        print(f"\nPessoa com nome {nome} não encontrada.")

    def pesquisar(self, nome):
        for pessoa in self.pessoas:
            if pessoa.nome == nome:
                print("\nPessoa encontrada:")
                print(pessoa)
                return
        print(f"\nPessoa com nome {nome} não encontrada.")

    def remover(self, nome):
        for pessoa in self.pessoas:
            if pessoa.nome == nome:
                self.pessoas.remove(pessoa)
                self.total_cadastradas -= 1
                print(f"\nPessoa {nome} removida com sucesso!")
                return
        print(f"\nPessoa com nome {nome} não encontrada.")

    def listar_todos(self):
        if not self.pessoas:
            print("\nNenhuma pessoa cadastrada.")
        else:
            print("\nLista de todas as pessoas:")
            for pessoa in self.pessoas:
                print(pessoa)

    def exibir_um(self, nome):
        for pessoa in self.pessoas:
            if pessoa.nome == nome:
                print("\nDados da pessoa:")
                print(pessoa)
                return
        print(f"\nPessoa com nome {nome} não encontrada.")

    def validar_sexo(self, sexo):
        while sexo.upper() not in ['M', 'F']:
            print("Erro: Sexo inválido. Digite 'M' para Masculino ou 'F' para Feminino.")
            sexo = input("Sexo (M/F): ")
        return sexo.upper()

    def relatorio_final(self):
        print(f"\nRelatório Final:")
        print(f"Total de pessoas cadastradas: {self.total_cadastradas}")


def menu():
    sistema = SistemaCadastro()

    while True:
        print("\nMenu:")
        print("1. Inserir")
        print("2. Alterar")
        print("3. Pesquisar por nome")
        print("4. Remover")
        print("5. Listar todos")
        print("6. Exibir um")
        print("0. Sair")
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            sexo = sistema.validar_sexo(input("Sexo (M/F): "))

            tipo_pessoa = input("A pessoa é um aluno ou um personal? (Digite 'aluno' ou 'personal'): ").strip().lower()
            if tipo_pessoa == 'aluno':
                id_aluno = input("ID do Aluno: ")
                altura = float(input("Altura (em metros): "))
                idade = int(input("Idade: "))
                peso = float(input("Peso (em kg): "))
                pessoa = Aluno(nome, telefone, sexo, id_aluno, altura, idade, peso)
            elif tipo_pessoa == 'personal':
                cref = input("CREF: ")
                pessoa = Personal(nome, telefone, sexo, cref)
            else:
                print("Tipo inválido, operação cancelada.")
                continue

            sistema.inserir(pessoa)

        elif opcao == '2':
            nome = input("Digite o nome da pessoa a ser alterada: ")
            sistema.alterar(nome)

        elif opcao == '3':
            nome = input("Digite o nome da pessoa a ser pesquisada: ")
            sistema.pesquisar(nome)

        elif opcao == '4':
            nome = input("Digite o nome da pessoa a ser removida: ")
            sistema.remover(nome)

        elif opcao == '5':
            sistema.listar_todos()

        elif opcao == '6':
            nome = input("Digite o nome da pessoa a ser exibida: ")
            sistema.exibir_um(nome)

        elif opcao == '0':
            print("\nSaindo do sistema...")
            sistema.relatorio_final()
            break

        else:
            print("\nOpção inválida! Tente novamente.")


if __name__ == "__main__":
    menu()

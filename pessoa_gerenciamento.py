class Pessoa:
    def __init__(self, nome, telefone, sexo, id):
        self.nome = nome
        self.telefone = telefone
        self.sexo = sexo
        self.id = id

    def __str__(self):
         return f"ID: {self.id}, Nome: {self.nome}, Telefone: {self.telefone}, Sexo: {self.sexo}"


class Aluno(Pessoa):
    def __init__(self, nome, telefone, sexo, matricula, altura, idade, peso):
        super().__init__(nome, telefone, sexo, id)
        self.matricula = matricula
        self.altura = altura
        self.idade = idade
        self.peso = peso
        self.imc = self.calcular_imc()
        self.treinos = []  # Lista que armazena os treinos do aluno
        self.progresso = []  # Lista que armazena o progresso do aluno

    def calcular_imc(self):
        return round(self.peso / (self.altura ** 2), 2)
    
    def adicionar_treino(self, treino):
        self.treinos.append(treino)
        print(f"{treino.nome} adicionado ao aluno {self.nome} - {self.matricula}.")
        
    def listar_treinos(self):
        print(f"Treinos do aluno {self.nome}:")
        for treino in self.treinos:
            print(f"- {treino.nome} ({treino.grupo_muscular}, {treino.dificuldade}, {treino.qnt_exercicios} exercícios)")
            
    def adicionar_progresso(self, progresso):
        self.progresso.append(progresso)
        print(f"Progresso do dia {progresso.data} adicionado ao aluno {self.nome} - {self.matricula}.")
    
    def listar_progresso(self):
        print(f"Progresso do aluno {self.nome} - {self.matricula}:")
        for prog in self.progresso:
            print(f"- Data: {prog.data}, Peso: {prog.peso}kg")

    def __str__(self):
        return (f"{super().__str__()}, Matricula: {self.matricula}, Altura: {self.altura}m, "
                f"Idade: {self.idade}, Peso: {self.peso}kg, IMC: {self.imc}")


class Personal(Pessoa):
    def __init__(self, nome, telefone, sexo, cref):
        super().__init__(nome, telefone, sexo, id)
        self.cref = cref

    def __str__(self):
        return f"{super().__str__()}, CREF: {self.cref}"


class Treino:
    def __init__(self, nome, grupo_muscular, dificuldade, qnt_exercicios, matricula):
        self.nome = nome
        self.grupo_muscular = grupo_muscular
        self.dificuldade = dificuldade
        self.qnt_exercicios = qnt_exercicios
        self.matricula = matricula
        
    def __str__(self):
        return (f"Treino: {self.nome}, Grupo Muscular: {self.grupo_muscular}, "
                f"Dificuldade: {self.dificuldade}, Exercícios: {self.qnt_exercicios}, "
                f"Matricula: {self.matricula}")


class Progresso:
    def __init__(self, data, peso):
        self.data = data
        self.peso = peso
        
    def __str__(self):
        return f"Data: {self.data}, Peso: {self.peso}kg"


class SistemaCadastro:
    def __init__(self):
        self.pessoas = []
        self.proximo_id = 1
        self.total_cadastradas = 0

    def inserir(self, pessoa):
        pessoa.id = self.proximo_id
        self.pessoas.append(pessoa)
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

    def pesquisar(self, id):
        for pessoa in self.pessoas:
            if pessoa.id == id:
                print("\nUsuário encontrado:")
                print(pessoa)
                return
        print(f"\nUsuário com ID {id} não encontrado.")

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
        print("7. Adicionar treino a aluno")
        print("8. Listar treinos de aluno")
        print("9. Adicionar progresso a aluno")
        print("10. Listar progresso de aluno")
        print("0. Sair")
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            sexo = sistema.validar_sexo(input("Sexo (M/F): "))

            tipo_pessoa = input("A pessoa é um aluno ou um personal? (Digite 'aluno' ou 'personal'): ").strip().lower()
            if tipo_pessoa == 'aluno':
                matricula = input("Matricula do Aluno: ")
                altura = float(input("Altura (em metros): "))
                idade = int(input("Idade: "))
                peso = float(input("Peso (em kg): "))
                pessoa = Aluno(nome, telefone, sexo, matricula, altura, idade, peso)
            elif tipo_pessoa == 'personal':
                cref = input("CREF: ")
                pessoa = Personal(nome, telefone, sexo, cref)
            else:
                print("Tipo inválido, operação cancelada.")
                continue

            sistema.inserir(pessoa)

        elif opcao == '2':
            id = int(input("Digite o ID da pessoa a ser alterada: "))
            sistema.alterar(id)

        elif opcao == '3':
            id = int(input("Digite o ID da pessoa a ser alterada: "))
            sistema.pesquisar(id)

        elif opcao == '4':
            id = input("Digite o ID da pessoa a ser removida: ")
            sistema.remover(id)

        elif opcao == '5':
            sistema.listar_todos()

        elif opcao == '6':
            id = input("Digite o ID da pessoa a ser exibida: ")
            sistema.exibir_um(id)

        elif opcao == '7':
            matricula = input("Digite a matricula do aluno para adicionar um treino: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                nome_treino = input("Nome do treino: ")
                grupo_muscular = input("Grupo muscular: ")
                dificuldade = input("Dificuldade: ")
                qnt_exercicios = int(input("Quantidade de exercícios: "))
                treino = Treino(nome_treino, grupo_muscular, dificuldade, qnt_exercicios, aluno.matricula)
                aluno.adicionar_treino(treino)
            else:
                print(f"Aluno de matrícula {matricula} não encontrado. Operação cancelada")

        elif opcao == '8':
            matricula = input("Digite a matricula do aluno para listar os treinos: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                aluno.listar_treinos()
            else:
                print(f"Aluno de matrícula {matricula} não encontrado. Operação cancelada")

        elif opcao == '9':
            matricula = input("Digite a matrícula do aluno para adicionar um progresso: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                data = input("Data do progresso (dd/mm/aaaa): ")
                peso = float(input("Peso (em kg): "))
                progresso = Progresso(data, peso)
                aluno.adicionar_progresso(progresso)
            else:
                print(f"Aluno de matrícula {matricula} não encontrado. Operação cancelada")

        elif opcao == '10':
            matricula = input("Digite a matricula do aluno para listar o progresso: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                aluno.listar_progresso()
            else:
                print(f"Aluno de matrícula {matricula} não encontrado. Operação cancelada")

        elif opcao == '0':
            print("\nSaindo do sistema...")
            sistema.relatorio_final()
            break

        else:
            print("\nOpção inválida! Tente novamente.")


if __name__ == "__main__":
    menu()

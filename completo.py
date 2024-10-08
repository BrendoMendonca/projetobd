from datetime import datetime

class Pessoa:
    def __init__(self, nome, telefone, sexo, id):
        self.nome = nome
        self.telefone = telefone
        self.sexo = sexo
        self.id = id

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Telefone: {self.telefone}, Sexo: {self.sexo}"

class Progresso:
    def __init__(self):
        self.progresso_aluno = {}

    def adicionar_progresso(self, aluno, data, peso):
        if aluno not in self.progresso_aluno:
            self.progresso_aluno[aluno] = []

        progresso = {
            'data': self.validar_data(data),
            'peso': peso,
            'altura': aluno.altura,
            'imc': self.calcular_imc(peso, aluno.altura)
        }

        self.progresso_aluno[aluno].append(progresso)
        aluno.peso = peso
        aluno.imc = progresso['imc']

        print(f"Progresso do dia {progresso['data']} adicionado ao aluno {aluno.nome} - {aluno.matricula}.")

    def listar_progresso(self, aluno):
        if aluno in self.progresso_aluno:
            print(f"Progresso do aluno {aluno.nome} - {aluno.matricula}:")
            for prog in self.progresso_aluno[aluno]:
                print(f"- Data: {prog['data']}, Peso: {prog['peso']}kg, IMC: {prog['imc']}")
        else:
            print(f"Não há progresso registrado para o aluno {aluno.nome}.")

    def validar_data(self, data):
        try:
            data_formatada = datetime.strptime(data, '%d/%m/%Y')
            return data_formatada.strftime('%d/%m/%Y')
        except ValueError:
            raise ValueError("Data inválida! Certifique-se de que está no formato dd/mm/aaaa e que o dia do mês é válido.")

    def calcular_imc(self, peso, altura):
        return round(peso / (altura ** 2), 2)


class Aluno(Pessoa):
    def __init__(self, nome, telefone, sexo, matricula, altura, idade, peso):
        super().__init__(nome, telefone, sexo, None)
        self.matricula = matricula
        self.altura = altura
        self.idade = idade
        self.peso = peso
        self.imc = self.calcular_imc()

    def calcular_imc(self):
        return round(self.peso / (self.altura ** 2), 2)

    def listar_treinos(self):
        print(f"Treinos do aluno {self.nome}:")
        for treino in self.treinos:
            print(f"- {treino.nome} ({treino.grupo_muscular}, {treino.dificuldade}, {treino.qnt_exercicios} exercícios)")

    def __str__(self):
        return (f"{super().__str__()}, Matricula: {self.matricula}, Altura: {self.altura}m, "
                f"Idade: {self.idade}, Peso: {self.peso}kg, IMC: {self.imc}")
    
    
class Personal(Pessoa):
    def __init__(self, nome, telefone, sexo, cref):
        super().__init__(nome, telefone, sexo, None)  # Passa None para o id, será atribuído no método inserir
        self.cref = cref

    def __str__(self):
        return f"{super().__str__()}, CREF: {self.cref}"


class Treino:
    def __init__(self):
        self.treinos_aluno = {}

    def adicionar_treino(self, aluno, nome_treino, grupo_muscular, dificuldade, qnt_exercicios):
        if aluno not in self.treinos_aluno:
            self.treinos_aluno[aluno] = []

        treino = {
            'nome': nome_treino,
            'grupo_muscular': grupo_muscular,
            'dificuldade': dificuldade,
            'qnt_exercicios': qnt_exercicios,
        }

        self.treinos_aluno[aluno].append(treino)
        print(f"Treino {nome_treino} adicionado ao aluno {aluno.nome} - {aluno.matricula}.")

    def listar_treinos(self, aluno):
        if aluno in self.treinos_aluno:
            print(f"Treinos do aluno {aluno.nome} - {aluno.matricula}:")
            for treino in self.treinos_aluno[aluno]:
                print(f"- {treino['nome']} ({treino['grupo_muscular']}, {treino['dificuldade']}, {treino['qnt_exercicios']} exercícios)")
        else:
            print(f"Não há treinos registrados para o aluno {aluno.nome}.")


class SistemaCadastro:
    def __init__(self):
        self.pessoas = []
        self.proximo_id = 1
        self.total_cadastradas = 0
        self.progresso = Progresso()
        self.treino = Treino() 

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
            id = int(input("Digite o ID da pessoa a ser removida: "))
            sistema.remover(id)

        elif opcao == '5':
            sistema.listar_todos()

        elif opcao == '6':
            id = int(input("Digite o ID da pessoa a ser exibida: "))
            sistema.exibir_um(id)

        elif opcao == '7':
            matricula = input("Digite a matricula do aluno para adicionar um treino: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                nome_treino = input("Nome do treino: ")
                grupo_muscular = input("Grupo muscular: ")
                dificuldade = input("Dificuldade: ")
                qnt_exercicios = int(input("Quantidade de exercícios: "))
                sistema.treino.adicionar_treino(aluno, nome_treino, grupo_muscular, dificuldade, qnt_exercicios)
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")

        elif opcao == '8':
            matricula = input("Digite a matricula do aluno para listar os treinos: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                sistema.treino.listar_treinos(aluno)
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")

        elif opcao == '9':
            matricula = input("Digite a matrícula do aluno para adicionar progresso: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                data = input("Data (dd/mm/aaaa): ")
                peso = float(input("Peso (em kg): "))
                try:
                    sistema.progresso.adicionar_progresso(aluno, data, peso)
                except ValueError as e:
                    print(e)
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")

        elif opcao == '10':
            matricula = input("Digite a matricula do aluno para listar o progresso: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                sistema.progresso.listar_progresso(aluno)
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")

        elif opcao == '0':
            sistema.relatorio_final()
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()
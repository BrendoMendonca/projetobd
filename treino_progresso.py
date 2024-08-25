# treino_progresso.py

from datetime import datetime

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

class Treino:
    def __init__(self, nome, gurpo_muscular, dificuldade, qnt_exercicios, id_aluno):
        self.nome = nome
        self.grupo_muscular = gurpo_muscular
        self.dificuldade = dificuldade
        self.qnt_exercicios = qnt_exercicios
        self.id_aluino = id_aluno
        
    def __str__(self):
        return (f"Treino: {self.nome}, Grupo Muscular: {self.grupo_muscular}, "
                f"Dificuldade: {self.dificuldade}, Exercícios: {self.qnt_exercicios}, "
                f"ID do Aluno: {self.id_aluno}")
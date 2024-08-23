class Progresso:
    def __init__(self, data, peso):
        self.data = data
        self.peso = peso
        
    def __str__(self) -> str:
        return f"Data: {self.data}, Peso: {self.peso}kg"
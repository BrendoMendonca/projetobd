
from usuarios import Aluno, Personal
from treino_progresso import Progresso, Treino
from database import conectar_banco
from vendas import Produto

class SistemaCadastro:
    def __init__(self):
        self.pessoas = []
        self.proximo_id = 1
        self.total_cadastradas = 0
        self.carregar_do_banco()
        #self.treino = Treino()
        #self.progresso = Progresso(None, None, None)
        #self.progresso = Progresso()  # Instância da classe Progresso para gerenciar o progresso
        #self.treino = Treino()  # Instância da classe Treino para gerenciar os treinos

    def inserir(self, pessoa):#método para inserir usuário
        
        self.pessoas.append(pessoa)
        pessoa.salvar_no_banco()
        
        self.total_cadastradas += 1
        print(f"\nUsuário {pessoa.nome} inserido com sucesso!")

    def alterar(self):#altera dados de usuário
        tipo_pessoa = input("Você quer alterar um aluno ou um personal? (Digite 'aluno' ou 'personal'): ").strip().lower()
        
        if tipo_pessoa == 'aluno':
            matricula = input("Digite a matrícula do aluno a ser alterado: ")
            for pessoa in self.pessoas:
                if isinstance(pessoa, Aluno) and pessoa.matricula == matricula:
                    pessoa.nome = input("Novo nome: ")
                    pessoa.telefone = input("Novo telefone: ")
                    pessoa.sexo = self.validar_sexo(input("Novo sexo (M/F): "))
                    
                    #salva as alterações no banco de dados
                    pessoa.salvar_no_banco()
                    
                    print(f"\nDados do aluno {pessoa.nome} alterados com sucesso!")
                    return
            print(f"\nAluno com matrícula {matricula} não encontrado.")

        elif tipo_pessoa == 'personal':
            cref = input("Digite o CREF do personal a ser alterado: ")
            for pessoa in self.pessoas:
                if isinstance(pessoa, Personal) and pessoa.cref == cref:
                    pessoa.nome = input("Novo nome: ")
                    pessoa.telefone = input("Novo telefone: ")
                    pessoa.sexo = self.validar_sexo(input("Novo sexo (M/F): "))
                    
                    #salva as alterações no banco de dados
                    pessoa.salvar_no_banco()
                    
                    print(f"\nDados do personal {pessoa.nome} alterados com sucesso!")
                    return
            print(f"\nPersonal com CREF {cref} não encontrado.")

    def pesquisar(self, nome):#pesquisa um usuário pelo nome
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

    def remover(self):#remove um usuário
        tipo_pessoa = input("Você quer remover um aluno ou um personal? (Digite 'aluno' ou 'personal'): ").strip().lower()
        
        if tipo_pessoa == 'aluno':
            matricula = input("Digite a matrícula do aluno a ser removido: ")
            for pessoa in self.pessoas:
                if isinstance(pessoa, Aluno) and pessoa.matricula == matricula:
                    conn = conectar_banco()
                    cursor = conn.cursor()
                    
                    #remove o aluno do banco de dados
                    cursor.execute('DELETE FROM alunos WHERE matricula = %s', (pessoa.matricula,))
                    
                    conn.commit()
                    conn.close()
                    
                    self.pessoas.remove(pessoa)
                    self.total_cadastradas -= 1
                    print(f"\nAluno {pessoa.nome} removido com sucesso!")
                    return
            print(f"\nAluno com matrícula {matricula} não encontrado.")
        
        elif tipo_pessoa == 'personal':
            cref = input("Digite o CREF do personal a ser removido: ")
            for pessoa in self.pessoas:
                if isinstance(pessoa, Personal) and pessoa.cref == cref:
                    conn = conectar_banco()
                    cursor = conn.cursor()
                    
                    #rremove o personal do banco de dados
                    cursor.execute('DELETE FROM personais WHERE cref = %s', (pessoa.cref,))
                    
                    conn.commit()
                    conn.close()
                    
                    self.pessoas.remove(pessoa)
                    self.total_cadastradas -= 1
                    print(f"\nPersonal {pessoa.nome} removido com sucesso!")
                    return
            print(f"\nPersonal com CREF {cref} não encontrado.")

    def listar_todos(self):#lista todos os usuários
        if not self.pessoas:
            print("\nNenhuma pessoa cadastrada.")
        else:
            print("\nLista de todas os usuários:")
            for pessoa in self.pessoas:
                print(pessoa)

    def exibir_um(self, id):#exibe um usuário
        for pessoa in self.pessoas:
            if pessoa.id == id:
                print("\nDados do usuário:")
                print(pessoa)
                return
        print(f"\nPessoa com id não encontrada.")

    def validar_sexo(self, sexo):#validação do sexo do usuário
        while sexo.upper() not in ['M', 'F']:
            print("Erro: Sexo inválido. Digite 'M' para Masculino ou 'F' para Feminino.")
            sexo = input("Sexo (M/F): ")
        return sexo.upper()

    def relatorio_final(self):#exibe o relatório de pessoas cadastradas
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
            
    def relatorio_vendas():#exibe o relatório de vendas
        conn = conectar_banco()
        cursor = conn.cursor()

        # Consulta para buscar todas as vendas registradas
        query = '''
            SELECT c.id, a.nome AS aluno, p.nome AS personal, pr.nome AS produto, cp.quantidade, pr.preco, c.forma_pagamento, c.data_compra
            FROM compras c
            JOIN alunos a ON c.aluno_id = a.id
            JOIN personais p ON c.personal_id = p.id
            JOIN compras_produtos cp ON c.id = cp.compra_id
            JOIN produtos pr ON cp.produto_id = pr.id
            ORDER BY c.data_compra DESC;
        '''

        cursor.execute(query)
        vendas = cursor.fetchall()

        conn.close()

        if vendas:
            print("\nRelatório de Vendas:")
            for venda in vendas:
                id_venda, aluno, personal, produto, quantidade, preco, forma_pagamento, data = venda
                total = quantidade * preco
                print(f"ID Venda: {id_venda} | Aluno: {aluno} | Personal: {personal} | Produto: {produto} | Quantidade: {quantidade} | Total: R$ {total:.2f} | Forma de Pagamento: {forma_pagamento} | Data: {data}")
        else:
            print("\nNenhuma venda registrada.")

    def carregar_do_banco(self):#recebe os dados do bd
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM alunos")
        for row in cursor.fetchall():
            aluno = Aluno(nome=row[1], telefone=row[2], sexo=row[3], matricula=row[4], altura=row[5], idade=row[6], peso=row[7], id=row[0])
            self.pessoas.append(aluno)
        
        cursor.execute("SELECT * FROM personais")
        for row in cursor.fetchall():
            personal = Personal(nome=row[1], telefone=row[2], sexo=row[3], cref=row[4])
            personal.id = row[0]  # Definir o ID do personal
            self.pessoas.append(personal)

        conn.close()
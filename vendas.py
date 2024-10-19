from database import conectar_banco
from decimal import Decimal


class Produto:
    def __init__(self, nome, preco, categoria, cidade_fabricacao, estoque):
        self.nome = nome
        self.preco = preco
        self.categoria = categoria
        self.cidade_fabricacao = cidade_fabricacao
        self.estoque = estoque

    @staticmethod
    def buscar_produtos(nome=None, preco_min=None, preco_max=None, categoria=None, cidade_fabricacao=None):
        conn = conectar_banco()
        cursor = conn.cursor()

        query = "SELECT nome, preco, categoria, cidade_fabricacao, estoque FROM produtos WHERE 1=1"
        params = []

        if nome:
            query += " AND nome LIKE %s"
            params.append(f"%{nome}%")
        if preco_min:
            query += " AND preco >= %s"
            params.append(preco_min)
        if preco_max:
            query += " AND preco <= %s"
            params.append(preco_max)
        if categoria:
            query += " AND categoria = %s"
            params.append(categoria)
        if cidade_fabricacao:
            query += " AND cidade_fabricacao = %s"
            params.append(cidade_fabricacao)

        cursor.execute(query, params)
        produtos = cursor.fetchall()
        
        conn.close()

        if produtos:
            print("\nProdutos encontrados:")
            for produto in produtos:
                print(f"Nome: {produto[0]}, Preço: R$ {produto[1]}, Categoria: {produto[2]}, Cidade: {produto[3]}, Estoque: {produto[4]}")
        else:
            print("\nNenhum produto encontrado com os critérios informados.")
    
    def registrar_compra_multiplos_produtos(aluno_matricula, personal_cref):
        conn = conectar_banco()
        cursor = conn.cursor()

        # Verifica se o aluno existe
        cursor.execute("SELECT id, torcedor, assiste, sousa FROM alunos WHERE matricula = %s", (aluno_matricula,))
        aluno = cursor.fetchone()

        if not aluno:
            print(f"Aluno com matrícula {aluno_matricula} não encontrado.")
            conn.close()
            return
        
        
        # Verifica se o personal existe
        cursor.execute("SELECT id FROM personais WHERE cref = %s", (personal_cref,))
        personal = cursor.fetchone()

        if not personal:
            print(f"Personal com CREF {personal_cref} não encontrado.")
            conn.close()
            return
        
        # Verifica se o aluno tem direito ao desconto
        tem_desconto = aluno[1].lower() == 'flamengo' and aluno[2].lower() == 'one piece' and aluno[3]

        total_compra = 0
        produtos_comprados = []

        # Loop para adicionar vários produtos à compra
        while True:
            nome_produto = input("Nome do produto (ou digite 'sair' para finalizar): ")
            if nome_produto.lower() == 'sair':
                break

            quantidade = int(input("Quantidade a ser vendida: "))

            # Verifica se o produto existe e se há estoque suficiente
            cursor.execute("SELECT id, preco, estoque FROM produtos WHERE nome = %s", (nome_produto,))
            produto = cursor.fetchone()

            if not produto:
                print(f"Produto {nome_produto} não encontrado.")
            elif produto[2] < quantidade:
                print(f"Estoque insuficiente. Apenas {produto[2]} unidades disponíveis para o produto {nome_produto}.")
            else:
                # Calcula o valor total da compra
                valor_produto = produto[1] * quantidade
                if tem_desconto:
                    valor_produto *=Decimal('0.9')
                    print(f"\nDesconto de 10% aplicado")
                total_compra += valor_produto

                produtos_comprados.append((aluno[0], personal[0], produto[0], quantidade, valor_produto))
                print(f"\n{quantidade} unidade(s) do produto {nome_produto} foram adicionadas à compra, totalizando R$ {valor_produto:.2f}.\n")

        # Exibir valor total antes de finalizar a compra
        if produtos_comprados:
            print(f"\nO valor total da compra é: R$ {total_compra:.2f}")
            forma_pagamento = input("Informe a forma de pagamento (Cartão, Dinheiro, Pix): ")

            # Registrar cada produto no banco de dados com a forma de pagamento
            for compra in produtos_comprados:
                cursor.execute('''INSERT INTO compras (aluno_id, personal_id, produto_id, quantidade, data_compra, forma_pagamento) 
                                VALUES (%s, %s, %s, %s, NOW(), %s)''', 
                                (compra[0], compra[1], compra[2], compra[3], forma_pagamento))

                # Atualiza o estoque do produto
                cursor.execute("UPDATE produtos SET estoque = estoque - %s WHERE id = %s", (compra[3], compra[2]))

            conn.commit()
            conn.close()

            print("Compra registrada com sucesso!")
        else:
            print("Nenhum produto foi adicionado à compra.")

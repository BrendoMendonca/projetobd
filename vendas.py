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
    def buscar_produtos(nome=None, preco_min=None, preco_max=None, categoria=None, cidade_fabricacao=None, estoque_min=None, estoque_max=None):
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
        if estoque_min is not None:
            query += " AND estoque >= %s"
            params.append(estoque_min)
        if estoque_max is not None:
            query += " AND estoque <= %s"
            params.append(estoque_max)

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

        total_compra = 0
        produtos_comprados = []

        # Verifica se o aluno tem direito ao desconto
        tem_desconto = aluno[1].lower() == 'flamengo' and aluno[2].lower() == 'one piece' and aluno[3]

        # Coleta os produtos que o usuário deseja comprar
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
                # Calcula o valor do produto e aplica o desconto, se aplicável
                valor_produto = produto[1] * quantidade
                if tem_desconto:
                    valor_produto *= Decimal('0.9')  # Aplica o desconto de 10%.
                    print(f"\nDesconto de 10% aplicado")
                total_compra += valor_produto

                # Adiciona o produto à lista de produtos comprados
                produtos_comprados.append((produto[0], quantidade, valor_produto))
                print(f"\n{quantidade} unidades do produto {nome_produto} foram adicionadas à compra, totalizando R$ {valor_produto:.2f}.\n")

        # Verifica se há produtos para registrar na compra
        if produtos_comprados:
            print(f"\nO valor total da compra é: R$ {total_compra:.2f}")
            forma_pagamento = input("Informe a forma de pagamento (Cartão, Dinheiro, Pix): ")

            # Registrar uma única compra com a forma de pagamento
            cursor.execute('''INSERT INTO compras (aluno_id, personal_id, data_compra, forma_pagamento) 
                            VALUES (%s, %s, NOW(), %s)''', 
                        (aluno[0], personal[0], forma_pagamento))

            # Obtém o ID da compra que acabou de ser inserida
            compra_id = cursor.lastrowid

            # Agora insere cada produto com o mesmo ID de compra
            for produto in produtos_comprados:
                produto_id, quantidade, valor_produto = produto
                cursor.execute('''INSERT INTO compras_produtos (compra_id, produto_id, quantidade, valor_total) 
                                VALUES (%s, %s, %s, %s)''', 
                                (compra_id, produto_id, quantidade, valor_produto))


                # Atualiza o estoque do produto
                cursor.execute("UPDATE produtos SET estoque = estoque - %s WHERE id = %s", (quantidade, produto_id))

            conn.commit()
            conn.close()

            print("Compra registrada com sucesso!")
        else:
            print("Nenhum produto foi adicionado à compra.")


            
    @staticmethod
    @staticmethod
    def listar_compras(aluno):
        conn = conectar_banco()
        cursor = conn.cursor()

        # Consulta para buscar todas as compras do aluno
        query = '''
            SELECT c.id, c.data_compra, c.forma_pagamento, SUM(cp.valor_total)
            FROM compras c
            JOIN compras_produtos cp ON c.id = cp.compra_id
            WHERE c.aluno_id = %s
            GROUP BY c.id
            ORDER BY c.data_compra DESC;
        '''

        cursor.execute(query, (aluno.id,))
        compras = cursor.fetchall()

        if compras:
            print(f"\nCompras realizadas pelo aluno {aluno.nome} - {aluno.matricula}:")
            for compra in compras:
                id_compra, data, forma_pagamento, total = compra
                print(f"\nID Compra: {id_compra}, Data: {data}, Pagamento: {forma_pagamento}, Total: R$ {total:.2f}")
                
                # Agora buscar os produtos dessa compra
                cursor.execute('''
                    SELECT p.nome, cp.quantidade, cp.valor_total
                    FROM compras_produtos cp
                    JOIN produtos p ON cp.produto_id = p.id
                    WHERE cp.compra_id = %s
                ''', (id_compra,))
                produtos = cursor.fetchall()

                for produto in produtos:
                    nome_produto, quantidade, valor_total = produto
                    print(f"   - Produto: {nome_produto}, Quantidade: {quantidade}, Total: R$ {valor_total:.2f}")
        else:
            print(f"\nNenhuma compra encontrada para o aluno {aluno.nome}.")


from sistema_cadastro import SistemaCadastro
from usuarios import Aluno, Personal
from treino_progresso import Progresso, Treino
from vendas import Produto


def menu():
    sistema = SistemaCadastro()

    while True:
        print("\nMenu:")
        print("1. Inserir")
        print("2. Alterar")
        print("3. Pesquisar pelo nome")
        print("4. Remover")
        print("5. Listar todos")
        print("6. Exibir um")
        print("7. Adicionar treino a aluno")
        print("8. Listar treinos de aluno")
        print("9. Adicionar progresso a aluno")
        print("10. Listar progresso de aluno")
        print("11. Buscar produto")
        print("12. Fazer uma venda")
        print("13. Verificar compras realizadas")
        print("0. Sair")
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            sexo = sistema.validar_sexo(input("Sexo (M/F): "))

            tipo_pessoa = input("A pessoa é um aluno ou um personal? (Digite 'aluno' ou 'personal'): ").strip().lower()
            if tipo_pessoa == 'aluno':
                matricula = input("Matrícula do Aluno: ")
                altura = float(input("Altura (em metros): "))
                idade = int(input("Idade: "))
                peso = float(input("Peso (em kg): "))
                
                torcedor = input("Time de Futebol: ")
                assiste = input("Série favorita: ")
                sousa = input("É de Sousa? (S/N): ").strip().upper() == 'S'
    
                pessoa = Aluno(nome, telefone, sexo, matricula, altura, idade, peso, torcedor, assiste, sousa)
            elif tipo_pessoa == 'personal':
                cref = input("CREF: ")
                pessoa = Personal(nome, telefone, sexo, cref)
            else:
                print("Tipo inválido, operação cancelada.")
                continue

            sistema.inserir(pessoa)

        elif opcao == '2':
            #id = int(input("Digite o ID da pessoa a ser alterada: "))
            sistema.alterar()

        elif opcao == '3':
            nome = input("Digite o nome da pessoa a ser pesquisada: ")
            sistema.pesquisar(nome)

        elif opcao == '4':
            #id = int(input("Digite o ID da pessoa a ser removida: "))
            sistema.remover()

        elif opcao == '5':
            sistema.listar_todos()

        elif opcao == '6':
            id = int(input("Digite o ID da pessoa a ser exibida: "))
            sistema.exibir_um(id)

        elif opcao == '7':  #adiciona treino a aluno
            matricula = input("Digite a matrícula do aluno para adicionar um treino: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                nome_treino = input("Nome do treino: ")
                grupo_muscular = input("Grupo muscular: ")
                dificuldade = input("Dificuldade: ")
                qnt_exercicios = int(input("Quantidade de exercícios: "))
               
                #cria uma instância de Treino passando os argumentos necessários
                treino = Treino(nome_treino, grupo_muscular, dificuldade, qnt_exercicios, matricula)
                
                treino.salvar_no_banco(aluno.id)  # Salva o treino no banco de dados
                aluno.treinos.append(treino)
                
                print("Treino adicionado com sucesso.")
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")

        elif opcao == '8':  #lista treinos de aluno
            matricula = input("Digite a matrícula do aluno para listar os treinos: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                Treino.listar_treinos(aluno)
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")

        elif opcao == '9':
            matricula = input("Digite a matrícula do aluno para adicionar progresso: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                data = input("Data (dd/mm/aaaa): ")
                peso = float(input("Peso (em kg): "))
                try:
                    progresso = Progresso(data, peso, aluno.altura)
                    
                    progresso.salvar_no_banco(aluno.id)  #salva o progresso no banco de dados
                    aluno.adicionar_progresso(progresso)
                    
                    print(f"Progresso adicionado com sucesso.")
                except ValueError as e:
                    print(e)
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")

        elif opcao == '10':  #listar progresso de aluno
            matricula = input("Digite a matrícula do aluno para listar o progresso: ")
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                Progresso.listar_progresso(aluno) 
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")
        
        elif opcao == '11':
            nome = input("Nome do produto (opcional): ").upper()
            preco_min = input("Preço mínimo (opcional): ").upper()
            preco_max = input("Preço máximo (opcional): ").upper()
            categoria = input("Categoria (garrafa/camisa) (opcional): ").upper()
            cidade = input("Cidade de fabricação (opcional): ").upper()
            estoque_min = input("Quantidade mínima em estoque (opcional): ").upper()
            estoque_max = input("Quantidade máxima em estoque (opcional): ").upper()
            
            preco_min = float(preco_min) if preco_min else None
            preco_max = float(preco_max) if preco_max else None
            estoque_min = int(estoque_min) if estoque_min else None
            estoque_max = int(estoque_max) if estoque_max else None
        
            Produto.buscar_produtos(nome=nome, preco_min=preco_min, preco_max=preco_max, categoria=categoria, cidade_fabricacao=cidade, estoque_min=estoque_min, estoque_max=estoque_max)

        elif opcao == '12':
            aluno_matricula = input("Matrícula do aluno (comprador): ")
            personal_cref = input("CREF do personal (vendedor): ")
            Produto.registrar_compra_multiplos_produtos(aluno_matricula, personal_cref)
        
        elif opcao == '13':  # Verificar compras realizadas pelo aluno
            matricula = input("Digite a matrícula do aluno para verificar as compras: ")
            
            aluno = next((p for p in sistema.pessoas if isinstance(p, Aluno) and p.matricula == matricula), None)
            if aluno:
                Produto.listar_compras(aluno)
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")
            
        elif opcao == '0':
            sistema.relatorio_final()
            SistemaCadastro.relatorio_vendas()
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()

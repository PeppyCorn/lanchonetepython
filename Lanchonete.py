import json

dados = dict()

def linha(titulo=''):
    print('=' * 30)
    if titulo:
        print(f'{titulo:^30}')
        print('=' * 30)


def listar_clientes():
    if not dados:
        print('Nenhum cliente cadastrado.')
        return
    
    print('--- Lista de Clientes ---')
    for nome, info in dados.items():
        print(f'Nome: {nome} - Telefone: {info["telefone"]}')

    print()


def fazer_pedido():
    if not dados:
        print('Nenhum cliente cadastrado.')
        return
    
    print('Clientes Cadastrados:')
    for i, nome in enumerate(dados.keys(), start=1):
        print(f'[{i}] - {nome}')
        
    while True:
        try:
            cliente_numero = int(input('Escolha o número do cliente: '))
            if cliente_numero < 1 or cliente_numero > len(dados):
                print('Número inválido.')
                continue
            
            nome_cliente = list(dados.keys())[cliente_numero - 1]
  
            quantidade_pedido = int(input('Quantos itens deseja pedir: '))
            if quantidade_pedido <= 0:
                print('Quantidade inválida.')
                continue
            
            total_pedido = 0
            for i in range(quantidade_pedido):
                while True:
                    item_pedido = input(f'Digite o nome do item {i+1}: ').strip().title()
                    if not item_pedido:
                        print('Nome do item inválido.')
                        continue
                    valor_item = float(input(f'Digite o valor do item {item_pedido}: '))
                    try:
                        if valor_item <= 0:
                            print('Valor inválido.')
                            continue
                        total_pedido += valor_item
                        break
                    except ValueError:
                        print('Valor inválido. Digite apenas números.')
                dados[nome_cliente]['pedidos'].append({
                    'item': item_pedido,
                    'valor': valor_item
                })

            
            print(f'Total do pedido: R$ {total_pedido:.2f}')
            desconto_total(total_pedido)
            
            break
        except ValueError:
            print('Entrada inválida. Digite apenas números.')
    salvar_arquivo()
        

def desconto_total(total):
    if total > 100:
        total -= total * 0.05
        print(f'Total com desconto: R$ {total:.2f}')
    return total 

def opcoes():
    while True:
        linha('=== Lanchonete do Pedro ===')
        print('''
            [1] - Cadastrar Cliente
            [2] - Listar Clientes
            [3] - Fazer Pedido
            [4] - Sair
            ''')
        opcao_escolhida = int(input('Escolha sua opção: '))

        if opcao_escolhida == 1:
            cadastrar_cliente()
        elif opcao_escolhida == 2:
            listar_clientes()
        elif opcao_escolhida == 3:
            fazer_pedido()
        elif opcao_escolhida == 4:
            break
        else:
            print('Opção inválida.')


def cadastrar_cliente():
    nome_cliente = input('Digite o nome do cliente: ').strip().title()
    if not nome_cliente:
        print('Nome inválido.')
        return
    if nome_cliente in dados:
        print('Cliente já cadastrado.')
        return
    while True:
        telefone_cliente = input('Digite o telefone: ')
        if telefone_cliente.isnumeric():
            break
        else:
            print('Telefone inválido. Digite apenas números.')
    for info in dados.values():
        if info["telefone"] == telefone_cliente:
            print('Telefone já cadastrado.')
            return
    dados[nome_cliente] = {
        'telefone': telefone_cliente,
        'pedidos': []
    }

    print(f'Cliente {nome_cliente} cadastrado com sucesso!\n')
    salvar_arquivo() 


def salvar_arquivo():
    try:
        with open('Lanchonete/pedidos.txt', 'w', encoding='utf-8') as pedidos:
            json.dump(dados, pedidos, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Erro ao salvar o arquivo: {e}')


def carregar_arquivo():
    global dados
    try:
        with open('Lanchonete/pedidos.txt', 'r', encoding='utf-8') as pedidos:
            dados = json.load(pedidos)
    except FileNotFoundError:
        print('Arquivo não encontrado. Será criado ao salvar.')
        dados = {}
    except Exception as e:
        print(f'Erro ao carregar o arquivo: {e}')
        
carregar_arquivo()

opcoes()

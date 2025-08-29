from collections import deque
import os

class Produto:
    def __init__(self, id, nome, quantidade, preco):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = float(preco)

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.nome} | Qtd: {self.quantidade} | Preço: R${self.preco:.2f}"

class Cliente:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.nome}"

class SistemaEstoque:
    def __init__(self):
        self.produtos = []
        self.clientes = []
        self.vendas = deque()
        self.operacoes = []

        self.next_produto_id = 1
        self.next_cliente_id = 1
        
        self.carregar_dados()

    def cadastrar_cliente(self):
        print("\n--- Cadastro de Cliente ---")
        nome = input("Digite o nome do cliente: ")
        if not nome:
            print("ERRO: Nome não pode ser vazio.")
            return

        cliente = Cliente(self.next_cliente_id, nome)
        self.clientes.append(cliente)
        self.operacoes.append(('add_cliente', self.next_cliente_id))
        self.next_cliente_id += 1
        print(f"Cliente '{nome}' cadastrado com sucesso! (ID: {cliente.id})")

    def listar_clientes(self):
        print("\n--- Clientes Cadastrados ---")
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in self.clientes:
                print(cliente)
        print("-" * 28)

    def cadastrar_produto(self):
        print("\n--- Cadastro de Produto ---")
        try:
            nome = input("Digite o nome do produto: ")
            if not nome:
                print("ERRO: Nome não pode ser vazio.")
                return
            quantidade = int(input("Digite a quantidade: "))
            preco = float(input("Digite o preço: "))

            if quantidade < 0 or preco < 0:
                print("ERRO: Quantidade e preço não podem ser negativos.")
                return

            produto = Produto(self.next_produto_id, nome, quantidade, preco)
            self.produtos.append(produto)
            self.operacoes.append(('add_produto', self.next_produto_id))
            self.next_produto_id += 1
            print(f"Produto '{nome}' cadastrado com sucesso! (ID: {produto.id})")

        except ValueError:
            print("ERRO: Quantidade ou preço inválido. Use apenas números.")

    def listar_produtos(self):
        print("\n--- Estoque Atual ---")
        if not self.produtos:
            print("Estoque vazio.")
        else:
            for produto in self.produtos:
                print(produto)
        print("-" * 21)

    def realizar_venda(self):
        print("\n--- Realizar Venda ---")
        if not self.produtos or not self.clientes:
            print("ERRO: É necessário ter ao menos um produto e um cliente cadastrado para realizar uma venda.")
            return
            
        try:
            self.listar_clientes()
            id_cliente = int(input("Digite o ID do cliente: "))
            cliente = self._buscar_por_id(self.clientes, id_cliente)
            if not cliente:
                print("ERRO: Cliente não encontrado.")
                return

            self.listar_produtos()
            id_produto = int(input("Digite o ID do produto: "))
            produto = self._buscar_por_id(self.produtos, id_produto)
            if not produto:
                print("ERRO: Produto não encontrado.")
                return

            qtd_venda = int(input("Digite a quantidade a ser vendida: "))
            if qtd_venda <= 0:
                print("ERRO: A quantidade deve ser positiva.")
                return
            if produto.quantidade < qtd_venda:
                print(f"ERRO: Estoque insuficiente. Disponível: {produto.quantidade}")
                return

            produto.quantidade -= qtd_venda
            valor_total = produto.preco * qtd_venda
            
            venda = {
                'cliente': cliente,
                'produto': produto,
                'quantidade': qtd_venda,
                'valor_total': valor_total
            }
            self.vendas.append(venda)
            self.operacoes.append(('venda', id_produto, qtd_venda))

            print(f"Venda realizada com sucesso para {cliente.nome}!")
            print(f"Valor total: R${valor_total:.2f}")

        except ValueError:
            print("ERRO: ID ou quantidade inválida. Use apenas números.")

    def visualizar_fila_vendas(self):
        print("\n--- Fila de Vendas Realizadas ---")
        if not self.vendas:
            print("Nenhuma venda registrada.")
        else:
            for venda in self.vendas:
                p, c, q, v = venda['produto'], venda['cliente'], venda['quantidade'], venda['valor_total']
                print(f"Cliente: {c.nome} | Produto: {p.nome} | Qtd: {q} | Valor Total: R${v:.2f}")
        print("-" * 32)
        
    def desfazer_ultima_operacao(self):
        print("\n--- Desfazer Última Operação ---")
        if not self.operacoes:
            print("Nenhuma operação para desfazer.")
            return

        ultima_op = self.operacoes.pop()
        tipo_op = ultima_op[0]

        if tipo_op == 'add_produto':
            id_produto = ultima_op[1]
            self.produtos = [p for p in self.produtos if p.id != id_produto]
            print(f"Operação desfeita: Cadastro do produto ID {id_produto} removido.")
        
        elif tipo_op == 'add_cliente':
            id_cliente = ultima_op[1]
            self.clientes = [c for c in self.clientes if c.id != id_cliente]
            print(f"Operação desfeita: Cadastro do cliente ID {id_cliente} removido.")

        elif tipo_op == 'venda':
            id_produto, qtd_devolvida = ultima_op[1], ultima_op[2]
            produto = self._buscar_por_id(self.produtos, id_produto)
            if produto:
                produto.quantidade += qtd_devolvida
                venda_removida = self.vendas.pop()
                print(f"Operação desfeita: Venda de {qtd_devolvida} unidade(s) do produto '{produto.nome}' cancelada.")
            else:
                self.operacoes.append(ultima_op)
                print("ERRO: Não foi possível desfazer a venda pois o produto original não existe mais.")

    def exibir_valor_total_estoque(self):
        total = sum(p.quantidade * p.preco for p in self.produtos)
        print(f"\nValor total do estoque: R${total:.2f}")

    def exibir_valor_total_vendas(self):
        total = sum(v['valor_total'] for v in self.vendas)
        print(f"\nValor total de vendas realizadas: R${total:.2f}")
    
    def exibir_gastos_clientes(self):
        print("\n--- Gastos Totais por Cliente ---")
        if not self.vendas:
            print("Nenhuma venda registrada para exibir gastos.")
            return

        gastos = {}
        for cliente in self.clientes:
            gastos[cliente.nome] = 0

        for venda in self.vendas:
            gastos[venda['cliente'].nome] += venda['valor_total']
        
        for nome, total in gastos.items():
            print(f"Cliente: {nome} | Total Gasto: R${total:.2f}")
        print("-" * 33)

    def pesquisar_produtos(self):
        print("\n--- Pesquisar Produtos ---")
        termo = input("Digite o nome ou ID do produto para pesquisar: ")
        resultados = []
        for p in self.produtos:
            if termo.isdigit() and p.id == int(termo):
                resultados.append(p)
            elif termo.lower() in p.nome.lower():
                resultados.append(p)
        
        if not resultados:
            print("Nenhum produto encontrado com o termo informado.")
        else:
            print("\n--- Resultados da Pesquisa ---")
            for r in resultados:
                print(r)
            print("-" * 28)

    def _buscar_por_id(self, lista, id):
        for item in lista:
            if item.id == id:
                return item
        return None

    def salvar_dados(self):
        try:
            with open("produtos.txt", "w") as f:
                for p in self.produtos:
                    f.write(f"{p.id},{p.nome},{p.quantidade},{p.preco}\n")
            
            with open("clientes.txt", "w") as f:
                for c in self.clientes:
                    f.write(f"{c.id},{c.nome}\n")
            print("Dados salvos com sucesso!")
        except IOError as e:
            print(f"ERRO ao salvar dados: {e}")

    def carregar_dados(self):
        try:
            if os.path.exists("produtos.txt"):
                with open("produtos.txt", "r") as f:
                    for linha in f:
                        id, nome, qtd, preco = linha.strip().split(',')
                        self.produtos.append(Produto(int(id), nome, int(qtd), float(preco)))
                    if self.produtos:
                        self.next_produto_id = max(p.id for p in self.produtos) + 1

            if os.path.exists("clientes.txt"):
                with open("clientes.txt", "r") as f:
                    for linha in f:
                        id, nome = linha.strip().split(',')
                        self.clientes.append(Cliente(int(id), nome))
                    if self.clientes:
                        self.next_cliente_id = max(c.id for c in self.clientes) + 1
            
            print("Dados carregados do sistema anterior.")
        except (IOError, ValueError) as e:
            print(f"ERRO ao carregar dados: {e}. Começando com sistema limpo.")

    def exibir_menu(self):
        print("\n===== MENU ESTOQUE E VENDAS =====")
        print("1. Cadastrar Cliente")
        print("2. Listar Clientes")
        print("3. Cadastrar Produto")
        print("4. Listar Produtos do Estoque")
        print("5. Realizar Venda")
        print("6. Visualizar Fila de Vendas")
        print("7. Desfazer Última Operação")
        print("8. Exibir Valor Total do Estoque")
        print("9. Exibir Valor Total de Vendas")
        print("10. Exibir Gastos por Cliente")
        print("--- Extras ---")
        print("11. Pesquisar Produto")
        print("12. Salvar Dados")
        print("0. Sair")
        print("=" * 33)

    def executar(self):
        while True:
            self.exibir_menu()
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.cadastrar_cliente()
            elif escolha == '2':
                self.listar_clientes()
            elif escolha == '3':
                self.cadastrar_produto()
            elif escolha == '4':
                self.listar_produtos()
            elif escolha == '5':
                self.realizar_venda()
            elif escolha == '6':
                self.visualizar_fila_vendas()
            elif escolha == '7':
                self.desfazer_ultima_operacao()
            elif escolha == '8':
                self.exibir_valor_total_estoque()
            elif escolha == '9':
                self.exibir_valor_total_vendas()
            elif escolha == '10':
                self.exibir_gastos_clientes()
            elif escolha == '11':
                self.pesquisar_produtos()
            elif escolha == '12':
                self.salvar_dados()
            elif escolha == '0':
                self.salvar_dados()
                print("Saindo do sistema... Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.")
            
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    sistema = SistemaEstoque()
    sistema.executar()
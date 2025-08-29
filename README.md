# Trabalho Avaliativo Estrutura de Dados

Este projeto foi desenvolvido como parte da avaliação da disciplina de Estrutura de Dados. O objetivo é aplicar os conceitos de Programação Orientada a Objetos (POO) e as estruturas de dados clássicas (Lista, Fila e Pilha) para criar um sistema de gerenciamento de estoque e vendas executado no terminal.

## Informações da Disciplina

* **Disciplina:** Estrutura de Dados
* **Professor:** Augusto Ortolan
* **Peso da Avaliação:** 2.0 pontos

## Integrantes do Grupo

* Pedro Luis Alves Bartz - 1135935
* Rafael Scortegagna Pedra - 1136090

## Estruturas de Dados Utilizadas

* **Lista (Python `list`):** Utilizada para armazenar o cadastro de produtos no estoque e o cadastro de clientes.
* **Fila (Python `collections.deque`):** Utilizada para gerenciar o histórico de vendas, garantindo a ordem de chegada (FIFO - First-In, First-Out).
* **Pilha (Python `list`):** Utilizada para permitir ao usuário desfazer a última operação realizada (cadastro ou venda), seguindo a ordem LIFO (Last-In, First-Out).

## Funcionalidades Implementadas

O sistema possui as seguintes funcionalidades:

### Funcionalidades Mínimas
1.  **Cadastrar Cliente:** Adiciona um novo cliente ao sistema.
2.  **Listar Clientes:** Exibe todos os clientes cadastrados.
3.  **Cadastrar Produto:** Adiciona um novo produto ao estoque.
4.  **Listar Produtos:** Exibe todos os produtos disponíveis no estoque.
5.  **Realizar Venda:** Registra uma venda, atualizando o estoque.
6.  **Visualizar Fila de Vendas:** Mostra o histórico de vendas na ordem em que ocorreram.
7.  **Desfazer Última Operação:** Reverte a última ação de cadastro ou venda.
8.  **Exibir Valor Total do Estoque:** Calcula e exibe o valor monetário total dos produtos em estoque.
9.  **Exibir Valor Total de Vendas:** Mostra o valor total acumulado com as vendas.
10. **Exibir Clientes e Valores Gastos:** Lista cada cliente e o total que já gastou.
11. **Sair:** Encerra a execução do programa.

### Funcionalidades Extras (Bônus)
* **Pesquisar Produtos:** Permite buscar produtos por nome ou por ID.
* **Salvar e Carregar Dados:** O sistema salva automaticamente o estado do estoque e dos clientes em arquivos (`produtos.txt`, `clientes.txt`) ao sair e os carrega ao iniciar, garantindo a persistência dos dados entre as execuções.

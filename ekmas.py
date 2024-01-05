import json

class SistemaUsuarios:
    def __init__(self):
        self.usuarios = {}
        self.carregar_usuarios()

    def carregar_usuarios(self):
        try:
            with open('usuarios_db.json', 'r') as file:
                self.usuarios = json.load(file)
        except FileNotFoundError:
            self.usuarios = {}

    def salvar_usuarios(self):
        with open('usuarios_db.json', 'w') as file:
            json.dump(self.usuarios, file)

    def cadastrar_usuario(self, username=None, senha=None):
        if not username:
            username = input("Digite o nome de usuário: ")
        if not senha:
            senha = input("Digite a senha: ")

        if username not in self.usuarios:
            self.usuarios[username] = senha
            print("Cadastro realizado com sucesso! Agora faça o login.")
            self.salvar_usuarios()
        else:
            print("Usuário já cadastrado. Por favor, escolha outro nome de usuário.")

    def realizar_login(self, username=None, senha=None):
        if not username:
            username = input("Digite o nome de usuário: ")
        if not senha:
            senha = input("Digite a senha: ")

        if username in self.usuarios and self.usuarios[username] == senha:
            print("Login bem-sucedido!")
            return True
        else:
            print("Usuário ou senha incorretos. Tente novamente.")
            return False

class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f}"



class EKMAS:

    def __init__(self):
        self.produtos = [
            Produto("Shampoo Nutritivo", 49.99),
            Produto("Shampoo Hidratante", 39.99),
            Produto("Condicionador Nutritivo", 35.99),
            Produto("Condicionador Hidratante", 45.99),
            Produto("Leave-in", 29.99),
            Produto("Spray Fixador", 32.99),
            Produto("Máscara Nutritiva", 69.99),
            Produto("Máscara Hidratante", 59.99)
        ]
        self.carrinho = {}
        self.pagamento = ["pix", "boleto", "cartao"]
        self.sistema_usuarios = SistemaUsuarios()
        self.usuario_logado = None

    def exibir_produtos(self):
        print("Produtos disponíveis:")
        for i, produto in enumerate(self.produtos, start=1):
            print(f"{i}. {produto.nome} - R${produto.preco:.2f}")

    def sel_prods(self):
        self.exibir_produtos()

        while True:
            try:
                escolha = int(input("Digite o número do produto desejado (ou 0 para sair): "))
                if escolha == 0:
                    if self.usuario_logado:
                        break
                    else:
                        print("Você precisa estar logado para finalizar a compra.")
                elif 1 <= escolha <= len(self.produtos):
                    produto = self.produtos[escolha - 1]
                    quantidade = int(input("Digite a quantidade desejada: "))
                    self.add_to_cart(produto, quantidade)
                    print(f"{quantidade} {produto.nome}(s) adicionado(s) ao carrinho.")
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Digite um número válido.")

        if self.usuario_logado and self.carrinho:
            self.finalizar_compra()

    def add_to_cart(self, produto, quantidade):
        if produto in self.carrinho:
            self.carrinho[produto] += quantidade
        else:
            self.carrinho[produto] = quantidade

    def visualizar_carrinho(self):
        print("Carrinho:")
        for produto, quantidade in self.carrinho.items():
            print(f"{quantidade} {produto}")

    def finalizar_compra(self):
        if self.usuario_logado:
            self.visualizar_carrinho()
            valor_total = sum(produto.preco * quantidade for produto, quantidade in self.carrinho.items())
            print(f"Total a pagar: R${valor_total:.2f}")
            forma_pagamento = input("Escolha a forma de pagamento (pix/boleto/cartao): ").lower()

            if forma_pagamento in self.pagamento:
                if forma_pagamento == "pix":
                    print("Código Pix gerado com sucesso.")
                    print("Pagamento bem-sucedido, Obrigado pela compra!")
                elif forma_pagamento == "boleto":
                    print("Boleto gerado com sucesso.")
                    print("Pagamento bem-sucedido, Obrigado pela compra!")
                elif forma_pagamento == "cartao":
                    print("Informe os detalhes do cartão.")
                    print("Pagamento bem-sucedido, Obrigado pela compra!")
            else:
                print("Forma de pagamento inválida. Tente novamente.")
        else:
            print("Você precisa estar logado para finalizar a compra.")

    def verificar_cadastro_apos_compra(self):
        resposta = input("Você já possui cadastro? (s/n): ").lower()
        if resposta == 's':
            self.sistema_usuarios.realizar_login()
        elif resposta == 'n':
            self.sistema_usuarios.cadastrar_usuario()
            self.sistema_usuarios.realizar_login()

    def realizar_login(self):
        while True:
            username = input("Digite o nome de usuário: ")
            senha = input("Digite a senha: ")
            if self.sistema_usuarios.realizar_login(username, senha):
                print("Login bem-sucedido!")
                self.usuario_logado = username
                break
            else:
                print("Login falhou. Tente novamente.")

    def cadastrar_usuario(self):
        username = input("Digite o nome de usuário: ")
        senha = input("Digite a senha: ")
        self.sistema_usuarios.cadastrar_usuario(username, senha)
        print("Cadastro realizado com sucesso! Realize o login para continuar.")
        self.realizar_login()


class PaginaInicial:

    def __init__(self):
        self.ekmas = EKMAS()

    def boas_vindas(self):
        print("Bem-vindo à EKMA'S! Onde a beleza se encontra com a compaixão. Descubra a essência da natureza em cada fio.")
        print("Com nossos produtos para cabelo veganos, porque a beleza verdadeira é gentil, ética e eco-friendly!")

    def iniciar_sistema(self):
        self.boas_vindas()

        while True:
            opcao = input("\nEscolha uma opção:\n1. Visualizar produtos\n0. Sair\nOpção: ")

            if opcao == '1':
                if not self.ekmas.usuario_logado:
                    resposta = input("Você já possui cadastro? (s/n): ").lower()
                    if resposta == 's':
                        self.ekmas.realizar_login()
                    elif resposta == 'n':
                        self.ekmas.sistema_usuarios.cadastrar_usuario()
                        self.ekmas.realizar_login()
                    else:
                        break  # Sair do loop se o usuário escolher sair

                self.ekmas.sel_prods()

            elif opcao == '0':
                print("Sistema encerrado.")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def possui_cadastro(self):
        resposta = input("Você já possui cadastro? (s/n): ").lower()
        return resposta == 's'


# Uso do código:
pagina_inicial = PaginaInicial()
pagina_inicial.iniciar_sistema()

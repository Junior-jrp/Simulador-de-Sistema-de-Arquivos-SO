

class GerenciadorArquivos:
    def __init__(self):
        self.rota_raiz = inode("/", é_diretorio=True)
        self.atual = self.rota_raiz
        self.nós = {}

    @staticmethod
    def limpar_tela():
        print("\n" * 50)

    def criar(self, nome, é_diretorio=False):
        if nome in self.atual.subdiretorios:
            print(f"\033[91mError:\033[00m '{nome}' já existente")
            return
        novo_nó = inode(nome, é_diretorio=é_diretorio)
        novo_nó.pai = self.atual
        self.atual.subdiretorios[nome] = novo_nó
        self.nós[novo_nó] = novo_nó
        print(f"\033[92m{'Diretório' if é_diretorio else 'Arquivo'} '{nome}' criado.\033[00m")

    def excluir(self, nome):
        if nome not in self.atual.subdiretorios:
            print(f"\033[91mErro: '{nome}' não encontrado\033[00m")
            return
        nó = self.atual.subdiretorios[nome]
        self.atual.subdiretorios.pop(nome)
        del self.nós[nó]
        print(
            f"\033[91mDiretório\033[00m" if nó.é_diretorio else "\033[92mArquivo\033[00m" + f" '{nome}' excluído com sucesso")

    def ler_arquivo(self, nome_arquivo):
        if nome_arquivo not in self.atual.subdiretorios or self.atual.subdiretorios[nome_arquivo].é_diretorio:
            print(f"\033[91mErro: '{nome_arquivo}' não é um arquivo\033[00m")
            return
        nó = self.atual.subdiretorios[nome_arquivo]
        print(f"\033[96m'{nome_arquivo}':\033[00m\n{nó.ler_blocos()}")

    def navegar(self, nome_diretorio):
        if nome_diretorio == "..":
            if self.atual.pai:
                self.atual = self.atual.pai
            else:
                print("Diretório root")
        elif nome_diretorio == ".":
            pass
        elif nome_diretorio in self.atual.subdiretorios and self.atual.subdiretorios[nome_diretorio].é_diretorio:
            self.atual = self.atual.subdiretorios[nome_diretorio]
        else:
            print(f"\033[91mErro: '{nome_diretorio}' é inválido\033[00m")
        print(f"Diretório atual: {self.atual.nome}")

    def mover(self, nome_arquivo, nome_diretorio_destino):
        if nome_arquivo not in self.atual.subdiretorios:
            print(f"\033[91mErro: '{nome_arquivo}' Arquivo não encontrado\033[00m")
            return
        if nome_diretorio_destino not in self.atual.subdiretorios or not self.atual.subdiretorios[nome_diretorio_destino].é_diretorio:
            print(f"\033[91mErro: '{nome_diretorio_destino}' Diretório não encontrado\033[00m")
            return

        nó = self.atual.subdiretorios.pop(nome_arquivo)
        diretorio_destino = self.atual.subdiretorios[nome_diretorio_destino]
        nó.pai = diretorio_destino
        diretorio_destino.subdiretorios[nome_arquivo] = nó
        self.nós[nó] = nó
        print(f"\033[92mArquivo '{nome_arquivo}' movido para '{nome_diretorio_destino}'\033[00m")

    def listar_diretorio(self):
        print(f"\033[96mConteúdo de {self.atual.nome}:\033[00m")
        for nó in sorted(self.atual.subdiretorios.values()):
            tipo = "DIR" if nó.é_diretorio else "ARQ"
            print(f"\033[93m{tipo}:\033[94m{nó.nome}\033[00m ({nó.tamanho} bytes)")

    def escrever_arquivo(self, nome_arquivo, dados):
        if nome_arquivo not in self.atual.subdiretorios or self.atual.subdiretorios[nome_arquivo].é_diretorio:
            print(f"\033[91mErro: '{nome_arquivo}' é inválido \033[00m")
            return
        nó = self.atual.subdiretorios[nome_arquivo]
        nó.adicionar_bloco(dados)
        print(f"Arquivo'{nome_arquivo}' atualizado com sucesso")

class inode:
    def __init__(self, nome, é_diretorio=False):
        self.nome = nome
        self.tamanho = 0
        self.bloco = ""
        self.é_diretorio = é_diretorio
        self.subdiretorios = {} if é_diretorio else None
        self.pai = None

    def adicionar_bloco(self, dados):
        if isinstance(dados, bytes):
            dados = dados.decode()
        self.bloco += dados
        self.tamanho += len(dados)

    def ler_blocos(self):
        return self.bloco if self.bloco else "(vazio)"

    def __lt__(self, other):
        return self.nome < other.nome



def main():
    gerenciador = GerenciadorArquivos()

    while True:
        print("\n\033[95mSistema de Arquivos Mac Junior\033[00m")
        print("\033[97m1. Criar arquivo/diretório\033[00m")
        print("\033[97m2. Listar conteúdo do diretório atual\033[00m")
        print("\033[97m3. Navegar para diretório\033[00m")
        print("\033[97m4. Mover arquivo\033[00m")
        print("\033[97m5. Escrever em arquivo\033[00m")
        print("\033[97m6. Ler arquivo\033[00m")
        print("\033[97m7. Excluir arquivo/diretório\033[00m")
        print("\033[97m8. Limpar tela\033[00m")
        print("\033[97m9. Sair\033[00m")

        escolha = input("\033[97mEscolha uma opção (1-9): \033[00m")

        if escolha == "1":
            nome = input("Digite o nome do arquivo/diretório: ")
            é_diretorio = input("É um diretório? (s/n): ").lower() == "s"
            gerenciador.criar(nome, é_diretorio=é_diretorio)
        elif escolha == "2":
            gerenciador.listar_diretorio()
        elif escolha == "3":
            nome_diretorio = input("Digite o nome do diretório para navegar: ")
            gerenciador.navegar(nome_diretorio)
        elif escolha == "4":
            nome_arquivo = input("Digite o nome do arquivo para mover: ")
            nome_diretorio_destino = input("Digite o nome do diretório de destino: ")
            gerenciador.mover(nome_arquivo, nome_diretorio_destino)
        elif escolha == "5":
            nome_arquivo = input("Digite o nome do arquivo: ")
            dados = input("Digite os dados para escrever: ")
            gerenciador.escrever_arquivo(nome_arquivo, dados.encode())
        elif escolha == "6":
            nome_arquivo = input("Digite o nome do arquivo: ")
            gerenciador.ler_arquivo(nome_arquivo)
        elif escolha == "7":
            nome = input("Digite o nome do arquivo/diretório para excluir: ")
            gerenciador.excluir(nome)
        elif escolha == "8":
            gerenciador.limpar_tela()
        elif escolha == "9":
            ascii_art = """                                                  
                                .
                               ":"
                             ___:____     |"\\/\"|
                           ,'        `.    \\  /
                           |  O        \\___/  |
                         ~^~^~^~^~^~^~^~^~^~^~^~^~            
                """
            print(f"\033[96mObrigado por usar o nosso sistema de arquivos. Até a próxima!\n{ascii_art}\033[00m")
            break

        else:
            print("\033[91mOpção inválida. Tente novamente.\033[00m")


if __name__ == "__main__":
    main()





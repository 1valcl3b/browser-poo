class Historico:
    def __init__(self):
        self.pilha = []

    def empilhar(self, url: str):
        self.pilha.append(url)

    def desempilhar(self):
        if not self.esta_vazio():
            return self.pilha.pop()
        return None

    def esta_vazio(self) -> bool:
        return len(self.pilha) == 0

    def listar(self) -> str:
        if self.pilha:
            return "[" + "][".join(self.pilha) + "]"
        return "[ ]"

class Browser:
    def __init__(self):
        self.historico = Historico()
        self.home = None
        self.urls_validas = self.carregar_arquivo()

    def carregar_arquivo(self) -> set:
        try:
            with open("urls.txt", "r") as f:
                return {linha.strip() for linha in f if linha.strip()}
        except FileNotFoundError:
            print("Arquivo 'urls.txt' não foi encontrado. Iniciando com Historico vazio .")
            return set()

    def validar_url(self, url: str) -> bool:
        return url in self.urls_validas

    def adicionar_url(self, url: str):
        if url in self.urls_validas:
            print(f"ERRO: URL '{url}' já existe!")
            return
        if not url.startswith("www"):
            print("ERRO: URL deve começar com 'www'")
            return
        self.urls_validas.add(url)
        print(f"URL '{url}' adicionada!")

    def exibir_tela(self):
        print("\n" + "-"*40)
        print(f"Histórico de Visitas: {self.historico.listar()}")
        print(f"Home: [{self.home if self.home else ' '}]")
        print("Digite a url ou #back para retornar à última página visitada.")

    def navegar_para(self, url_destino: str):
        if not self.validar_url(url_destino):
            print(f"ERRO: '{url_destino}' não é uma URL válida!")
            return
        if self.home is not None:
            self.historico.empilhar(self.home)
        self.home = url_destino

    def voltar(self):
        if self.historico.esta_vazio():
            print("ERRO: Não há página anterior para voltar!")
            return
        self.home = self.historico.desempilhar()
        print(f"\nVoltando para {self.home}\n")

    def mostrar_historico(self):
        print(f"\nHistórico completo: {self.historico.listar()}\n")

navegador = Browser()
while True:
  navegador.exibir_tela()
  comando = input("url: ").strip()
  if comando == "#sair":
    break
  elif comando == "#back":
    navegador.voltar()
  elif comando == "#showhist":
    navegador.mostrar_historico()
  elif comando.startswith("#add"):
    partes = comando.split(maxsplit=1)
    if len(partes) == 2:
      url = partes[1]
      if url.startswith("www"):
        navegador.adicionar_url(url)
      else:
        print("ERRO: URL deve começar com 'www'")
    else:
      print("ERRO: Use #add <url>")
  else:
    navegador.navegar_para(comando)
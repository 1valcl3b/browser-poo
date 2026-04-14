class Historico:
    def __init__(self):
        self.pilha = []
        
    def empilhar(self, url):
        self.pilha.append(url)

    def desempilhar(self):
        if self.pilha:
            return self.pilha.pop()
        return None

    def listar(self):
        if not self.pilha:
           return "[ ]"

        res = ""
        for item in self.pilha:
            res += f"[{item}]"
        return res
    
class Browser:
    def __init__(self):
        self.historico = Historico()
        self.home = None
        self.urls_validas = self.carregar_arq()
        self.historico_completo = []

    def carregar_arq(self):
        try:
            with open("urls.txt", "r") as f:
                urls = set()
                for linha in f:
                    urls.add(linha.strip())
            return urls

        except FileNotFoundError:
            print("Arquivo não foi encontrado. Iniciando com Historico vazio.")
            return set()

    def validar_url(self, url):
        return url in self.urls_validas

    def adicionar_url(self, url):
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

    def navegar_para(self, url_destino):
        if self.validar_url(url_destino) == False:
            print(f"ERRO: '{url_destino}' não é uma URL válida!")
            return
        
        if self.home is not None:
            self.historico.empilhar(self.home)
        self.home = url_destino

        self.historico_completo.append(url_destino)

    def voltar(self):
        if  not self.historico.pilha:
            print("ERRO: Não há página anterior para voltar!")
            return
        
        self.home = self.historico.desempilhar()

        self.historico_completo.append(self.home)
        print(f"\nVoltando para {self.home}\n")


    def show_historico(self):
        if self.historico_completo:
            res = ""
            for item in self.historico_completo:
                res += f"[{item}]"
        else:
            res = "[ ]"

        return print(f"Historico completo: {res}")
          

navegador = Browser()

while True:
  navegador.exibir_tela()
  comando = input("url: ").strip()

  if comando == "#sair":
    break
  
  elif comando == "#back":
    navegador.voltar()
    
  elif comando == "#showhist":
    navegador.show_historico()
    
  elif comando.startswith("#add"):
      partes = comando.split(maxsplit=1)
      if len(partes) != 2:
          print("ERRO: use #add <url> ")
      else:
          url = partes[1]
          navegador.adicionar_url(url)     
  
  else:
    navegador.navegar_para(comando)
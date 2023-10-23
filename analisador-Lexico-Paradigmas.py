import re
from tkinter import *
from tkinter.filedialog import askopenfile 

class Application:
  def __init__(self, master=None):
    self.widget1 = Frame(master)
    self.widget1.pack()
    self.msg = Label(self.widget1, text="Interpretador Léxico")
    self.msg["font"] = ("Verdana", "10", "italic", "bold")
    self.msg.pack ()
    self.instrucao = Label(self.widget1, text="insira um arquivo \".in\" com a expressão que deseja analisar")
    self.instrucao["font"] = ("Verdana", "8", "italic")
    self.instrucao.pack()
    self.botao = Button(self.widget1)
    self.botao["text"] = "escolha o arquivo"
    self.botao["font"] = ("Calibri", "10")
    self.botao["width"] = 20
    self.botao["command"] = self.open_file
    self.botao.pack ()
    # Definindo a lista de palavras-chave
    self.palavras_chaves = [
      (r'\(', 'init_parenteses'),
      (r'\)', 'close_parenteses'),
      (r'\+', 'ou'),
      (r'\*', 'e'),
      (r'True', 'verdadeiro'),
      (r'False', 'falso'),
      (r'->', 'implica'),
      (r'<->', 'se_e_somente_se'),
      (r'¬', 'nao'),
      (r'[a-zA-Z_][a-zA-Z0-9_]{0,99}', 'variavel'),
    ]
    

  # Função que faz com que os comentários sejam ignorados
  def ignorando_comentarios(self, text):
    return re.sub(r'\\.*', '', text).rstrip()

  def analisador_lexico(self, expressao):
    tokens = []
    while expressao:
      # lstrip faz com que os espaços em branco à esquerda sejam ignorados.
      expressao = expressao.lstrip()
      for pattern, nome_do_token in self.palavras_chaves:
        # A variável match tenta fazer uma correspondência entre as palavras-chave e a expressão no início da linha.
        match = re.match(pattern, expressao)
        if match:
          token = match.group(0)
          tokens.append((token, nome_do_token))
          expressao = expressao[len(token):]
          break
      else:
        raise ValueError(f"Caractere inválido na expressão: {expressao[0]}")
    return tokens
  
  def open_file(self):
    file_path = askopenfile(mode='r', filetypes=[('in files', '*.in')])
    if file_path is not None:
      with open(file_path.name, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
          linha = self.ignorando_comentarios(linha)
          tokens = self.analisador_lexico(linha)
          self.msg1 = Label(self.widget1, text="expressão encontrada:")
          self.msg1.pack()
          self.expressao = Label(self.widget1, text = linha)
          self.expressao.pack()
          self.msg2 = Label(self.widget1, text="Resultado da analise:")
          self.msg2.pack()
          self.label = Label(self.widget1)
          self.label["text"] = tokens
          self.label.pack()

root = Tk()
root.title("Interpretador Léxico")
root.geometry('800x600')
Application(root)
root.mainloop()
"""
SmartCity - mensagens seguras entre as filiais de Maricá e Niterói
COM TELA DE LOGIN E CADASTRO + CIFRA DE VIGENÈRE
INCLUI HISTÓRICO DE LOGIN E HISTÓRICO DE MENSAGENS

Para abrir: python smartcity_login.py
"""

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os


# ======================================================================
# PARTE 0 - GERENCIAMENTO DE USUÁRIOS
# ======================================================================

ARQUIVO_USUARIOS = "usuarios.json"


def gerar_codigo_hora():
    """Gera código baseado em data e hora: YYYYMMDDHH"""
    agora = datetime.now()
    return agora.strftime("%Y%m%d%H")


def carregar_usuarios():
    """Carrega usuários do arquivo."""
    if not os.path.exists(ARQUIVO_USUARIOS):
        return {}
    try:
        with open(ARQUIVO_USUARIOS, "r") as f:
            return json.load(f)
    except:
        return {}


def salvar_usuarios(usuarios):
    """Salva usuários no arquivo."""
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f)


def username_existe(username):
    """Verifica se username existe."""
    usuarios = carregar_usuarios()
    return username in usuarios


def validar_login(username, senha):
    """Valida login."""
    usuarios = carregar_usuarios()
    if username not in usuarios:
        return False
    return usuarios[username] == senha


def cadastrar_usuario(username, senha):
    """Cadastra novo usuário."""
    usuarios = carregar_usuarios()
    usuarios[username] = senha
    salvar_usuarios(usuarios)


# ======================================================================
# PARTE 0.5 - HISTÓRICOS (LOGIN E MENSAGENS)
# ======================================================================

ARQUIVO_HIST_LOGIN = "historico_login.json"
ARQUIVO_HIST_MENSAGENS = "historico_mensagens.json"


def agora_formatado():
    """Data e hora atuais no formato DD/MM/AAAA HH:MM:SS."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def carregar_historico(caminho):
    """Lê uma lista de registros de um arquivo JSON (lista vazia se não existir)."""
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados if isinstance(dados, list) else []
    except (OSError, ValueError):
        return []


def adicionar_registro(caminho, registro):
    """Acrescenta um registro ao histórico. Nunca derruba o programa se falhar."""
    historico = carregar_historico(caminho)
    historico.append(registro)
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def registrar_login(username, evento):
    """Registra um evento de login. evento: 'Login com sucesso', 'Senha incorreta',
    'Usuário inexistente' ou 'Cadastro'."""
    adicionar_registro(ARQUIVO_HIST_LOGIN, {
        "data_hora": agora_formatado(),
        "usuario": username,
        "evento": evento,
    })


def registrar_mensagem(username, acao, arquivo, tamanho):
    """Registra uma mensagem enviada/lida.
    Só guarda dados do envio (quem, quando, arquivo, tamanho) - NUNCA o texto da
    mensagem, para não anular a criptografia."""
    adicionar_registro(ARQUIVO_HIST_MENSAGENS, {
        "data_hora": agora_formatado(),
        "usuario": username,
        "acao": acao,
        "arquivo": arquivo,
        "tamanho": tamanho,
    })


# ======================================================================
# PARTE 1 - TELA DE LOGIN
# ======================================================================

class TelaLogin:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("SmartCity - Login")
        self.janela.geometry("600x500")
        
        # Título
        titulo = ttk.Label(self.janela, text="SmartCity", font=("Arial", 16, "bold"))
        titulo.pack(pady=20)
        
        subtitulo = ttk.Label(self.janela, text="Login", font=("Arial", 11))
        subtitulo.pack(pady=(0, 20))
        
        # Frame
        frame = ttk.Frame(self.janela, padding=20)
        frame.pack(fill="both", expand=True)
        
        # Username
        ttk.Label(frame, text="Username:").pack(anchor="w")
        self.username = ttk.Entry(frame, width=30)
        self.username.pack(fill="x", pady=(0, 15))
        self.username.focus()
        
        # Senha
        ttk.Label(frame, text="Senha:").pack(anchor="w")
        self.senha = ttk.Entry(frame, width=30, show="*")
        self.senha.pack(fill="x", pady=(0, 20))
        
        # Botão Login
        ttk.Button(frame, text="Login", command=self.fazer_login).pack(fill="x", pady=(0, 8))
        
        # Link Cadastro
        linha = ttk.Frame(frame)
        linha.pack(fill="x")
        ttk.Label(linha, text="Sem conta? ").pack(side="left")
        ttk.Button(linha, text="Cadastrar", command=self.abrir_cadastro, width=10).pack(side="left")
        
        self.senha.bind("<Return>", lambda e: self.fazer_login())
    
    def fazer_login(self):
        """Faz login."""
        username = self.username.get().strip()
        senha = self.senha.get()
        
        if not username:
            messagebox.showwarning("Erro", "Digite o username")
            return
        
        if not senha:
            messagebox.showwarning("Erro", "Digite a senha")
            return
        
        if not validar_login(username, senha):
            if username_existe(username):
                registrar_login(username, "Senha incorreta")
            else:
                registrar_login(username, "Usuário inexistente")
            messagebox.showerror("Erro", "Username ou senha incorretos")
            self.username.delete(0, "end")
            self.senha.delete(0, "end")
            return
        
        registrar_login(username, "Login com sucesso")
        self.janela.destroy()
        abrir_smartcity(username)
    
    def abrir_cadastro(self):
        """Abre tela de cadastro."""
        self.janela.withdraw()
        TelaCadastro(self.janela)


# ======================================================================
# PARTE 2 - TELA DE CADASTRO
# ======================================================================

class TelaCadastro:
    def __init__(self, janela_login):
        self.janela_login = janela_login
        self.janela = tk.Toplevel(janela_login)
        self.janela.title("SmartCity - Cadastro")
        self.janela.geometry("600x500")
        
        # Título
        titulo = ttk.Label(self.janela, text="Criar Conta", font=("Arial", 14, "bold"))
        titulo.pack(pady=20)
        
        # Frame
        frame = ttk.Frame(self.janela, padding=15)
        frame.pack(fill="both", expand=True)
        
        # Username
        ttk.Label(frame, text="Username:").pack(anchor="w")
        self.username = ttk.Entry(frame, width=30)
        self.username.pack(fill="x", pady=(0, 12))
        
        # Senha
        ttk.Label(frame, text="Senha:").pack(anchor="w")
        self.senha = ttk.Entry(frame, width=30, show="*")
        self.senha.pack(fill="x", pady=(0, 12))
        
        # Confirmar
        ttk.Label(frame, text="Confirmar Senha:").pack(anchor="w")
        self.confirmar = ttk.Entry(frame, width=30, show="*")
        self.confirmar.pack(fill="x", pady=(0, 12))
        
        # Código
        ttk.Label(frame, text="Código de Acesso:").pack(anchor="w")
        self.codigo = ttk.Entry(frame, width=30)
        self.codigo.pack(fill="x", pady=(0, 3))
        
        ttk.Label(frame, text="(Muda a cada hora)", font=("Arial", 8)).pack(anchor="w", pady=(0, 15))
        
        # Botões
        ttk.Button(frame, text="Cadastrar", command=self.cadastrar).pack(fill="x", pady=(0, 8))
        ttk.Button(frame, text="Voltar", command=self.voltar).pack(fill="x")
        
        self.codigo.bind("<Return>", lambda e: self.cadastrar())
    
    def cadastrar(self):
        """Cadastra usuário."""
        username = self.username.get().strip()
        senha = self.senha.get()
        confirmar = self.confirmar.get()
        codigo = self.codigo.get().strip()
        
        if not username:
            messagebox.showwarning("Erro", "Digite um username")
            return
        
        if username_existe(username):
            messagebox.showwarning("Erro", "Username já existe")
            return
        
        if not senha:
            messagebox.showwarning("Erro", "Digite a senha")
            return
        
        if senha != confirmar:
            messagebox.showwarning("Erro", "Senhas não combinam")
            return
        
        if not codigo:
            messagebox.showwarning("Erro", "Digite o código")
            return
        
        codigo_correto = gerar_codigo_hora()
        if codigo != codigo_correto:
            messagebox.showerror("Erro", f"Código errado!\nCódigo correto: {codigo_correto}")
            return
        
        cadastrar_usuario(username, senha)
        registrar_login(username, "Cadastro")
        messagebox.showinfo("Sucesso", "Conta criada!\nFaça login agora.")
        self.janela.destroy()
        self.janela_login.deiconify()
    
    def voltar(self):
        """Volta para login."""
        self.janela.destroy()
        self.janela_login.deiconify()


# ======================================================================
# PARTE 3 - A ÁRVORE (original)
# ======================================================================

class No:
    """Um nó da árvore: guarda uma letra e aponta para no máximo 2 filhos."""

    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


def gerar_arvore(texto):
    """Transforma o texto em uma árvore."""
    if texto == "":
        return None
    meio = len(texto) // 2
    no = No(texto[meio])
    no.esquerda = gerar_arvore(texto[:meio])
    no.direita = gerar_arvore(texto[meio + 1:])
    return no


def ler_em_ordem(no):
    """Lê a árvore em ordem (esquerda, raiz, direita) e devolve o texto."""
    if no is None:
        return ""
    return ler_em_ordem(no.esquerda) + no.valor + ler_em_ordem(no.direita)


def desenhar(no, nivel=0):
    """Devolve as linhas para mostrar a árvore 'deitada' na tela."""
    if no is None:
        return []
    return (desenhar(no.direita, nivel + 1)
            + ["    " * nivel + repr(no.valor)]
            + desenhar(no.esquerda, nivel + 1))


# ======================================================================
# PARTE 4 - CRIPTOGRAFIA (CIFRA DE VIGENÈRE)
# ======================================================================

def criptografar_vigenere(no, chave, indice=0):
    """
    Criptografa a árvore aplicando a Cifra de Vigenère em ordem in-order (esquerda, raiz, direita).
    Usa os códigos ord() dos caracteres da chave textual.
    """
    if no is None:
        return indice
    indice = criptografar_vigenere(no.esquerda, chave, indice)
    
    deslocamento = ord(chave[indice % len(chave)])
    if isinstance(no.valor, str):
        val = ord(no.valor)
    else:
        val = no.valor
    no.valor = val + deslocamento
    
    indice += 1
    indice = criptografar_vigenere(no.direita, chave, indice)
    return indice


def descriptografar_vigenere(no, chave, indice=0):
    """
    Descriptografa a árvore revertendo a Cifra de Vigenère em ordem in-order (esquerda, raiz, direita).
    """
    if no is None:
        return indice
    indice = descriptografar_vigenere(no.esquerda, chave, indice)
    
    deslocamento = ord(chave[indice % len(chave)])
    if isinstance(no.valor, int):
        val = no.valor
    else:
        val = ord(no.valor)
    no.valor = chr(val - deslocamento)
    
    indice += 1
    indice = descriptografar_vigenere(no.direita, chave, indice)
    return indice


# ======================================================================
# PARTE 5 - SALVAR E LER O ARQUIVO (original)
# ======================================================================

def arvore_para_dicionario(no):
    if no is None:
        return None
    return {
        "valor": no.valor,
        "esquerda": arvore_para_dicionario(no.esquerda),
        "direita": arvore_para_dicionario(no.direita),
    }


def dicionario_para_arvore(dados):
    if dados is None:
        return None
    no = No(dados["valor"])
    no.esquerda = dicionario_para_arvore(dados["esquerda"])
    no.direita = dicionario_para_arvore(dados["direita"])
    return no


def salvar_arquivo(caminho, no):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(arvore_para_dicionario(no), arquivo)


def carregar_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


# ======================================================================
# PARTE 6 - A JANELA DO SMARTCITY
# ======================================================================

TIPOS_ARQUIVO = [("Mensagem SmartCity", "*.json")]


def criar_caixa(pai, altura, so_leitura):
    """Cria uma caixa de texto com barra de rolagem."""
    quadro = ttk.Frame(pai)
    caixa = tk.Text(quadro, height=altura, font=("Consolas", 10))
    barra = ttk.Scrollbar(quadro, command=caixa.yview)
    caixa.config(yscrollcommand=barra.set)
    barra.pack(side="right", fill="y")
    caixa.pack(side="left", fill="both", expand=True)
    if so_leitura:
        caixa.config(state="disabled")
    return quadro, caixa


def mostrar(caixa, texto):
    """Troca o texto de uma caixa que o usuário não pode editar."""
    caixa.config(state="normal")
    caixa.delete("1.0", "end")
    caixa.insert("1.0", texto)
    caixa.config(state="disabled")


def ler_chave(campo):
    """Lê a chave textual digitada para a Cifra de Vigenère."""
    chave = campo.get().strip()
    if not chave:
        messagebox.showwarning("Chave", "Digite uma chave (palavra/frase secreta) para a Cifra de Vigenère.")
        return None
    return chave


class App:
    def __init__(self, janela, usuario=""):
        self.usuario = usuario
        janela.title("SmartCity - Mensagens seguras (Cifra de Vigenère) - Usuário: " + usuario)
        janela.geometry("700x680")

        self.arvore = None
        self.texto_da_arvore = ""
        self.criptografada = False
        self.dados_lidos = None
        self.caminho_lido = ""

        abas = ttk.Notebook(janela)
        abas.pack(fill="both", expand=True, padx=10, pady=10)
        aba_escrever = ttk.Frame(abas, padding=10)
        aba_ler = ttk.Frame(abas, padding=10)
        aba_historico = ttk.Frame(abas, padding=10)
        abas.add(aba_escrever, text="Escrever")
        abas.add(aba_ler, text="Ler")
        abas.add(aba_historico, text="Histórico")
        self.montar_escrever(aba_escrever)
        self.montar_ler(aba_ler)
        self.montar_historico(aba_historico)
        # Atualiza as tabelas sempre que a aba Histórico é aberta
        abas.bind("<<NotebookTabChanged>>",
                  lambda e: self.atualizar_historicos() if abas.select() == str(aba_historico) else None)

    def montar_escrever(self, aba):
        ttk.Label(aba, text="Mensagem:").pack(anchor="w")
        quadro, self.campo_mensagem = criar_caixa(aba, 6, False)
        quadro.pack(fill="x", pady=(0, 10))

        linha = ttk.Frame(aba)
        linha.pack(fill="x", pady=(0, 10))
        ttk.Label(linha, text="Chave (Palavra/Palavra-Passe):").pack(side="left")
        self.chave_escrever = ttk.Entry(linha, width=20)
        self.chave_escrever.pack(side="left", padx=5)

        botoes = ttk.Frame(aba)
        botoes.pack(fill="x", pady=(0, 10))
        ttk.Button(botoes, text="Gerar Árvore", command=self.clicou_gerar).pack(side="left", padx=(0, 5))
        ttk.Button(botoes, text="Criptografar Árvore", command=self.clicou_criptografar).pack(side="left", padx=5)
        ttk.Button(botoes, text="Salvar Mensagem", command=self.clicou_salvar).pack(side="left", padx=5)

        self.status_escrever = ttk.Label(aba, text="Digite a mensagem e clique em Gerar Árvore.")
        self.status_escrever.pack(anchor="w", pady=(0, 10))

        ttk.Label(aba, text="Árvore (a raiz é a linha mais à esquerda):").pack(anchor="w")
        quadro, self.caixa_arvore_escrever = criar_caixa(aba, 14, True)
        quadro.pack(fill="both", expand=True)

    def mensagem_mudou(self):
        if self.campo_mensagem.get("1.0", "end-1c") != self.texto_da_arvore:
            messagebox.showwarning("Mensagem", "A mensagem foi alterada. Clique em Gerar Árvore de novo.")
            return True
        return False

    def clicou_gerar(self):
        texto = self.campo_mensagem.get("1.0", "end-1c")
        if texto.strip() == "":
            messagebox.showwarning("Mensagem", "Escreva uma mensagem primeiro.")
            return
        self.arvore = gerar_arvore(texto)
        self.texto_da_arvore = texto
        self.criptografada = False
        mostrar(self.caixa_arvore_escrever, "\n".join(desenhar(self.arvore)))
        self.status_escrever.config(text="Árvore gerada. Digite a palavra-chave e clique em Criptografar Árvore.")

    def clicou_criptografar(self):
        if self.arvore is None:
            messagebox.showwarning("Árvore", "Clique em Gerar Árvore primeiro.")
            return
        if self.criptografada:
            messagebox.showinfo("Árvore", "A árvore já está criptografada. Clique em Salvar Mensagem.")
            return
        if self.mensagem_mudou():
            return
        chave = ler_chave(self.chave_escrever)
        if chave is None:
            return
        criptografar_vigenere(self.arvore, chave)
        self.criptografada = True
        mostrar(self.caixa_arvore_escrever, "\n".join(desenhar(self.arvore)))
        self.status_escrever.config(text="Árvore criptografada com Vigenère. Clique em Salvar Mensagem.")

    def clicou_salvar(self):
        if self.arvore is None or not self.criptografada:
            messagebox.showwarning("Salvar", "Gere e criptografe a árvore antes de salvar.")
            return
        if self.mensagem_mudou():
            return
        caminho = filedialog.asksaveasfilename(
            title="Salvar mensagem (escolha o pen drive)",
            defaultextension=".json", filetypes=TIPOS_ARQUIVO)
        if caminho == "":
            return
        try:
            salvar_arquivo(caminho, self.arvore)
        except OSError:
            messagebox.showerror("Salvar", "Não foi possível salvar o arquivo.")
            return
        registrar_mensagem(self.usuario, "Enviada", caminho, len(self.texto_da_arvore))
        self.status_escrever.config(text="Mensagem salva em: " + caminho)
        messagebox.showinfo("Salvar", "Mensagem salva com sucesso!")

    def montar_ler(self, aba):
        ttk.Button(aba, text="Ler Mensagem", command=self.clicou_ler).pack(anchor="w", pady=(0, 10))

        linha = ttk.Frame(aba)
        linha.pack(fill="x", pady=(0, 10))
        ttk.Label(linha, text="Chave (Palavra/Palavra-Passe):").pack(side="left")
        self.chave_ler = ttk.Entry(linha, width=20)
        self.chave_ler.pack(side="left", padx=5)
        ttk.Button(linha, text="Descriptografar", command=self.clicou_descriptografar).pack(side="left", padx=5)

        self.status_ler = ttk.Label(aba, text="Clique em Ler Mensagem e escolha o arquivo do pen drive.")
        self.status_ler.pack(anchor="w", pady=(0, 10))

        quadro, self.caixa_mensagem_lida = criar_caixa(aba, 6, True)
        quadro.pack(side="bottom", fill="x")
        ttk.Label(aba, text="Mensagem:").pack(side="bottom", anchor="w")

        ttk.Label(aba, text="Árvore (a raiz é a linha mais à esquerda):").pack(anchor="w")
        quadro, self.caixa_arvore_ler = criar_caixa(aba, 12, True)
        quadro.pack(fill="both", expand=True, pady=(0, 10))

    # ------------------------------------------------------------------
    # ABA HISTÓRICO
    # ------------------------------------------------------------------
    def criar_tabela(self, pai, colunas):
        """Cria uma tabela (Treeview) com barra de rolagem. colunas = [(titulo, largura), ...]"""
        quadro = ttk.Frame(pai)
        tabela = ttk.Treeview(quadro, columns=[c[0] for c in colunas], show="headings")
        for titulo, largura in colunas:
            tabela.heading(titulo, text=titulo)
            tabela.column(titulo, width=largura, anchor="w")
        barra = ttk.Scrollbar(quadro, command=tabela.yview)
        tabela.config(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        tabela.pack(side="left", fill="both", expand=True)
        return quadro, tabela

    def montar_historico(self, aba):
        topo = ttk.Frame(aba)
        topo.pack(fill="x", pady=(0, 8))
        ttk.Button(topo, text="Atualizar", command=self.atualizar_historicos).pack(side="left")

        ttk.Label(aba, text="Histórico de mensagens:", font=("Arial", 10, "bold")).pack(anchor="w")
        quadro, self.tabela_mensagens = self.criar_tabela(aba, [
            ("Data/Hora", 130), ("Usuário", 90), ("Ação", 70),
            ("Arquivo", 250), ("Caracteres", 80)])
        quadro.pack(fill="both", expand=True, pady=(0, 10))

        ttk.Label(aba, text="Histórico de login:", font=("Arial", 10, "bold")).pack(anchor="w")
        quadro, self.tabela_logins = self.criar_tabela(aba, [
            ("Data/Hora", 150), ("Usuário", 150), ("Evento", 250)])
        quadro.pack(fill="both", expand=True)

    def atualizar_historicos(self):
        """Recarrega as duas tabelas do disco, do mais recente para o mais antigo."""
        for tabela in (self.tabela_mensagens, self.tabela_logins):
            tabela.delete(*tabela.get_children())
        for r in reversed(carregar_historico(ARQUIVO_HIST_MENSAGENS)):
            self.tabela_mensagens.insert("", "end", values=(
                r.get("data_hora", ""), r.get("usuario", ""), r.get("acao", ""),
                r.get("arquivo", ""), r.get("tamanho", "")))
        for r in reversed(carregar_historico(ARQUIVO_HIST_LOGIN)):
            self.tabela_logins.insert("", "end", values=(
                r.get("data_hora", ""), r.get("usuario", ""), r.get("evento", "")))

    def clicou_ler(self):
        caminho = filedialog.askopenfilename(
            title="Escolha o arquivo da mensagem", filetypes=TIPOS_ARQUIVO)
        if caminho == "":
            return
        try:
            dados = carregar_arquivo(caminho)
            arvore = dicionario_para_arvore(dados)
        except Exception:
            messagebox.showerror("Ler", "Esse arquivo não é uma mensagem SmartCity válida.")
            return
        if arvore is None:
            messagebox.showerror("Ler", "A mensagem está vazia.")
            return
        self.dados_lidos = dados
        self.caminho_lido = caminho
        mostrar(self.caixa_arvore_ler, "\n".join(desenhar(arvore)))
        mostrar(self.caixa_mensagem_lida, "")
        self.status_ler.config(text="Árvore carregada (criptografada). Digite a chave e clique em Descriptografar.")

    def clicou_descriptografar(self):
        if self.dados_lidos is None:
            messagebox.showwarning("Descriptografar", "Clique em Ler Mensagem primeiro.")
            return
        chave = ler_chave(self.chave_ler)
        if chave is None:
            return
        try:
            arvore = dicionario_para_arvore(self.dados_lidos)
            descriptografar_vigenere(arvore, chave)
            texto = ler_em_ordem(arvore)
            mostrar(self.caixa_arvore_ler, "\n".join(desenhar(arvore)))
            mostrar(self.caixa_mensagem_lida, texto)
        except Exception:
            messagebox.showerror("Descriptografar", "Não foi possível descriptografar. A chave está errada.")
            return
        registrar_mensagem(self.usuario, "Lida", self.caminho_lido, len(texto))
        self.status_ler.config(text="Pronto. Se o texto saiu embaralhado, a chave está errada: tente de novo.")


def abrir_smartcity(usuario=""):
    """Abre SmartCity após login."""
    janela = tk.Tk()
    App(janela, usuario)
    janela.mainloop()


if __name__ == "__main__":
    janela = tk.Tk()
    TelaLogin(janela)
    janela.mainloop()

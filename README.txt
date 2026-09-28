===============================================
SMARTCITY - MENSAGENS SEGURAS (CIFRA DE VIGENÈRE)
===============================================

O QUÊ?
======
SmartCity é um programa para enviar mensagens de forma segura entre a filial de Maricá e a filial de Niterói, usando uma estrutura de dados de árvore binária e Cifra de Vigenère.


COMO INSTALAR?
==============
Você NÃO precisa instalar nada!

Requisitos:
- Python 3.6+ instalado (vem com Tkinter já incluído)


COMO USAR?
==========

1. ABRA O PROGRAMA:
   python smartcity_login.py

2. TELA DE LOGIN APARECE

3. PRIMEIRA VEZ? Clique em "Cadastrar"

4. PREENCHA O CADASTRO:
   Username: (escolha um nome, tipo: alice)
   Senha: (escolha uma senha, tipo: abc123)
   Confirmar Senha: (repita a senha)
   Código de Acesso: (veja abaixo como funciona)

5. DEPOIS DE CADASTRAR:
   Volta para LOGIN
   Digite username + senha que acabou de criar
   Clique em "Login"

6. PRONTO!
   SmartCity abre com as 2 abas:
   - Escrever (para Maricá enviar)
   - Ler (para Niterói receber)


QUAL É O CÓDIGO DE ACESSO?
==========================

O código muda A CADA HORA!
Formato: YYYYMMDDHH (Ano + Mês + Dia + Hora)


COMO FUNCIONA?
==============

ABA "ESCREVER" (Maricá):
1. Digite a mensagem
2. Clique "Gerar Árvore" (cria a árvore binária)
3. Digite uma chave textual (ex: "SEGREDO" ou "CHAVE123")
4. Clique "Criptografar Árvore"
5. Clique "Salvar Mensagem"
6. Escolha o pen drive e salve

ABA "LER" (Niterói):
1. Clique "Ler Mensagem"
2. Escolha o arquivo .json do pen drive
3. Digite a MESMA palavra-chave usada em Maricá
4. Clique "Descriptografar"
5. A mensagem original aparece


ABA "HISTÓRICO"
===============

Mostra duas tabelas (do mais recente para o mais antigo):

- Histórico de mensagens: data/hora, usuário, ação (Enviada ou Lida),
  arquivo e quantidade de caracteres.
- Histórico de login: data/hora, usuário e evento (Login com sucesso,
  Senha incorreta, Usuário inexistente, Cadastro).

Clique em "Atualizar" para recarregar. Os dados ficam em
historico_mensagens.json e historico_login.json (mesma pasta do usuarios.json).
O TEXTO das mensagens nunca é gravado no histórico, só os dados do envio.


TECNOLOGIA
==========

- Linguagem: Python
- Interface: Tkinter
- Estrutura de dados: Árvore Binária
- Criptografia: Cifra de Vigenère
- Armazenamento: JSON

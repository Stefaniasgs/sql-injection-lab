# Laboratório de SQL Injection: Ataque e Defesa


## Sobre o projeto

Laboratório prático que demonstra uma vulnerabilidade de SQL Injection 
e as camadas de defesa para mitigá-la, utilizando Python e SQLite.

O projeto simula um sistema de login e percorre três cenários: a 
exploração da vulnerabilidade, a correção usando prepared statements, 
e uma camada adicional de sanitização e validação de entrada.


## Como a vulnerabilidade é explorada

A versão vulnerável constrói a query SQL concatenando diretamente a 
entrada do usuário:

python
query = "SELECT * FROM usuarios WHERE email='" + email + "' AND senha='" + senha + "'"


Isso permite que uma entrada como `' OR '1'='1' --` no campo de email 
burle a autenticação, retornando um resultado válido independentemente 
da senha.


## Como a defesa funciona

**1. Prepared Statements**
A versão segura utiliza queries parametrizadas, onde os valores são 
passados separadamente da estrutura da query:

python
query = "SELECT * FROM usuarios WHERE email = ? AND senha = ?"
cursor.execute(query, (email, senha))


Isso impede que a entrada do usuário seja interpretada como parte do 
comando SQL.

**2. Sanitização e Validação de Entrada**
Como camada adicional, o input passa por validações antes de chegar 
à query:
- Verificação de tamanho máximo de email e senha
- Validação de formato de email via regex
- Bloqueio de caracteres potencialmente perigosos (`'`, `"`, `;`, `\`, `<`, `>`)


## Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| Python | Linguagem principal |
| SQLite | Banco de dados em memória para os testes |
| re (Regex) | Validação de formato e caracteres proibidos |


## Aprendizados

Este projeto evidenciou como uma vulnerabilidade comum como SQL 
Injection pode ser explorada com inputs simples, e como camadas de 
defesa em diferentes níveis prepared statements na camada de banco 
de dados e sanitização na camada de entrada trabalham juntas para 
mitigar o risco.


## Contato

- 💼 [LinkedIn](https://www.linkedin.com/in/stefania-silva-aa84983a5)
- 🐙 [GitHub](https://github.com/Stefaniasgs)
- 📧 stefaniasilva0000@gmail.com

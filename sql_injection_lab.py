import sqlite3
import re

CARACTERES_PROIBIDOS = re.compile(r"['\";\\<>]")
FORMATO_EMAIL        = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
TAMANHO_MAXIMO_EMAIL = 100
TAMANHO_MAXIMO_SENHA = 64


def sanitizar_input(email: str, senha: str) -> tuple[bool, str]:

    if len(email) > TAMANHO_MAXIMO_EMAIL:
        return False, f"Email excede {TAMANHO_MAXIMO_EMAIL} caracteres."
    if len(senha) > TAMANHO_MAXIMO_SENHA:
        return False, f"Senha excede {TAMANHO_MAXIMO_SENHA} caracteres."

    if not FORMATO_EMAIL.match(email):
        return False, "Formato de e-mail inválido."

    if CARACTERES_PROIBIDOS.search(email) or CARACTERES_PROIBIDOS.search(senha):
        return False, "Caracteres não permitidos detectados no input."

    return True, ""


def criar_banco():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE usuarios (
            nome  TEXT,
            email TEXT,
            senha TEXT
        )
    """)
    cursor.execute("INSERT INTO usuarios VALUES ('Ana Silva', 'ana@email.com', 'senha123')")
    cursor.execute("INSERT INTO usuarios VALUES ('João Costa', 'joao@email.com', 'abcd456')")
    conn.commit()
    print("✅ Banco de dados criado!\n")
    return conn


def login_vulneravel(cursor, email, senha):
    print("--- Login Vulnerável ---")
    query = "SELECT * FROM usuarios WHERE email='" + email + "' AND senha='" + senha + "'"
    print("Query executada:", query)
    cursor.execute(query)
    resultado = cursor.fetchone()

    if resultado:
        print("✅ Login realizado! Usuário:", resultado[0])
    else:
        print("❌ Email ou senha incorretos.")

    print()


def login_seguro(cursor, email, senha):
    print("--- Login Seguro ---")
    query = "SELECT * FROM usuarios WHERE email = ? AND senha = ?"
    print("Query executada:", query)
    print("Valores passados:", email, "|", senha)
    cursor.execute(query, (email, senha))
    resultado = cursor.fetchone()

    if resultado:
        print("✅ Login realizado! Usuário:", resultado[0])
    else:
        print("❌ Email ou senha incorretos.")

    print()


def demonstrar_ataque(conn):
    print("=" * 50)
    print("💀 DEMONSTRAÇÃO 1: Ataque no login vulnerável")
    print("=" * 50)
    email_malicioso = "' OR '1'='1' --"
    senha_qualquer  = "nao_importa"
    print("Email digitado:", email_malicioso)
    print("Senha digitada:", senha_qualquer)
    print()
    login_vulneravel(conn.cursor(), email_malicioso, senha_qualquer)


def demonstrar_defesa(conn):
    print("=" * 50)
    print("🛡️  DEMONSTRAÇÃO 2: Ataque bloqueado no login seguro")
    print("=" * 50)
    email_malicioso = "' OR '1'='1' --"
    senha_qualquer  = "nao_importa"
    print("Email digitado:", email_malicioso)
    print("Senha digitada:", senha_qualquer)
    print()
    login_seguro(conn.cursor(), email_malicioso, senha_qualquer)


def demonstrar_sanitizacao(conn):
    print("=" * 50)
    print("🧹 DEMONSTRAÇÃO 4: Sanitização bloqueando na entrada")
    print("=" * 50)

    casos = [
        ("' OR '1'='1' --", "nao_importa",  "Clássico SQL Injection"),
        ("a" * 150,          "senha123",      "Email gigante (DoS)"),
        ("email-sem-arroba", "senha123",      "Formato de e-mail inválido"),
        ("hacker@evil.com",  "x; DROP TABLE","Caractere suspeito na senha"),
    ]

    for email, senha, descricao in casos:
        print(f"\n🔸 Caso: {descricao}")
        print(f"   Email : {email[:60]}{'...' if len(email) > 60 else ''}")
        print(f"   Senha : {senha}")
        valido, motivo = sanitizar_input(email, senha)
        if valido:
            print("   Resultado: ✅ Input aceito — seguindo para o banco.")
            login_seguro(conn.cursor(), email, senha)
        else:
            print(f"   Resultado: 🚫 Input REJEITADO antes de chegar ao banco.")
            print(f"   Motivo   : {motivo}")

    print()


def demonstrar_login_real(conn):
    print("=" * 50)
    print("✅ DEMONSTRAÇÃO 3: Login legítimo funcionando")
    print("=" * 50)
    email_real = "ana@email.com"
    senha_real = "senha123"
    print("Email digitado:", email_real)
    print("Senha digitada:", senha_real)
    print()
    login_seguro(conn.cursor(), email_real, senha_real)


if __name__ == "__main__":
    print("\n🔐 LABORATÓRIO DE DEFESA: SQL INJECTION EM PYTHON")
    print("=" * 50)
    print("Autora: Stefania Guedes")
    print("Área:   Cibersegurança | Python | SQLite")
    print("=" * 50 + "\n")

    conn = criar_banco()
    demonstrar_ataque(conn)
    demonstrar_defesa(conn)
    demonstrar_sanitizacao(conn)
    demonstrar_login_real(conn)

    print("=" * 50)
    print("O QUE APRENDEMOS:")
    print("=" * 50)

    conn.close()
    print("Laboratório encerrado.")
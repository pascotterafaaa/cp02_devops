import os
import sys
from decimal import Decimal, InvalidOperation

import mysql.connector
from mysql.connector import Error


def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "3306")),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "senha_564928"),
        database=os.environ.get("DB_NAME", "dimdim_564928"),
    )


def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS transacoes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        descricao VARCHAR(120) NOT NULL,
        valor DECIMAL(10, 2) NOT NULL,
        tipo ENUM('ENTRADA', 'SAIDA') NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()


def create_transaction():
    descricao = input("Descricao: ").strip()
    valor = read_decimal("Valor: ")
    tipo = read_type()

    sql = "INSERT INTO transacoes (descricao, valor, tipo) VALUES (%s, %s, %s)"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (descricao, valor, tipo))
            new_id = cursor.lastrowid
        conn.commit()

    print(f"INSERT realizado com sucesso. ID criado: {new_id}")


def list_transactions():
    sql = "SELECT id, descricao, valor, tipo, criado_em FROM transacoes ORDER BY id"
    with get_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

    if not rows:
        print("Nenhuma transacao cadastrada.")
        return

    print("\nID | DESCRICAO | VALOR | TIPO | CRIADO EM")
    print("-" * 72)
    for row in rows:
        print(
            f"{row['id']} | {row['descricao']} | "
            f"R$ {row['valor']} | {row['tipo']} | {row['criado_em']}"
        )


def update_transaction():
    transaction_id = read_int("ID da transacao para UPDATE: ")
    descricao = input("Nova descricao: ").strip()
    valor = read_decimal("Novo valor: ")
    tipo = read_type()

    sql = """
    UPDATE transacoes
       SET descricao = %s,
           valor = %s,
           tipo = %s
     WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (descricao, valor, tipo, transaction_id))
            affected_rows = cursor.rowcount
        conn.commit()

    if affected_rows == 0:
        print("Nenhuma linha alterada. Verifique se o ID existe.")
    else:
        print("UPDATE realizado com sucesso.")


def delete_transaction():
    transaction_id = read_int("ID da transacao para DELETE: ")

    sql = "DELETE FROM transacoes WHERE id = %s"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (transaction_id,))
            affected_rows = cursor.rowcount
        conn.commit()

    if affected_rows == 0:
        print("Nenhuma linha removida. Verifique se o ID existe.")
    else:
        print("DELETE realizado com sucesso.")


def read_int(message):
    while True:
        try:
            return int(input(message).strip())
        except ValueError:
            print("Digite um numero inteiro valido.")


def read_decimal(message):
    while True:
        try:
            value = Decimal(input(message).replace(",", ".").strip())
            if value <= 0:
                print("Digite um valor maior que zero.")
                continue
            return value
        except InvalidOperation:
            print("Digite um valor decimal valido. Exemplo: 150.75")


def read_type():
    while True:
        tipo = input("Tipo [ENTRADA/SAIDA]: ").strip().upper()
        if tipo in ("ENTRADA", "SAIDA"):
            return tipo
        print("Tipo invalido. Use ENTRADA ou SAIDA.")


def show_menu():
    print("\n==== CRUD DimDim - RM 564928 ====")
    print("1 - INSERT: criar transacao")
    print("2 - SELECT: listar transacoes")
    print("3 - UPDATE: atualizar transacao")
    print("4 - DELETE: remover transacao")
    print("0 - Sair")


def main():
    try:
        create_table()
    except Error as error:
        print("Erro ao conectar/criar tabela no MySQL.")
        print(f"Detalhe: {error}")
        print("Confira se o container db_564928 esta rodando e se os exports estao corretos.")
        sys.exit(1)

    while True:
        show_menu()
        option = input("Escolha: ").strip()

        try:
            if option == "1":
                create_transaction()
            elif option == "2":
                list_transactions()
            elif option == "3":
                update_transaction()
            elif option == "4":
                delete_transaction()
            elif option == "0":
                print("Encerrando aplicacao.")
                break
            else:
                print("Opcao invalida.")
        except Error as error:
            print(f"Erro no banco de dados: {error}")


if __name__ == "__main__":
    main()

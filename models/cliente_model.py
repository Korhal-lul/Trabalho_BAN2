from config.database import get_connection

class ClienteModel:

    @staticmethod
    def listar():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_cliente,
                   telefone,
                   email,
                   tipo_cliente
            FROM trabalho.cliente
            ORDER BY id_cliente
        """)

        dados = cur.fetchall()

        cur.close()
        conn.close()

        return dados

    @staticmethod
    def inserir(telefone, email, tipo_cliente, id_endereco):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO trabalho.cliente
            (telefone,email,tipo_cliente,id_endereco)
            VALUES (%s,%s,%s,%s)
        """, (telefone,email,tipo_cliente,id_endereco))

        conn.commit()

        cur.close()
        conn.close()
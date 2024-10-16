import logging
import psycopg2
from psycopg2 import sql

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs.log'),
        logging.StreamHandler()  
    ]
)

def create_connection(host, port, user, password):
    logging.info("Conectando ao banco de dados...")
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname='postgres')
    conn.autocommit = True

    cur = conn.cursor()
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("AtividadeBolsaFamilia")))
        cur.close()
        conn.close()
    except Exception as e:
        pass

def create_table(host, port, user, password):
    logging.info("Criando tabela no banco de dados...")
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname="AtividadeBolsaFamilia")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""
CREATE TABLE IF NOT EXISTS beneficiarios (
    id SERIAL PRIMARY KEY,
    mes_competencia VARCHAR(6),
    mes_referencia VARCHAR(6),
    uf VARCHAR(2),
    codigo_municipio_siafi VARCHAR(4),
    nome_municipio VARCHAR(100),
    cpf_favorecido VARCHAR(14),
    nis_favorecido VARCHAR(11),
    nome_favorecido VARCHAR(100),
    valor_parcela DECIMAL(10, 2)
);
    """)

def insert_data(host, port, user, password, data):
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname="AtividadeBolsaFamilia")
    conn.autocommit = True
    cur = conn.cursor()
    insert_query = """
            INSERT INTO beneficiarios (mes_competencia, mes_referencia, uf, codigo_municipio_siafi, 
                                       nome_municipio, cpf_favorecido, nis_favorecido, nome_favorecido, 
                                       valor_parcela)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    cur.execute(insert_query, data)
    cur.close()
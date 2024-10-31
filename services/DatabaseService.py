import os
import psycopg
from psycopg import sql




class DatabaseService:
    
    def __init__(self, host, port, user, password, logger):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.logger = logger
        
    def create_connection(self):
        try:    
            self.logger.info("Conectando ao banco de dados...")
            conn = psycopg.connect(host=self.host, port=self.post, user=self.user, password=self.password, dbname='postgres')
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("AtividadeBolsaFamilia")))
            cur.close()
            conn.close()
        except Exception as e:
            pass

    def create_table(self):
        self.logger.info("Criando tabela no banco de dados...")
        conn = psycopg.connect(host=self.host, port=self.port, user=self.user, password=self.password, dbname="AtividadeBolsaFamilia")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS beneficiarios (
        id SERIAL PRIMARY KEY,
        mes_competencia VARCHAR(6),
        mes_referencia VARCHAR(6),
        uf VARCHAR(2),
        codigo_municipio_siafi VARCHAR(15),
        nome_municipio VARCHAR(100),
        cpf_favorecido VARCHAR(14),
        nis_favorecido VARCHAR(11),
        nome_favorecido VARCHAR(100),
        valor_parcela DECIMAL(10, 2)
    );
        """)

    def get_data_ready(self, file):
        tmp = 'tmp.csv'
        try:
            with open(file, "r") as infile, open(tmp, "w") as outfile:

                header = infile.readline() 
                outfile.write(header)
                cnt = 0
                for line in infile:
                    columns = line.strip().split(";")
                    columns[-1] = columns[-1].replace(",", ".")
                    outfile.write(";".join(columns) + "\n")
                    cnt += 1
                    if cnt % 100000 == 0:
                        self.logger.info(f"Tratamento inicial: {cnt}")
            self.logger.info("Tratamento inicial finalizado!")
            self.logger.warning("Removendo arquivo original...")
            os.remove(file)
            return tmp
        except Exception as e:
            self.logger.error(f"Erro ao tratar arquivo: {e}")
            return

    def insert_data(self):
        try:
            conn = psycopg.connect(host=self.host, port=self.port, user=self.user, password=self.password, dbname="AtividadeBolsaFamilia")
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {e}")
            return
        cur = conn.cursor()
        try:
            with open("tmp.csv") as f:
                with cur.copy(sql.SQL('COPY {} (mes_competencia, mes_referencia, uf, codigo_municipio_siafi, nome_municipio, cpf_favorecido, nis_favorecido, nome_favorecido, valor_parcela) FROM STDIN WITH (FORMAT CSV, HEADER, DELIMITER \';\')').format(sql.Identifier('beneficiarios'))) as copy:
                    cnt = 0
                    for line in f:
                        copy.write(line)
                        cnt += 1
                        if cnt % 100000 == 0:
                            self.logger.info(f"Inserção: {cnt}")
            conn.commit()
            cur.close()
            self.logger.info("Inserção finalizada!")
            self.logger.warning("Removendo arquivo temporário...")
            os.remove("tmp.csv")
            return cnt
        except Exception as e:
            self.logger.error(f"Erro ao inserir dados: {e}")
            return
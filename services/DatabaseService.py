import os
import time
import psycopg
from psycopg import sql

from static.Constants import selects_dict



class DatabaseService:
    
    def __init__(self, host, port, user, password, logger):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.logger = logger
        self.conn = self.connect_database()
    

    def connect_database(self):
        self.logger.info("Conectando ao banco de dados...")
        try:
            conn = psycopg.connect(host=self.host, port=self.port, user=self.user, password=self.password, dbname="postgres")
            conn.autocommit = True
            self.logger.info("Conexão realizada com sucesso!")
            return conn
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao banco de dados, verifique suas credenciais: {e}")

    def create_database(self):
        try:
            cur = self.conn.cursor()
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("AtividadeBolsaFamilia")))
            cur.close()
        except Exception as e:
            self.logger.error(f"Erro ao criar banco de dados: {e}")
            return
        
    def create_table(self):
        try:	
            self.logger.info("Criando tabela no banco de dados...")
            
            cur = self.conn.cursor()
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
            cur.close()
        except Exception as e:
            self.logger.error(f"Erro ao criar tabela: {e}")
            return


    def insert_data(self,):
        cur = self.conn.cursor()
        self.logger.info("Inserindo dados...")
        try:
            with open("tmp.csv") as f:
                with cur.copy(sql.SQL('COPY {} (mes_competencia, mes_referencia, uf, codigo_municipio_siafi, nome_municipio, cpf_favorecido, nis_favorecido, nome_favorecido, valor_parcela) FROM STDIN WITH (FORMAT CSV, HEADER, DELIMITER \';\')').format(sql.Identifier('beneficiarios'))) as copy:
                    cnt = 0
                    for line in f:
                        copy.write(line)
                        cnt += 1
                        if cnt % 100000 == 0:
                            self.logger.info(f"Dados inseridos: {cnt}")
            cur.close()
            self.logger.info("Inserção finalizada!")
            self.logger.warning("Removendo arquivo temporário...")
            os.remove("tmp.csv")
            return cnt
        except Exception as e:
            self.logger.error(f"Erro ao inserir dados: {e}")
            return
        
    def selects_with_times(self):
        cur = self.conn.cursor()
        self.logger.info("Realizando Selects..")
        allResults = []
        try:
            for desc, select in selects_dict.items():
                result = []
                self.logger.info(f"Realizando Select: {desc}")
                start = time.time()
                cur.execute(select)
                end = time.time()
                rows = cur.fetchall()
                labels =  [desc[0] for desc in cur.description] 
                
                self.logger.info(f"Tempo: {end - start}")
                result.append(desc) #0 Descricao
                result.append(select) #1 Select
                result.append(end - start) #2 Tempo
                result.append(len(rows)) #3 Quantidade de registros
                result.append(labels) #4 Labels
                result.append(rows) #5 Registros
                allResults.append(result) 
            cur.close()
            self.logger.info("Selects finalizados!")
            return allResults

        except Exception as e:
            self.logger.error(f"Erro ao selecionar dados: {e}")
            return
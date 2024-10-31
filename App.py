from services.ScrapperService import ScrapperService
from services.DatabaseService import DatabaseService
import services.LoggerService as LoggerService

import time

#Feito por: EzioPP
def main():
    logger = LoggerService.get_logger()
    logger.warning("\n\nPor algum motivo alguns arquivos sao baixado com nome diferente\nQualquer coisa so me chamar\n\n")
    try:
        selectOnly = input("Deseja apenas fazer os selects? (s/n): ")
        if selectOnly == 's':
            selectOnly = True
        else:
            selectOnly = False
            month = int(input("OBRIGATORIO!\nDigite o mês\nTipo 1,2,3,4...: "))
            year = int(input("OBRIGATORIO!\nDigite o ano\nTipo 2020,2021,2022...: "))
        port = int(input("OBRIGATORIO!\nDigite a porta do banco de dados\nTipo 5432: ") or 5432)
        user = input("Digite o nome do usuário\nTipo postgres: ") or 'postgres'
        password = input("Digite a senha do usuário\nTipo 123456: ") or '123456'
        
    except Exception as e:
        logger.error("Erro ao ler os dados de entrada: ", e)
        return
    if selectOnly:
        databaseService = DatabaseService("localhost", port, user, password, logger)
        databaseService.selects_with_times()
        return
    scrapperService = ScrapperService(logger)
    startDownloadTime = time.time()
    file_name = scrapperService.get_data(month, year)
    endDownloadTime = time.time()
    csv_file = scrapperService.extract_data(file_name)
    endExtractTime = time.time()
    databaseService = DatabaseService("localhost", port, user, password, logger)
    databaseService.create_database()
    databaseService.create_table()
    endDatabaseTime = time.time()
    databaseService.get_data_ready(csv_file)
    endPrepareTime = time.time()
    total = databaseService.insert_data()
    endInsertTime = time.time()
    logger.info("Fim da execução!!!")
    logger.info(f"Tempo de download: {endDownloadTime - startDownloadTime}")
    logger.info(f"Tempo de extração: {endExtractTime - endDownloadTime}")
    logger.info(f"Tempo de criação do banco de dados: {endDatabaseTime - endExtractTime}")
    logger.info(f"Tempo de preparação dos dados: {endPrepareTime - endDatabaseTime}")
    logger.info(f"Tempo de inserção dos dados: {endInsertTime - endPrepareTime}")
    logger.info(f"Tempo total: {endInsertTime - startDownloadTime}")
    logger.info(f"Total de registros inseridos: {total}")
    


if __name__ == "__main__":
    main()
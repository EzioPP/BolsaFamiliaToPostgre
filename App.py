import logging
import os #NOTE: quebra no linux, fds ngm usa
import pandas as pd
import ScrapperService
import DatabaseService
#Feito por: EzioPP
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs.log'),
        logging.StreamHandler()  
    ]
)
def main():

    month = int(input("OBRIGATORIO!\nDigite o mês\nTipo 1,2,3,4...: "))
    year = int(input("OBRIGATORIO!\nDigite o ano\nTipo 2020,2021,2022...: "))
    port = int(input("OBRIGATORIO!\nDigite a porta do banco de dados\nTipo 5432: ") or 5432)
    user = input("Digite o nome do usuário\nTipo postgres: ") or 'postgres'
    password = input("Digite a senha do usuário\nTipo 123456: ") or '123456'
    file_name = ScrapperService.get_data(month, year)
    csv_file = ScrapperService.extract_data(file_name)
    logging.info(f"Lendo arquivo {csv_file}, Isso pode demorar um pouco...")
    data = pd.read_csv(csv_file, sep=";", encoding="ISO-8859-1")
    logging.info(f"Arquivo {csv_file} lido com sucesso!")
    logging.info("Limpando...")
    os.remove(csv_file)
    logging.info("Arquivo csv removido!")
    DatabaseService.create_connection("localhost", port, user, password)
    DatabaseService.create_table("localhost", port, user, password)
    counter = 0
    errorB = False
    for index, row in data.iterrows():
        try:
            new_value = row['VALOR PARCELA']
            new_value = float(new_value.replace('.', '').replace(',', '.'))

            new_NIS = row['NIS FAVORECIDO']

            if type(new_NIS) == float or type(new_NIS) == int: #NOTE: n sei, nem quero saber o pq do panda ver o nis como float
                new_NIS = str(int(new_NIS))
            else:
                logging.warning(f"NIS inválido: {new_NIS}, linha {index}, {row}")
                errorB = True
    
            row['VALOR PARCELA'] = new_value
            row['NIS FAVORECIDO'] = new_NIS

            

            DatabaseService.insert_data("localhost", port, user, password, row)


            counter += 1
            if counter % 100 == 0:
                logging.info(f"Dados inseridos: {counter}")
        except Exception as e:
            logging.error(f"Erro ao inserir dados: {e}\n{index}\n{row}")
            errorB = True

            continue

    if errorB:
        logging.error("Erro ao inserir dados, isso pode afetar a atividade, verifique o log!!!")    
    
    logging.info(f"Total de dados inseridos: {counter}")
    logging.info("Fim da execução!!!")


if __name__ == "__main__":
    main()
from zipfile import ZipFile
import requests
import logging
import os #NOTE: opcoinal para limpar o arquivo zip dps da extração, tbm quebra no linux
from Constants import months_dict
from Constants import URL

URL = "https://portaldatransparencia.gov.br/download-de-dados/novo-bolsa-familia/"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs.log'),
        logging.StreamHandler()  
    ]
)

def get_data(month, year):

    logging.info(f"Indo Baixar arquivo do mês {month} do ano {year}.")
    year_month = str(year) + str(month).zfill(2)
    url = f"{URL}{year_month}"
    logging.info(f"URL: {url}")



    file_name = f"Pagamentos_{months_dict[month]}_{year}.zip"
    logging.info(f"Baixando arquivo {file_name}.")
    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f"Erro ao baixar arquivo: {response.status_code}")
        return None
        
    with open(file_name, "wb") as file:
        file.write(response.content)

    logging.info("Arquivo baixado com sucesso!")

    return file_name



def extract_data(zip_file):
    try:
        logging.info(f"Indo extrair arquivo {zip_file}.")
        with ZipFile(zip_file, 'r') as zip:
            zip.extractall()
            csv_file = zip.namelist()[0]
        logging.info(f"Arquivo extraído: {csv_file}!")
        logging.info("Limpando...")
        os.remove(zip_file)
        logging.info("Arquivo zip removido!")
        return csv_file
    except Exception as e:
        logging.error(f"Erro ao extrair arquivo: {e}")
        return None
    
    

if __name__ == "__main__":
    file_name = get_data(1, 2022)
    print(extract_data(file_name))
from static.Constants import months_dict
from static.Constants import URL

from zipfile import ZipFile
import requests
import os

class ScrapperService:
    
    def __init__(self, logger):
        self.logger = logger
    
    def get_data(self, month, year):
        self.logger.info(f"Indo Baixar arquivo do mês {month} do ano {year}.")
        year_month = str(year) + str(month).zfill(2)
        urlEnd = f"{URL}{year_month}"
        self.logger.info(f"URL: {urlEnd}")
        file_name = f"Pagamentos_{months_dict[month]}_{year}.zip"
        self.logger.info(f"Baixando arquivo {file_name}.")
        try:
            response = requests.get(urlEnd)
            if response.status_code != 200:
                self.logger.error(f"Erro ao baixar arquivo: {response.status_code}")
                return None            
            with open(file_name, "wb") as file:
                file.write(response.content)
        except Exception as e:
            self.logger.error(f"Erro ao baixar arquivo: {e}")
            return None
        self.logger.info("Arquivo baixado com sucesso!")

        return file_name

    def extract_data(self, zip_file):
        try:
            self.logger.info(f"Indo extrair arquivo {zip_file}.")
            with ZipFile(zip_file, 'r') as zip:
                zip.extractall()
                csv_file = zip.namelist()[0]
            self.logger.info(f"Arquivo extraído: {csv_file}!")
            self.logger.info("Limpando...")
            os.remove(zip_file)
            self.logger.info("Arquivo zip removido!")
            return csv_file
        except Exception as e:
            self.logger.error(f"Erro ao extrair arquivo: {e}")
            return None

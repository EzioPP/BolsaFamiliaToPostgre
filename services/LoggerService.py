import logging

def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger()
    return logger
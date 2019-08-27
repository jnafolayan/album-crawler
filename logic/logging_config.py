import logging


formatter = '[%(asctime)s] %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=formatter,
                    datefmt='%d-%m-%Y %H:%M:%S')

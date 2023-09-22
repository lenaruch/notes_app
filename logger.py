import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="notes_log.log",
    format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
    datefmt='%d-%m-%Y %H:%M:%S',
)
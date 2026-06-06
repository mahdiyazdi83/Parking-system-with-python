import logging
import sys

class Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)5s - %(message)s",
        encoding="UTF-8",
        handlers=[
            logging.FileHandler("loglist.log", encoding="UTF-8"),  # مسیر ساده شد
            logging.StreamHandler(sys.stdout)
        ]
    )

    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    @classmethod
    def info(cls, message):
        logging.info(message)


    @classmethod
    def error(cls, message):
        logging.error(message)
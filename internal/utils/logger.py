import logging
import concurrent.futures

LEVEL = logging.DEBUG

_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
logging.basicConfig(level=LEVEL)
log = logging.getLogger()


class LLLog:

    @staticmethod
    def get_logger(name) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.addHandler(logging.StreamHandler())
        return logger

    @staticmethod
    def info(msg, *args):
        rec = logging.LogRecord()
        _executor.submit(logging.info, rec, args=())

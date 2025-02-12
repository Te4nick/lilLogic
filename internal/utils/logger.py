import logging
import os


class CustomFormatter(logging.Formatter):
    def format(self, record):
        abs_path = record.pathname
        relative_path = os.path.relpath(abs_path, start=os.getcwd())
        record.pathname = relative_path
        return super().format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = CustomFormatter(
    "%(asctime)s %(pathname)s:%(lineno)d %(levelname)s %(message)s"
)
colour_formatter = CustomFormatter(
    "\x1b[32m"
    + "%(asctime)s %(pathname)s:%(lineno)d %(levelname)s"
    + "\x1b[0m"
    + "\x1b[34m"
    + " %(message)s"
    + "\x1b[0m"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(colour_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

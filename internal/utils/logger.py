from loguru import logger
import sys

logger.add(
    sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>"
)

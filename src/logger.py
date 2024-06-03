from logging import getLogger, FileHandler, Formatter, DEBUG

from config import Logger

logger = getLogger()

logger.setLevel(Logger.level)

handler = FileHandler(f".app.log")

timestamp_format = "%Y-%m-%d %H:%M:%S"

formatter = Formatter(
    "%(asctime)s.%(msecs)03d  %(name)s - %(levelname)s - %(message)s",
    datefmt=timestamp_format,
)

handler.setFormatter(formatter)

logger.addHandler(handler)

logger.debug("logger initialized")

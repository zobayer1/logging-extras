import logging.config
import yaml

with open("logging.yaml", "r") as config_file:
    logging.config.dictConfig(yaml.safe_load(config_file.read()))

logger = logging.getLogger("test_logger")

logger.debug("This is a debug log")
logger.info("This is an info log")
logger.warning("This is an warning log")
logger.error("This is an error log")
logger.critical("This is a critical log")

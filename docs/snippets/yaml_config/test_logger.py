import logging
from logging_.config import YAMLConfig

with open("logging.yaml", "r") as config_file:
    YAMLConfig(config_file.read(), silent=True)

# alternatively, you can use
# YAMLConfig.from_file("logging.yaml", silent=True)

logger = logging.getLogger("test_logger")

logger.debug("This is a debug log")
logger.info("This is an info log")
logger.warning("This is an warning log")
logger.error("This is an error log")
logger.critical("This is a critical log")

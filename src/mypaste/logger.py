import logging


LOGGER_NAME = "mypaste"


def config_logger(level: int) -> None:
    """
    Set up the logging configuration.
    """
    logging.basicConfig(level=level)
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)


def get_logger() -> logging.Logger:
    """
    Return the logger for this application. This should be always
    called before logging anything.
    """
    return logging.getLogger(LOGGER_NAME)

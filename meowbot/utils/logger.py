import logging


def setup_logger(name="meowbot", level=logging.INFO):
    """
    Sets up and returns a logger.

    Args:
        name (str): The name of the logger.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        log_file (str): Optional. File to write logs to.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

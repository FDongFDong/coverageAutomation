import logging
import logging.handlers


def CreateLogger(logger_name):
    # Create Logger
    logger = logging.getLogger(logger_name)

    # Check handler exists
    if len(logger.handlers) > 0:
        return logger  # Logger already exists

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('\n[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    # Create Handlers
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)

    logger.addHandler(streamHandler)
    return logger





"""Sets up logging and global variables."""
import os
import logging

from app.config.reader import constants
from concurrent_log_handler import ConcurrentRotatingFileHandler


def setup_logging(app):
    handlers = []

    logfile = os.path.abspath(constants.LOG_FILE)
    rotate_handler = ConcurrentRotatingFileHandler(logfile, 'a', 512 * 1024, 5)
    handlers.append(rotate_handler)

    if constants.LOG_STDERR:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers
    )

    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.info('Setup logging')
    logger.info('CWD: %s', os.getcwd())

    for _ in ['werkzeug']:
        # logging.getLogger(_).setLevel(logging.CRITICAL)
        # logging.getLogger(_).disabled = True
        # logging.getLogger(_).handlers = []
        pass

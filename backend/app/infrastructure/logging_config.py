import logging
import sys
import json
from pythonjsonlogger import jsonlogger


def setup_logging():
    """
    Set up structured logging for the project.
    Logs are output in JSON format for Docker/production compatibility.
    """
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s',
        rename_fields={
            'asctime': 'timestamp',
            'levelname': 'level',
            'name': 'logger',
            'message': 'msg'
        }
    )
    log_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = [log_handler]
    root_logger.propagate = False


# Call setup_logging at import time
setup_logging()

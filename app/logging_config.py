import logging
from datetime import datetime

def configure_logging():
    log_format = (
        "%(asctime)s %(levelname)-5s %(process)d --- [%(threadName)s] "
        "%(name)s : %(message)s"
    )
    logging.Formatter.converter = lambda *args: datetime.utcnow().timetuple()
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format
    )

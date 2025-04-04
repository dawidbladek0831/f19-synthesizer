import time
import logging

logger = logging.getLogger(__name__)

def log_execution_time(message=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            log_message = message or f"{func.__name__} completed"
            logger.debug(f"{log_message} in {elapsed_time:.3f} seconds.")
            return result
        return wrapper
    return decorator

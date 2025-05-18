import asyncio
import functools
import time
import logging
import inspect

def log_execution_time(message=None):
    def decorator(func):
        is_coroutine = asyncio.iscoroutinefunction(func)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            log_message = message or f"{func.__name__} completed"
            module_name = inspect.getmodule(func).__name__
            logging.getLogger(module_name).debug(f"{log_message} in {elapsed_time:.3f} seconds.")
            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            log_message = message or f"{func.__name__} completed"
            module_name = inspect.getmodule(func).__name__
            logging.getLogger(module_name).debug(f"{log_message} in {elapsed_time:.3f} seconds.")
            return result

        return async_wrapper if is_coroutine else sync_wrapper

    return decorator

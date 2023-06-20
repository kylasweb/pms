import functools
from src.logger import init_logger
from sqlalchemy.exc import OperationalError, ProgrammingError , IntegrityError

error_logger = init_logger("error_logger")
def error_handler(view_func):
    @functools.wraps(view_func)
    async def wrapped_method(*args, **kwargs):
        try:
            return await view_func(*args, **kwargs)
        except (OperationalError, ProgrammingError, IntegrityError, AttributeError) as e:
            # Handle specific MySQL errors here
            error_logger.error(str(e))
            pass

    return wrapped_method

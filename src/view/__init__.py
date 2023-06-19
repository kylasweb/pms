import functools

from sqlalchemy.exc import OperationalError, ProgrammingError , IntegrityError


def error_handler(view_func):
    @functools.wraps(view_func)
    async def wrapped_method(*args, **kwargs):
        try:
            return await view_func(*args, **kwargs)
        except (OperationalError, ProgrammingError, IntegrityError) as e:
            # Handle specific MySQL errors here
            pass

    return wrapped_method

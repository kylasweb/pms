import functools

from sqlalchemy.exc import OperationalError


def error_handler(view_func):
    @functools.wraps(view_func)
    async def wrapped_method(*args, **kwargs):
        try:
            return await view_func(*args, **kwargs)
        except OperationalError as e:
            pass

    return wrapped_method

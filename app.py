import logging

from src.logger import init_logger
from src.config import config_instance
from src.main import create_app

app = create_app(config=config_instance())
static_logger = init_logger('static')
static_logger.setLevel(logging.WARNING)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, extra_files=['src', 'templates', 'static'])


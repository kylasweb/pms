from src.config import config_instance
from src.main import create_app

app = create_app(config=config_instance())

if __name__ == "__main__":
    app.run()

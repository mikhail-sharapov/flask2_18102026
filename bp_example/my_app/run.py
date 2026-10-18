import os, sys
sys.path.append(os.path.pardir)
from my_app import create_app
from my_app.config import ProductionConfig, DevelopmentConfig

"""При запуске через flask run настройки берутся из .flaskenv"""

app = create_app()
# print(app.config.get("SECRET_KEY"))

if __name__ == '__main__':
    """Настройки при запуске python run.py, если их прописать"""
    app.run(host="0.0.0.0", port=3333, debug=True)
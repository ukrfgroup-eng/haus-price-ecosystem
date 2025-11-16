"""
MATRIX CORE - Основной пакет нейро-экосистемы строительства.
"""

__version__ = "1.0.0"
__author__ = "Дома-Цены.РФ"
__description__ = "Автономный AI-мозг строительной экосистемы"

from flask import Flask
from .config import Config


def create_app():
    """Фабрика приложений Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализация модулей
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    return app

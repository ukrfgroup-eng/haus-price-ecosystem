import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Базовый конфигурационный класс"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    
    # Настройки внешних API
    UMNIKO_API_KEY = os.getenv('UMNIKO_API_KEY', '')
    TILDA_API_KEY = os.getenv('TILDA_API_KEY', '')
    
    # Настройки бота
    BOT_WEBHOOK_URL = os.getenv('BOT_WEBHOOK_URL', '')
    BOT_TIMEOUT = int(os.getenv('BOT_TIMEOUT', '30'))
    
    # Логирование
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    DATABASE_URL = 'sqlite:///test.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

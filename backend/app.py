"""
MATRIX CORE - Основной модуль нейро-экосистемы строительства.

Центральный мозг системы, обрабатывающий запросы и координирующий работу модулей.
"""

from flask import Flask, request, jsonify
from .config import config
from .routes import api_bp
import logging
import sys

def create_app(config_name='default'):
    """Фабрика создания приложения Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Настройка логирования
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(app.config['LOG_FILE']),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Регистрация blueprint API
    app.register_blueprint(api_bp)
    
    # Базовые маршруты
    @app.route('/')
    def home():
        return jsonify({
            'status': 'success',
            'message': 'MATRIX CORE API работает',
            'version': '1.0.0'
        })
    
    @app.route('/api/v1/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'MATRIX CORE',
            'timestamp': '2024-01-01T00:00:00Z'  # TODO: заменить на текущее время
        })
    
    # Обработчик ошибок
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'message': 'Ресурс не найден'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Внутренняя ошибка сервера'
        }), 500
    
    return app

# Создание приложения для запуска
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )

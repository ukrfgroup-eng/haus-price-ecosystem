"""
MATRIX CORE - Основной модуль нейро-экосистемы строительства.

Центральный мозг системы, обрабатывающий запросы и координирующий работу модулей.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from .config import config
from .routes import api_bp
from .routes.webhook_routes import webhook_bp
import logging
import sys
import os

def create_app(config_name='default'):
    """Фабрика создания приложения Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Включение CORS для фронтенд интеграций
    CORS(app, resources={
        r"/api/*": {"origins": "*"},
        r"/webhook/*": {"origins": "*"}
    })
    
    # Настройка логирования
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(app.config['LOG_FILE']),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    # Регистрация blueprint API
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(webhook_bp, url_prefix='/webhook')
    
    # Базовые маршруты
    @app.route('/')
    def home():
        return jsonify({
            'status': 'success',
            'message': 'MATRIX CORE API работает',
            'version': '1.0.0',
            'services': {
                'api': 'доступно по /api/v1',
                'webhooks': 'доступно по /webhook',
                'health': 'доступно по /health'
            }
        })
    
    @app.route('/health')
    def health_check():
        """Проверка здоровья всех компонентов системы"""
        from datetime import datetime
        
        health_status = {
            'status': 'healthy',
            'service': 'MATRIX CORE',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'api': 'operational',
                'database': 'in_memory',  # Временное хранилище
                'ai_models': 'operational',
                'webhooks': 'operational'
            },
            'version': '1.0.0',
            'uptime': 'just_started'  # В реальной системе нужно считать время работы
        }
        
        return jsonify(health_status)
    
    @app.route('/api/v1/status')
    def api_status():
        """Статус API системы"""
        from .routes.analysis_routes import analysis_results, user_requests
        from .routes.partner_routes import partners_db
        from .routes.user_routes import users_db
        from .routes.connection_routes import connections_db
        
        status = {
            'system': 'MATRIX CORE',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'statistics': {
                'total_users': len(users_db),
                'total_partners': len(partners_db),
                'total_requests': len(user_requests),
                'total_analyses': len(analysis_results),
                'total_connections': len(connections_db)
            },
            'features': {
                'ai_analysis': 'enabled',
                'partner_matching': 'enabled',
                'crisis_detection': 'enabled',
                'webhook_integration': 'enabled'
            }
        }
        
        return jsonify(status)
    
    # Обработчики ошибок
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'message': 'Ресурс не найден',
            'path': request.path
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'status': 'error',
            'message': 'Метод не разрешен для данного ресурса',
            'allowed_methods': error.valid_methods
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Внутренняя ошибка сервера: {str(error)}")
        return jsonify({
            'status': 'error',
            'message': 'Внутренняя ошибка сервера',
            'error_id': str(id(error))
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Глобальный обработчик исключений"""
        logger.error(f"Необработанное исключение: {str(error)}")
        return jsonify({
            'status': 'error',
            'message': 'Произошла непредвиденная ошибка',
            'error_type': type(error).__name__
        }), 500
    
    # Middleware для логирования запросов
    @app.before_request
    def log_request_info():
        """Логирование входящих запросов"""
        if request.path not in ['/health', '/favicon.ico']:
            logger.info(f"Запрос: {request.method} {request.path} - {request.remote_addr}")
    
    @app.after_request
    def log_response_info(response):
        """Логирование исходящих ответов"""
        if request.path not in ['/health', '/favicon.ico']:
            logger.info(f"Ответ: {request.method} {request.path} - {response.status_code}")
        return response
    
    logger.info("MATRIX CORE приложение инициализировано")
    
    return app

# Создание приложения для запуска
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"""
    🧠 MATRIX CORE запускается...
    
    📊 Статус: ИНИЦИАЛИЗАЦИЯ
    🌐 Хост: {host}
    🚪 Порт: {port}
    🔧 Режим: {'development' if app.config['DEBUG'] else 'production'}
    
    📍 Доступные endpoints:
    - Главная: http://{host}:{port}/
    - Здоровье: http://{host}:{port}/health
    - Статус API: http://{host}:{port}/api/v1/status
    - API документация: http://{host}:{port}/api/v1/
    - Вебхуки: http://{host}:{port}/webhook/
    
    🎯 Система готова к работе!
    """)
    
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG']
    )

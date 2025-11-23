
"""
Минимальное приложение MATRIX CORE для тестирования
"""

from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Загрузка конфигурации
    app.config.from_object(config[config_name])
    
    # Включение CORS
    CORS(app)
    
    @app.route('/')
    def home():
        return jsonify({
            "status": "success", 
            "message": "MATRIX CORE API",
            "version": "1.0.0"
        })
    
    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy", 
            "timestamp": "2024-01-01T00:00:00Z",
            "system": "MATRIX CORE"
        })
    
    @app.route('/api/v1/status')
    def api_status():
        return jsonify({
            "system": "MATRIX CORE", 
            "version": "1.0.0",
            "status": "operational",
            "endpoints": {
                "health": "/health",
                "status": "/api/v1/status"
            }
        })
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
# Добавь этот импорт после существующих импортов
try:
    from backend.routes.demo_routes import demo_bp as demo_routes_bp
    app.register_blueprint(demo_bp, url_prefix='/api/v1')
except ImportError:
    print("⚠️  Demo routes не загружены (возможно файл отсутствует)")
# Добавь этот код после существующих маршрутов, перед созданием app

try:
    from backend.routes.demo_routes import demo_bp
    app.register_blueprint(demo_bp, url_prefix='/api/v1')
    print("✅ Demo routes зарегистрированы")
except ImportError as e:
    print(f"⚠️  Demo routes не загружены: {e}")

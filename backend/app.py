"""
Минимальное приложение MATRIX CORE для тестирования
"""

from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return jsonify({"status": "success", "message": "MATRIX CORE API"})
    
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"})
    
    @app.route('/api/v1/status')
    def api_status():
        return jsonify({
            "system": "MATRIX CORE", 
            "version": "1.0.0",
            "status": "operational"
        })
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

"""
Модуль маршрутов API MATRIX CORE.

Определяет все API endpoint-ы системы.
"""

from flask import Blueprint

# Создаем основной Blueprint для API
api_bp = Blueprint('api', __name__)

# Импортируем все маршруты
from . import analysis_routes
from . import partner_routes  
from . import user_routes
from . import connection_routes

# Регистрируем модули маршрутов
from .analysis_routes import analysis_bp
from .partner_routes import partner_bp
from .user_routes import user_bp
from .connection_routes import connection_bp

api_bp.register_blueprint(analysis_bp, url_prefix='/analyze')
api_bp.register_blueprint(partner_bp, url_prefix='/partners')
api_bp.register_blueprint(user_bp, url_prefix='/users') 
api_bp.register_blueprint(connection_bp, url_prefix='/connect')

__all__ = ['api_bp']

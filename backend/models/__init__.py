"""
Модуль моделей данных MATRIX CORE.

Содержит модели пользователей, запросов, партнеров и соединений.
"""

from .user_models import User, UserRequest
from .partner_models import Partner, Connection
from .analysis_models import AnalysisResult, Recommendation

__all__ = [
    'User',
    'UserRequest', 
    'Partner',
    'Connection',
    'AnalysisResult',
    'Recommendation'
]

"""
Файл для обратной совместимости - редирект на правильный путь к моделям
"""

from backend.models.user_models import User, UserRequest, UserProfile

__all__ = ['User', 'UserRequest', 'UserProfile']

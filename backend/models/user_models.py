"""
Модели пользователей для MATRIX CORE
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid

class User:
    """Базовая модель пользователя"""
    
    def __init__(self, user_id: str = None, user_type: str = None, email: str = None, created_at: str = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.user_type = user_type  # 'customer', 'contractor', 'producer'
        self.email = email
        self.created_at = created_at or datetime.now().isoformat()
        self.profile_data = {}
        self.verification_status = "pending"
        self.is_active = True
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'user_type': self.user_type,
            'email': self.email,
            'created_at': self.created_at,
            'profile_data': self.profile_data,
            'verification_status': self.verification_status,
            'is_active': self.is_active
        }

class UserRequest:
    """Модель пользовательского запроса"""
    
    def __init__(self, request_id: str = None, user_id: str = None, request_type: str = None, request_data: Dict = None):
        self.request_id = request_id or str(uuid.uuid4())
        self.user_id = user_id
        self.request_type = request_type
        self.request_data = request_data or {}
        self.created_at = datetime.now().isoformat()
        self.status = 'pending'

class UserProfile:
    """Расширенный профиль пользователя"""
    
    def __init__(self, user_id: str = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.region = ""
        self.specialization = ""
        self.budget_range = ""
        self.timeline = ""

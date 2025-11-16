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
        self.verification_status = "pending"  # pending, verified, rejected
        self.is_active = True
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            'user_id': self.user_id,
            'user_type': self.user_type,
            'email': self.email,
            'created_at': self.created_at,
            'profile_data': self.profile_data,
            'verification_status': self.verification_status,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Создание из словаря"""
        user = cls(
            user_id=data.get('user_id'),
            user_type=data.get('user_type'),
            email=data.get('email'),
            created_at=data.get('created_at')
        )
        user.profile_data = data.get('profile_data', {})
        user.verification_status = data.get('verification_status', 'pending')
        user.is_active = data.get('is_active', True)
        return user

class UserRequest:
    """Модель пользовательского запроса"""
    
    def __init__(self, request_id: str = None, user_id: str = None, request_type: str = None, request_data: Dict = None):
        self.request_id = request_id or str(uuid.uuid4())
        self.user_id = user_id
        self.request_type = request_type  # 'partner_search', 'info_query', 'connection_request'
        self.request_data = request_data or {}
        self.created_at = datetime.now().isoformat()
        self.status = 'pending'  # 'pending', 'processing', 'completed', 'failed'
        self.matched_partners = []  # Список подобранных партнеров
        self.response_data = {}     # Данные ответа пользователю
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            'request_id': self.request_id,
            'user_id': self.user_id,
            'request_type': self.request_type,
            'request_data': self.request_data,
            'created_at': self.created_at,
            'status': self.status,
            'matched_partners': self.matched_partners,
            'response_data': self.response_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserRequest':
        """Создание из словаря"""
        request = cls(
            request_id=data.get('request_id'),
            user_id=data.get('user_id'),
            request_type=data.get('request_type'),
            request_data=data.get('request_data', {})
        )
        request.created_at = data.get('created_at', request.created_at)
        request.status = data.get('status', 'pending')
        request.matched_partners = data.get('matched_partners', [])
        request.response_data = data.get('response_data', {})
        return request

class UserProfile:
    """Расширенный профиль пользователя"""
    
    def __init__(self, user_id: str = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.region = ""
        self.specialization = ""
        self.budget_range = ""
        self.timeline = ""
        self.preferences = {}
        self.interaction_history = []
        self.crisis_indicators = {  # Показатели для кризисного подбора
            'urgency_level': 0,     # 0-10
            'available_capacity': 100,
            'flexible_pricing': False,
            'special_conditions': []
        }
    
    def update_from_request(self, request_data: Dict):
        """Обновление профиля на основе запроса"""
        if 'region' in request_data:
            self.region = request_data['region']
        if 'specialization' in request_data:
            self.specialization = request_data['specialization']
        if 'budget_range' in request_data:
            self.budget_range = request_data['budget_range']
        if 'timeline' in request_data:
            self.timeline = request_data['timeline']
        
        # Обновление кризисных показателей
        if 'urgency_level' in request_data:
            self.crisis_indicators['urgency_level'] = request_data['urgency_level']
        if 'available_capacity' in request_data:
            self.crisis_indicators['available_capacity'] = request_data['available_capacity']
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            'user_id': self.user_id,
            'region': self.region,
            'specialization': self.specialization,
            'budget_range': self.budget_range,
            'timeline': self.timeline,
            'preferences': self.preferences,
            'interaction_history': self.interaction_history,
            'crisis_indicators': self.crisis_indicators
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        """Создание из словарь"""
        profile = cls(user_id=data.get('user_id'))
        profile.region = data.get('region', '')
        profile.specialization = data.get('specialization', '')
        profile.budget_range = data.get('budget_range', '')
        profile.timeline = data.get('timeline', '')
        profile.preferences = data.get('preferences', {})
        profile.interaction_history = data.get('interaction_history', [])
        profile.crisis_indicators = data.get('crisis_indicators', {
            'urgency_level': 0,
            'available_capacity': 100,
            'flexible_pricing': False,
            'special_conditions': []
        })
        return profile

"""
Модели анализа и рекомендаций для MATRIX CORE
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid

class AnalysisResult:
    """Результат анализа пользовательского запроса"""
    
    def __init__(self, analysis_id: str = None, request_id: str = None, user_id: str = None):
        self.analysis_id = analysis_id or str(uuid.uuid4())
        self.request_id = request_id
        self.user_id = user_id
        self.intent = ""           # Определенное намерение пользователя
        self.confidence = 0.0      # Уверенность в определении намерения (0-1)
        self.entities = {}         # Извлеченные сущности (регион, бюджет и т.д.)
        self.relevant_partners = []  # Список подходящих партнеров с оценками
        self.recommendations = []    # Рекомендации для пользователя
        self.alternative_suggestions = []  # Альтернативные варианты
        self.crisis_match_score = 0.0  # Оценка соответствия кризисным показателям
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            'analysis_id': self.analysis_id,
            'request_id': self.request_id,
            'user_id': self.user_id,
            'intent': self.intent,
            'confidence': self.confidence,
            'entities': self.entities,
            'relevant_partners': self.relevant_partners,
            'recommendations': self.recommendations,
            'alternative_suggestions': self.alternative_suggestions,
            'crisis_match_score': self.crisis_match_score,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AnalysisResult':
        """Создание из словаря"""
        analysis = cls(
            analysis_id=data.get('analysis_id'),
            request_id=data.get('request_id'),
            user_id=data.get('user_id')
        )
        analysis.intent = data.get('intent', '')
        analysis.confidence = data.get('confidence', 0.0)
        analysis.entities = data.get('entities', {})
        analysis.relevant_partners = data.get('relevant_partners', [])
        analysis.recommendations = data.get('recommendations', [])
        analysis.alternative_suggestions = data.get('alternative_suggestions', [])
        analysis.crisis_match_score = data.get('crisis_match_score', 0.0)
        analysis.created_at = data.get('created_at', analysis.created_at)
        return analysis

class Recommendation:
    """Модель рекомендации для пользователя"""
    
    def __init__(self, recommendation_id: str = None, user_id: str = None, partner_id: str = None):
        self.recommendation_id = recommendation_id or str(uuid.uuid4())
        self.user_id = user_id
        self.partner_id = partner_id
        self.reason = ""           # Почему рекомендован этот партнер
        self.match_score = 0.0     # Оценка соответствия (0-1)
        self.crisis_boost = 0.0    # Бонус за кризисное соответствие
        self.priority = 0          # Приоритет показа (чем выше, тем раньше покажем)
        self.category = ""         # Категория рекомендации
        self.displayed = False     # Была ли показана пользователю
        self.accepted = False      # Принял ли пользователь рекомендацию
        self.feedback = ""         # Отзыв пользователя о рекомендации
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            'recommendation_id': self.recommendation_id,
            'user_id': self.user_id,
            'partner_id': self.partner_id,
            'reason': self.reason,
            'match_score': self.match_score,
            'crisis_boost': self.crisis_boost,
            'priority': self.priority,
            'category': self.category,
            'displayed': self.displayed,
            'accepted': self.accepted,
            'feedback': self.feedback,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Recommendation':
        """Создание из словаря"""
        recommendation = cls(
            recommendation_id=data.get('recommendation_id'),
            user_id=data.get('user_id'),
            partner_id=data.get('partner_id')
        )
        recommendation.reason = data.get('reason', '')
        recommendation.match_score = data.get('match_score', 0.0)
        recommendation.crisis_boost = data.get('crisis_boost', 0.0)
        recommendation.priority = data.get('priority', 0)
        recommendation.category = data.get('category', '')
        recommendation.displayed = data.get('displayed', False)
        recommendation.accepted = data.get('accepted', False)
        recommendation.feedback = data.get('feedback', '')
        recommendation.created_at = data.get('created_at', recommendation.created_at)
        return recommendation

class CrisisMatch:
    """Модель для кризисного подбора партнеров"""
    
    def __init__(self, match_id: str = None):
        self.match_id = match_id or str(uuid.uuid4())
        self.customer_id = ""
        self.partner_id = ""
        self.urgency_match = 0.0    # Совпадение по срочности
        self.capacity_match = 0.0   # Совпадение по мощностям
        self.geo_match = 0.0        # Географическое совпадение
        self.specialization_match = 0.0  # Совпадение по специализации
        self.price_match = 0.0      # Совпадение по бюджету
        self.total_score = 0.0      # Общая оценка
        self.recommendation_priority = 0  # Приоритет рекомендации
        self.created_at = datetime.now().isoformat()
    
    def calculate_total_score(self):
        """Расчет общей оценки совпадения"""
        weights = {
            'urgency': 0.3,
            'capacity': 0.25,
            'specialization': 0.2,
            'geo': 0.15,
            'price': 0.1
        }
        
        self.total_score = (
            self.urgency_match * weights['urgency'] +
            self.capacity_match * weights['capacity'] +
            self.specialization_match * weights['specialization'] +
            self.geo_match * weights['geo'] +
            self.price_match * weights['price']
        )
        
        # Установка приоритета на основе общей оценки
        if self.total_score >= 0.8:
            self.recommendation_priority = 3  # Высокий
        elif self.total_score >= 0.6:
            self.recommendation_priority = 2  # Средний
        else:
            self.recommendation_priority = 1  # Низкий
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            'match_id': self.match_id,
            'customer_id': self.customer_id,
            'partner_id': self.partner_id,
            'urgency_match': self.urgency_match,
            'capacity_match': self.capacity_match,
            'geo_match': self.geo_match,
            'specialization_match': self.specialization_match,
            'price_match': self.price_match,
            'total_score': self.total_score,
            'recommendation_priority': self.recommendation_priority,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CrisisMatch':
        """Создание из словаря"""
        match = cls(match_id=data.get('match_id'))
        match.customer_id = data.get('customer_id', '')
        match.partner_id = data.get('partner_id', '')
        match.urgency_match = data.get('urgency_match', 0.0)
        match.capacity_match = data.get('capacity_match', 0.0)
        match.geo_match = data.get('geo_match', 0.0)
        match.specialization_match = data.get('specialization_match', 0.0)
        match.price_match = data.get('price_match', 0.0)
        match.total_score = data.get('total_score', 0.0)
        match.recommendation_priority = data.get('recommendation_priority', 0)
        match.created_at = data.get('created_at', match.created_at)
        return match

"""
Модели партнеров для MATRIX CORE
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid

class Partner:
    """Модель партнера (подрядчика или производителя)"""
    
    def __init__(self, partner_id: str = None, user_id: str = None, company_name: str = None):
        self.partner_id = partner_id or str(uuid.uuid4())
        self.user_id = user_id
        self.company_name = company_name
        
        # 🏢 О компании
        self.legal_name = ""
        self.tax_id = ""
        self.years_on_market = 0
        self.team_size = ""
        
        # 🎯 Услуги и специализация (КРИТИЧЕСКИ ВАЖНО!)
        self.specializations = []  # ["каркасные дома", "отделка", "кровля"]
        self.services = []         # ["строительство", "проектирование", "ремонт"]
        self.materials_supply = [] # ["кирпич", "бетон", "металлоконструкции"]
        
        # 🗺️ География работы
        self.regions = []          # ["Московская область", "Центральный регион"]
        self.willing_to_travel = False
        self.max_travel_distance = 0
        
        # 💼 Мощности и возможности
        self.production_capacity = ""    # "до 10 объектов в месяц"
        self.warehouse_space = ""        # "1000 м² складов"
        self.current_workload = 0        # 0-100% загрузка
        self.available_capacity = 100    # Свободные мощности для новых заказов
        
        # 📊 Кризисные показатели (для AI-подбора)
        self.urgency_level = 0           # 0-10 (насколько срочно нужны заказы)
        self.min_order_size = 0          # Минимальный объем заказа
        self.flexible_pricing = False    # Готовность к Negotiation
        self.special_offers = []         # Акции для быстрого сбыта
        
        # 🏆 Репутация и доказательства
        self.portfolio = []              # Ссылки на выполненные проекты
        self.certificates = []           # Сертификаты и лицензии
        self.client_reviews = []         # Отзывы клиентов
        self.verification_status = "pending"  # "pending", "verified", "rejected"
        
        # 💰 Условия работы
        self.payment_terms = ""          # "предоплата 30%", "поэтапно"
        self.warranty_period = ""        # "5 лет на конструкции"
        self.contract_types = []         # ["договор подряда", "субподряд"]
        
        # Системные поля
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.is_active = True
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            'partner_id': self.partner_id,
            'user_id': self.user_id,
            'company_name': self.company_name,
            'legal_name': self.legal_name,
            'tax_id': self.tax_id,
            'years_on_market': self.years_on_market,
            'team_size': self.team_size,
            'specializations': self.specializations,
            'services': self.services,
            'materials_supply': self.materials_supply,
            'regions': self.regions,
            'willing_to_travel': self.willing_to_travel,
            'max_travel_distance': self.max_travel_distance,
            'production_capacity': self.production_capacity,
            'warehouse_space': self.warehouse_space,
            'current_workload': self.current_workload,
            'available_capacity': self.available_capacity,
            'urgency_level': self.urgency_level,
            'min_order_size': self.min_order_size,
            'flexible_pricing': self.flexible_pricing,
            'special_offers': self.special_offers,
            'portfolio': self.portfolio,
            'certificates': self.certificates,
            'client_reviews': self.client_reviews,
            'verification_status': self.verification_status,
            'payment_terms': self.payment_terms,
            'warranty_period': self.warranty_period,
            'contract_types': self.contract_types,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Partner':
        """Создание из словаря"""
        partner = cls(
            partner_id=data.get('partner_id'),
            user_id=data.get('user_id'),
            company_name=data.get('company_name')
        )
        
        # Заполняем все поля из данных
        partner.legal_name = data.get('legal_name', '')
        partner.tax_id = data.get('tax_id', '')
        partner.years_on_market = data.get('years_on_market', 0)
        partner.team_size = data.get('team_size', '')
        partner.specializations = data.get('specializations', [])
        partner.services = data.get('services', [])
        partner.materials_supply = data.get('materials_supply', [])
        partner.regions = data.get('regions', [])
        partner.willing_to_travel = data.get('willing_to_travel', False)
        partner.max_travel_distance = data.get('max_travel_distance', 0)
        partner.production_capacity = data.get('production_capacity', '')
        partner.warehouse_space = data.get('warehouse_space', '')
        partner.current_workload = data.get('current_workload', 0)
        partner.available_capacity = data.get('available_capacity', 100)
        partner.urgency_level = data.get('urgency_level', 0)
        partner.min_order_size = data.get('min_order_size', 0)
        partner.flexible_pricing = data.get('flexible_pricing', False)
        partner.special_offers = data.get('special_offers', [])
        partner.portfolio = data.get('portfolio', [])
        partner.certificates = data.get('certificates', [])
        partner.client_reviews = data.get('client_reviews', [])
        partner.verification_status = data.get('verification_status', 'pending')
        partner.payment_terms = data.get('payment_terms', '')
        partner.warranty_period = data.get('warranty_period', '')
        partner.contract_types = data.get('contract_types', [])
        partner.created_at = data.get('created_at', partner.created_at)
        partner.updated_at = data.get('updated_at', partner.updated_at)
        partner.is_active = data.get('is_active', True)
        
        return partner

class Connection:
    """Модель соединения между пользователями"""
    
    def __init__(self, connection_id: str = None, from_user: str = None, to_user: str = None, context: Dict = None):
        self.connection_id = connection_id or str(uuid.uuid4())
        self.from_user = from_user  # Кто инициировал
        self.to_user = to_user      # Кому направили
        self.context = context or {}  # Контекст запроса
        self.status = 'pending'     # 'pending', 'accepted', 'rejected', 'completed'
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.connection_score = 0.0  # Оценка релевантности связи (0-1)
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            'connection_id': self.connection_id,
            'from_user': self.from_user,
            'to_user': self.to_user,
            'context': self.context,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'connection_score': self.connection_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Connection':
        """Создание из словаря"""
        connection = cls(
            connection_id=data.get('connection_id'),
            from_user=data.get('from_user'),
            to_user=data.get('to_user'),
            context=data.get('context', {})
        )
        connection.status = data.get('status', 'pending')
        connection.created_at = data.get('created_at', connection.created_at)
        connection.updated_at = data.get('updated_at', connection.updated_at)
        connection.connection_score = data.get('connection_score', 0.0)
        return connection

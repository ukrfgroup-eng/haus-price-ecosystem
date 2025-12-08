"""
Модели базы данных для экосистемы Дома-Цены.РФ
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Partner(db.Model):
    """Модель партнера (компании/ИП)"""
    
    __tablename__ = 'partners'
    
    # Основные поля
    id = db.Column(db.Integer, primary_key=True)
    partner_code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Статус
    status = db.Column(db.String(20), default='pending')
    registration_stage = db.Column(db.String(50), default='started')
    
    # Юридические данные
    company_name = db.Column(db.String(255), nullable=False)
    legal_form = db.Column(db.String(10))
    inn = db.Column(db.String(12), unique=True, nullable=False)
    ogrn = db.Column(db.String(15))
    legal_address = db.Column(db.Text)
    actual_address = db.Column(db.Text)
    
    # Контактные данные
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    website = db.Column(db.String(255))
    
    # Услуги и специализация
    main_category = db.Column(db.String(50))
    specializations = db.Column(db.JSON)
    regions = db.Column(db.JSON)
    services = db.Column(db.JSON)
    
    # Верификация
    verification_status = db.Column(db.String(20), default='pending')
    verification_date = db.Column(db.DateTime)
    verification_data = db.Column(db.JSON)
    verification_method = db.Column(db.String(50))
    
    # Документы
    documents = db.Column(db.JSON)
    
    # Для связи с ботами
    telegram_user_id = db.Column(db.String(50))
    telegram_username = db.Column(db.String(100))
    telegram_chat_id = db.Column(db.String(50))
    registration_source = db.Column(db.String(50))
    
    # Подписка и монетизация
    subscription_plan = db.Column(db.String(20), default='trial')
    subscription_expires = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'partner_code': self.partner_code,
            'company_name': self.company_name,
            'legal_form': self.legal_form,
            'inn': self.inn,
            'status': self.status,
            'phone': self.phone,
            'email': self.email,
            'verification_status': self.verification_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'registration_stage': self.registration_stage
        }


class VerificationLog(db.Model):
    """Лог верификационных запросов"""
    
    __tablename__ = 'verification_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partners.id'))
    inn = db.Column(db.String(12))
    request_type = db.Column(db.String(50))
    request_data = db.Column(db.JSON)
    response_data = db.Column(db.JSON)
    status = db.Column(db.String(20))
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BotConversation(db.Model):
    """История диалогов с ботами"""
    
    __tablename__ = 'bot_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    bot_id = db.Column(db.String(50))
    platform = db.Column(db.String(20))
    conversation_data = db.Column(db.JSON)
    current_step = db.Column(db.String(50))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

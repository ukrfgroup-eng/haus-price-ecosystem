"""
Маршруты для вебхуков внешних систем MATRIX CORE

Интеграция с Umniko ботами, Tilda и другими платформами.
"""

from flask import Blueprint, request, jsonify
import logging
import json

from ..utils.webhook_helpers import process_webhook, verify_signature
from ..utils.data_helpers import format_response

# Создаем Blueprint для вебхуков
webhook_bp = Blueprint('webhooks', __name__)
logger = logging.getLogger(__name__)

@webhook_bp.route('/umniko', methods=['POST'])
def umniko_webhook():
    """
    Вебхук для интеграции с Umniko ботами
    
    Ожидаемый формат от Umniko:
    {
        "user_id": "user_123",
        "message": "Ищу строителя дома в Москве",
        "user_data": {
            "user_type": "customer",
            "region": "Московская область"
        },
        "session_id": "session_456",
        "timestamp": "2024-01-01T12:00:00Z"
    }
    """
    try:
        # Проверка подписи (в продакшене)
        # if not verify_signature(request.headers, request.get_data(), 'your-secret'):
        #     return jsonify(format_response(
        #         message='Неверная подпись вебхука',
        #         status='error'
        #     )), 401
        
        data = request.get_json()
        
        if not data:
            return jsonify(format_response(
                message='Отсутствуют данные в запросе',
                status='error'
            )), 400
        
        logger.info(f"Вебхук от Umniko: пользователь {data.get('user_id', 'unknown')}")
        
        # Обработка вебхука
        result = process_webhook(data)
        
        if result.get('status') == 'error':
            return jsonify(format_response(
                message=result.get('message', 'Ошибка обработки вебхука'),
                status='error'
            )), 400
        
        logger.info(f"Вебхук обработан успешно. Ответов: {len(result.get('messages', []))}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука Umniko: {str(e)}")
        return jsonify(format_response(
            message=f'Внутренняя ошибка обработки вебхука: {str(e)}',
            status='error'
        )), 500

@webhook_bp.route('/tilda', methods=['POST'])
def tilda_webhook():
    """
    Вебхук для интеграции с Tilda (формы регистрации)
    
    Ожидаемый формат от Tilda:
    {
        "form_id": "partner_registration",
        "fields": {
            "company_name": "Тестовая компания",
            "email": "test@example.com",
            "user_type": "contractor",
            "specializations": ["каркасные дома"]
        },
        "page_url": "https://дом-цены.рф/partner-registration"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify(format_response(
                message='Отсутствуют данные в запросе',
                status='error'
            )), 400
        
        form_id = data.get('form_id', 'unknown')
        logger.info(f"Вебхук от Tilda: форма {form_id}")
        
        # Обработка разных типов форм
        if form_id == 'partner_registration':
            result = process_partner_registration(data.get('fields', {}))
        elif form_id == 'user_registration':
            result = process_user_registration(data.get('fields', {}))
        else:
            return jsonify(format_response(
                message=f'Неизвестный тип формы: {form_id}',
                status='error'
            )), 400
        
        return jsonify(format_response(
            data=result,
            message='Форма успешно обработана'
        ))
        
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука Tilda: {str(e)}")
        return jsonify(format_response(
            message=f'Ошибка обработки формы: {str(e)}',
            status='error'
        )), 500

@webhook_bp.route('/flexbe', methods=['POST'])
def flexbe_webhook():
    """
    Вебхук для интеграции с Flexbe (главная страница)
    
    Обрабатывает действия пользователей с главной страницы:
    - Нажатие кнопки "Найти подрядчика"
    - Быстрые заявки
    - Подписки на рассылку
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify(format_response(
                message='Отсутствуют данные в запросе',
                status='error'
            )), 400
        
        action = data.get('action', 'unknown')
        logger.info(f"Вебхук от Flexbe: действие {action}")
        
        # Обработка разных действий
        if action == 'quick_search':
            result = process_quick_search(data)
        elif action == 'newsletter_subscription':
            result = process_newsletter_subscription(data)
        elif action == 'contact_request':
            result = process_contact_request(data)
        else:
            return jsonify(format_response(
                message=f'Неизвестное действие: {action}',
                status='error'
            )), 400
        
        return jsonify(format_response(
            data=result,
            message='Действие успешно обработано'
        ))
        
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука Flexbe: {str(e)}")
        return jsonify(format_response(
            message=f'Ошибка обработки действия: {str(e)}',
            status='error'
        )), 500

# Вспомогательные функции для обработки данных

def process_partner_registration(fields: dict) -> dict:
    """Обработка регистрации партнера из Tilda формы"""
    # Здесь будет интеграция с API партнеров
    # Пока возвращаем заглушку
    
    required_fields = ['company_name', 'email', 'user_type']
    missing_fields = [field for field in required_fields if field not in fields]
    
    if missing_fields:
        return {
            'status': 'validation_error',
            'missing_fields': missing_fields
        }
    
    return {
        'status': 'success',
        'next_steps': [
            'Проверка данных компании',
            'Верификация контактной информации', 
            'Активация аккаунта в течение 24 часов'
        ],
        'estimated_time': '1-2 рабочих дня'
    }

def process_user_registration(fields: dict) -> dict:
    """Обработка регистрации пользователя из Tilda формы"""
    required_fields = ['email', 'user_type']
    missing_fields = [field for field in required_fields if field not in fields]
    
    if missing_fields:
        return {
            'status': 'validation_error',
            'missing_fields': missing_fields
        }
    
    return {
        'status': 'success',
        'welcome_message': 'Добро пожаловать в экосистему Дома-Цены.РФ!',
        'immediate_actions': [
            'Создайте первый запрос через бота',
            'Заполните профиль для персонализированных рекомендаций'
        ]
    }

def process_quick_search(data: dict) -> dict:
    """Обработка быстрого поиска с главной страницы"""
    search_params = data.get('params', {})
    
    return {
        'search_id': 'quick_search_123',
        'estimated_results': '50+ партнеров',
        'processing_time': 'менее 60 секунд',
        'next_step': 'переход к боту для уточнения деталей'
    }

def process_newsletter_subscription(data: dict) -> dict:
    """Обработка подписки на рассылку"""
    email = data.get('email', '')
    
    return {
        'status': 'subscribed',
        'email': email,
        'subscription_type': 'industry_news',
        'frequency': 'еженедельно'
    }

def process_contact_request(data: dict) -> dict:
    """Обработка запроса на обратную связь"""
    return {
        'request_id': 'contact_123',
        'response_time': 'в течение 2 часов',
        'contact_method': 'email или телефон'
    }

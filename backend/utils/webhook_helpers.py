"""
Вспомогательные функции для обработки вебхуков
"""

def process_umniko_webhook(data):
    """Обработка вебхука от ProTalk"""
    return {
        "status": "success",
        "message": "Webhook processed",
        "session_id": data.get("session_id", "")
    }

def process_tilda_webhook(data):
    """Обработка вебхука от Tilda"""
    return {
        "status": "success", 
        "message": "Tilda webhook processed"
    }

def process_flexbe_webhook(data):
    """Обработка вебхука от Flexbe"""
    return {
        "status": "success",
        "message": "Flexbe webhook processed"
    }

def validate_webhook_signature(signature, payload):
    """Валидация подписи вебхука"""
    return True  # Заглушка для тестов

def format_bot_response(messages, session_data=None):
    """Форматирование ответа для бота"""
    return {
        "messages": messages,
        "session_data": session_data or {}
    }

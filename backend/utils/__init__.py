"""
Модуль утилит MATRIX CORE.

Содержит вспомогательные функции, хелперы и утилиты для работы системы.
"""

from .ai_helpers import analyze_user_intent, build_response, find_relevant_partners
from .data_helpers import normalize_user_data, validate_request, format_response
from .webhook_helpers import process_webhook, verify_signature

__all__ = [
    'analyze_user_intent',
    'build_response', 
    'find_relevant_partners',
    'normalize_user_data',
    'validate_request',
    'format_response',
    'process_webhook',
    'verify_signature'
]

"""
Маршруты анализа для MATRIX CORE API

Обрабатывает пользовательские запросы, анализирует намерения и подбирает партнеров.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
import logging

# Создаем Blueprint для анализа
analysis_bp = Blueprint('analysis', __name__)
logger = logging.getLogger(__name__)

# Временное хранилище (позже заменим на базу данных)
analysis_results = {}
user_requests = {}

@analysis_bp.route('/request', methods=['POST'])
def analyze_user_request():
    """
    Анализ пользовательского запроса и подбор релевантных партнеров
    
    Пример запроса:
    {
        "user_id": "user_123",
        "user_type": "customer",
        "message": "Ищу строителя каркасного дома в Московской области до 3 млн рублей",
        "user_data": {
            "region": "Московская область",
            "budget_range": "1-3 млн",
            "timeline": "3 месяца"
        }
    }
    """
    try:
        data = request.get_json()
        
        # Валидация входных данных
        if not data or 'message' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Отсутствует текст запроса'
            }), 400
        
        user_id = data.get('user_id', str(uuid.uuid4()))
        user_type = data.get('user_type', 'customer')
        message = data.get('message', '')
        user_data = data.get('user_data', {})
        
        logger.info(f"Анализ запроса от пользователя {user_id}: {message}")
        
        # Анализ намерения пользователя (заглушка - потом заменим на AI)
        intent_analysis = analyze_user_intent(message, user_type)
        
        # Извлечение сущностей из запроса (заглушка)
        entities = extract_entities(message, user_data)
        
        # Подбор релевантных партнеров (заглушка)
        relevant_partners = find_relevant_partners(intent_analysis, entities, user_type)
        
        # Создание результата анализа
        analysis_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())
        
        analysis_result = {
            'analysis_id': analysis_id,
            'request_id': request_id,
            'user_id': user_id,
            'intent': intent_analysis.get('intent', 'unknown'),
            'confidence': intent_analysis.get('confidence', 0.0),
            'entities': entities,
            'relevant_partners': relevant_partners,
            'recommendations': build_recommendations(relevant_partners, intent_analysis),
            'crisis_match_score': calculate_crisis_match(relevant_partners),
            'created_at': datetime.now().isoformat()
        }
        
        # Сохраняем результаты
        analysis_results[analysis_id] = analysis_result
        user_requests[request_id] = {
            'request_id': request_id,
            'user_id': user_id,
            'user_type': user_type,
            'message': message,
            'user_data': user_data,
            'created_at': datetime.now().isoformat()
        }
        
        logger.info(f"Анализ завершен. Найдено партнеров: {len(relevant_partners)}")
        
        return jsonify({
            'status': 'success',
            'analysis_id': analysis_id,
            'request_id': request_id,
            'intent': intent_analysis.get('intent'),
            'confidence': intent_analysis.get('confidence'),
            'relevant_partners_count': len(relevant_partners),
            'recommendations': analysis_result['recommendations'][:3],  # Топ-3 рекомендации
            'crisis_match_score': analysis_result['crisis_match_score']
        })
        
    except Exception as e:
        logger.error(f"Ошибка при анализе запроса: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Внутренняя ошибка сервера: {str(e)}'
        }), 500

@analysis_bp.route('/crisis-match', methods=['POST'])
def crisis_partner_matching():
    """
    Кризисный подбор партнеров на основе срочности и доступных мощностей
    
    Пример запроса:
    {
        "customer_id": "user_123",
        "requirements": {
            "region": "Московская область",
            "specialization": "каркасные дома",
            "budget_range": "1-3 млн",
            "urgency_level": 8
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'customer_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Отсутствует customer_id'
            }), 400
        
        customer_id = data['customer_id']
        requirements = data.get('requirements', {})
        
        logger.info(f"Кризисный подбор для клиента {customer_id}")
        
        # Кризисный подбор партнеров (заглушка)
        crisis_matches = find_crisis_partners(requirements)
        
        return jsonify({
            'status': 'success',
            'customer_id': customer_id,
            'crisis_matches': crisis_matches,
            'total_matches': len(crisis_matches),
            'high_priority_matches': len([m for m in crisis_matches if m.get('priority', 0) >= 3])
        })
        
    except Exception as e:
        logger.error(f"Ошибка при кризисном подборе: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка кризисного подбора: {str(e)}'
        }), 500

@analysis_bp.route('/result/<analysis_id>', methods=['GET'])
def get_analysis_result(analysis_id):
    """Получение результатов анализа по ID"""
    try:
        if analysis_id not in analysis_results:
            return jsonify({
                'status': 'error',
                'message': 'Анализ не найден'
            }), 404
        
        return jsonify({
            'status': 'success',
            'analysis': analysis_results[analysis_id]
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении анализа: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения анализа: {str(e)}'
        }), 500

# Заглушки функций (реализуем позже в utils/ai_helpers.py)

def analyze_user_intent(message: str, user_type: str) -> dict:
    """Анализ намерения пользователя (заглушка)"""
    # Простая логика определения намерения
    intent_keywords = {
        'partner_search': ['ищу', 'нужен', 'найти', 'подрядчик', 'строитель', 'производитель'],
        'info_query': ['сколько', 'стоимость', 'цена', 'информация', 'консультация'],
        'connection_request': ['связаться', 'контакт', 'связь', 'предложение']
    }
    
    message_lower = message.lower()
    detected_intent = 'info_query'
    confidence = 0.5
    
    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in message_lower:
                detected_intent = intent
                confidence = 0.8
                break
    
    return {
        'intent': detected_intent,
        'confidence': confidence,
        'user_type': user_type
    }

def extract_entities(message: str, user_data: dict) -> dict:
    """Извлечение сущностей из запроса (заглушка)"""
    entities = user_data.copy()
    
    # Простое извлечение регионов
    regions = ['москв', 'подмосков', 'санкт-петербург', 'питер', 'казан', 'новосибирск']
    message_lower = message.lower()
    
    for region in regions:
        if region in message_lower:
            entities['region'] = region.capitalize()
            break
    
    # Извлечение бюджетных диапазонов
    budget_indicators = ['тысяч', 'миллион', 'млн', 'рубл']
    for indicator in budget_indicators:
        if indicator in message_lower:
            # Упрощенное извлечение чисел
            entities['budget_mentioned'] = True
            break
    
    return entities

def find_relevant_partners(intent_analysis: dict, entities: dict, user_type: str) -> list:
    """Подбор релевантных партнеров (заглушка)"""
    # Временные данные партнеров (позже заменим на базу)
    sample_partners = [
        {
            'partner_id': 'partner_1',
            'company_name': 'СтройДом Профи',
            'specializations': ['каркасные дома', 'деревянные дома'],
            'regions': ['Московская область'],
            'urgency_level': 7,
            'available_capacity': 80,
            'match_score': 0.85,
            'crisis_boost': 0.3
        },
        {
            'partner_id': 'partner_2', 
            'company_name': 'Московский Строитель',
            'specializations': ['каркасные дома', 'кирпичные дома'],
            'regions': ['Московская область', 'Центральный регион'],
            'urgency_level': 5,
            'available_capacity': 60,
            'match_score': 0.75,
            'crisis_boost': 0.2
        },
        {
            'partner_id': 'partner_3',
            'company_name': 'ЭкоДом',
            'specializations': ['эко-строительство', 'каркасные дома'],
            'regions': ['Московская область'],
            'urgency_level': 9,
            'available_capacity': 95,
            'match_score': 0.65,
            'crisis_boost': 0.4
        }
    ]
    
    # Фильтрация по региону (если указан)
    region = entities.get('region', '')
    if region:
        filtered_partners = [
            p for p in sample_partners 
            if region in p.get('regions', []) or not p.get('regions')
        ]
    else:
        filtered_partners = sample_partners
    
    return filtered_partners

def build_recommendations(partners: list, intent_analysis: dict) -> list:
    """Построение рекомендаций на основе подобранных партнеров"""
    recommendations = []
    
    for partner in partners:
        recommendation = {
            'partner_id': partner['partner_id'],
            'company_name': partner['company_name'],
            'reason': f"Специализация: {', '.join(partner['specializations'][:2])}",
            'match_score': partner['match_score'],
            'crisis_boost': partner.get('crisis_boost', 0),
            'priority': 3 if partner['match_score'] > 0.8 else 2 if partner['match_score'] > 0.6 else 1,
            'urgency_level': partner['urgency_level'],
            'available_capacity': partner['available_capacity']
        }
        recommendations.append(recommendation)
    
    # Сортировка по приоритету и оценке
    recommendations.sort(key=lambda x: (x['priority'], x['match_score']), reverse=True)
    return recommendations

def calculate_crisis_match(partners: list) -> float:
    """Расчет общей оценки кризисного соответствия"""
    if not partners:
        return 0.0
    
    total_score = sum(p['match_score'] for p in partners)
    crisis_boost = sum(p.get('crisis_boost', 0) for p in partners)
    
    return min(1.0, (total_score / len(partners)) + (crisis_boost / len(partners)))

def find_crisis_partners(requirements: dict) -> list:
    """Кризисный подбор партнеров по срочности (заглушка)"""
    # Здесь будет сложная логика подбора по кризисным показателям
    urgency = requirements.get('urgency_level', 0)
    
    # Возвращаем примеры кризисных совпадений
    return [
        {
            'partner_id': 'partner_3',
            'company_name': 'ЭкоДом',
            'crisis_match': 0.9,
            'reason': 'Высокая срочность (9/10) и доступность мощностей (95%)',
            'priority': 3
        },
        {
            'partner_id': 'partner_1',
            'company_name': 'СтройДом Профи', 
            'crisis_match': 0.7,
            'reason': 'Средняя срочность (7/10) и хорошая доступность (80%)',
            'priority': 2
        }
    ]

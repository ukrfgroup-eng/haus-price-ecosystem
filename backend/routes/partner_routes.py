"""
Маршруты для работы с партнерами MATRIX CORE

Регистрация, управление профилями и поиск партнеров для экосистемы.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
import logging

# Создаем Blueprint для партнеров
partner_bp = Blueprint('partners', __name__)
logger = logging.getLogger(__name__)

# Временное хранилище партнеров (позже заменим на базу данных)
partners_db = {}
partner_profiles = {}

@partner_bp.route('/register', methods=['POST'])
def register_partner():
    """
    Регистрация нового партнера в экосистеме
    
    Пример запроса:
    {
        "user_id": "user_123",
        "company_name": "СтройДом Профи",
        "user_type": "contractor",
        "email": "info@stroydom.ru",
        "company_data": {
            "legal_name": "ООО СтройДом Профи",
            "tax_id": "1234567890",
            "years_on_market": 5,
            "team_size": "10-50 человек",
            "specializations": ["каркасные дома", "деревянные дома"],
            "services": ["строительство", "проектирование"],
            "regions": ["Московская область", "Центральный регион"],
            "production_capacity": "до 5 объектов в месяц",
            "current_workload": 40,
            "urgency_level": 7,
            "min_order_size": 500000,
            "flexible_pricing": true,
            "payment_terms": "предоплата 30%, поэтапная оплата",
            "warranty_period": "5 лет на конструкции"
        }
    }
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['company_name', 'user_type', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Отсутствует обязательное поле: {field}'
                }), 400
        
        user_id = data.get('user_id', str(uuid.uuid4()))
        company_name = data['company_name']
        user_type = data['user_type']
        email = data['email']
        company_data = data.get('company_data', {})
        
        # Проверка типа пользователя
        if user_type not in ['contractor', 'producer']:
            return jsonify({
                'status': 'error',
                'message': 'Тип пользователя должен быть contractor или producer'
            }), 400
        
        logger.info(f"Регистрация партнера: {company_name} ({user_type})")
        
        # Создание профиля партнера
        partner_id = str(uuid.uuid4())
        
        partner_profile = {
            'partner_id': partner_id,
            'user_id': user_id,
            'company_name': company_name,
            'user_type': user_type,
            'email': email,
            'legal_name': company_data.get('legal_name', ''),
            'tax_id': company_data.get('tax_id', ''),
            'years_on_market': company_data.get('years_on_market', 0),
            'team_size': company_data.get('team_size', ''),
            'specializations': company_data.get('specializations', []),
            'services': company_data.get('services', []),
            'materials_supply': company_data.get('materials_supply', []),
            'regions': company_data.get('regions', []),
            'willing_to_travel': company_data.get('willing_to_travel', False),
            'max_travel_distance': company_data.get('max_travel_distance', 0),
            'production_capacity': company_data.get('production_capacity', ''),
            'warehouse_space': company_data.get('warehouse_space', ''),
            'current_workload': company_data.get('current_workload', 0),
            'available_capacity': 100 - company_data.get('current_workload', 0),
            'urgency_level': company_data.get('urgency_level', 0),
            'min_order_size': company_data.get('min_order_size', 0),
            'flexible_pricing': company_data.get('flexible_pricing', False),
            'special_offers': company_data.get('special_offers', []),
            'portfolio': company_data.get('portfolio', []),
            'certificates': company_data.get('certificates', []),
            'client_reviews': company_data.get('client_reviews', []),
            'verification_status': 'pending',
            'payment_terms': company_data.get('payment_terms', ''),
            'warranty_period': company_data.get('warranty_period', ''),
            'contract_types': company_data.get('contract_types', []),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'is_active': True
        }
        
        # Сохраняем партнера
        partners_db[partner_id] = partner_profile
        partner_profiles[user_id] = partner_profile
        
        logger.info(f"Партнер зарегистрирован: {partner_id}")
        
        return jsonify({
            'status': 'success',
            'partner_id': partner_id,
            'message': 'Партнер успешно зарегистрирован',
            'verification_status': 'pending',
            'next_steps': [
                'Загрузите документы для верификации',
                'Дополните информацию о компании в личном кабинете',
                'Настройте уведомления о новых заказах'
            ]
        })
        
    except Exception as e:
        logger.error(f"Ошибка при регистрации партнера: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка регистрации: {str(e)}'
        }), 500

@partner_bp.route('/search', methods=['POST'])
def search_partners():
    """
    Поиск партнеров по критериям
    
    Пример запроса:
    {
        "criteria": {
            "regions": ["Московская область"],
            "specializations": ["каркасные дома"],
            "min_available_capacity": 50,
            "max_urgency_level": 5,
            "services": ["строительство"]
        },
        "sort_by": "relevance",  # relevance, urgency, capacity
        "limit": 10
    }
    """
    try:
        data = request.get_json()
        criteria = data.get('criteria', {})
        sort_by = data.get('sort_by', 'relevance')
        limit = data.get('limit', 10)
        
        logger.info(f"Поиск партнеров по критериям: {criteria}")
        
        # Фильтрация партнеров по критериям
        filtered_partners = []
        
        for partner_id, partner in partners_db.items():
            if not partner.get('is_active', True):
                continue
            
            # Проверка региона
            regions = criteria.get('regions', [])
            if regions and not any(region in partner.get('regions', []) for region in regions):
                continue
            
            # Проверка специализации
            specializations = criteria.get('specializations', [])
            if specializations and not any(spec in partner.get('specializations', []) for spec in specializations):
                continue
            
            # Проверка доступной мощности
            min_capacity = criteria.get('min_available_capacity', 0)
            if partner.get('available_capacity', 0) < min_capacity:
                continue
            
            # Проверка уровня срочности
            max_urgency = criteria.get('max_urgency_level', 10)
            if partner.get('urgency_level', 0) > max_urgency:
                continue
            
            # Проверка услуг
            services = criteria.get('services', [])
            if services and not any(service in partner.get('services', []) for service in services):
                continue
            
            # Расчет релевантности
            relevance_score = calculate_relevance_score(partner, criteria)
            partner['relevance_score'] = relevance_score
            
            filtered_partners.append(partner)
        
        # Сортировка результатов
        if sort_by == 'urgency':
            filtered_partners.sort(key=lambda x: x.get('urgency_level', 0), reverse=True)
        elif sort_by == 'capacity':
            filtered_partners.sort(key=lambda x: x.get('available_capacity', 0), reverse=True)
        else:  # relevance
            filtered_partners.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Ограничение количества результатов
        results = filtered_partners[:limit]
        
        return jsonify({
            'status': 'success',
            'total_found': len(filtered_partners),
            'returned': len(results),
            'partners': results
        })
        
    except Exception as e:
        logger.error(f"Ошибка при поиске партнеров: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка поиска: {str(e)}'
        }), 500

@partner_bp.route('/<partner_id>/profile', methods=['GET'])
def get_partner_profile(partner_id):
    """Получение профиля партнера по ID"""
    try:
        if partner_id not in partners_db:
            return jsonify({
                'status': 'error',
                'message': 'Партнер не найден'
            }), 404
        
        partner = partners_db[partner_id]
        
        # Не показываем некоторые системные поля
        public_profile = {k: v for k, v in partner.items() 
                         if k not in ['tax_id', 'internal_notes']}
        
        return jsonify({
            'status': 'success',
            'partner': public_profile
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении профиля партнера: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения профиля: {str(e)}'
        }), 500

@partner_bp.route('/<partner_id>/profile', methods=['PUT'])
def update_partner_profile(partner_id):
    """Обновление профиля партнера"""
    try:
        if partner_id not in partners_db:
            return jsonify({
                'status': 'error',
                'message': 'Партнер не найден'
            }), 404
        
        data = request.get_json()
        partner = partners_db[partner_id]
        
        # Обновляем разрешенные поля
        updatable_fields = [
            'company_name', 'specializations', 'services', 'materials_supply',
            'regions', 'production_capacity', 'current_workload', 'urgency_level',
            'min_order_size', 'flexible_pricing', 'special_offers', 'portfolio',
            'certificates', 'payment_terms', 'warranty_period'
        ]
        
        updates_made = 0
        for field in updatable_fields:
            if field in data:
                partner[field] = data[field]
                updates_made += 1
        
        # Пересчитываем доступную мощность
        if 'current_workload' in data:
            partner['available_capacity'] = 100 - partner['current_workload']
        
        partner['updated_at'] = datetime.now().isoformat()
        
        logger.info(f"Профиль партнера {partner_id} обновлен: {updates_made} полей")
        
        return jsonify({
            'status': 'success',
            'message': f'Профиль успешно обновлен ({updates_made} полей)',
            'updated_at': partner['updated_at']
        })
        
    except Exception as e:
        logger.error(f"Ошибка при обновлении профиля партнера: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка обновления: {str(e)}'
        }), 500

@partner_bp.route('/<partner_id>/stats', methods=['GET'])
def get_partner_stats(partner_id):
    """Получение статистики партнера"""
    try:
        if partner_id not in partners_db:
            return jsonify({
                'status': 'error',
                'message': 'Партнер не найден'
            }), 404
        
        # Здесь будет реальная статистика из базы данных
        # Пока возвращаем заглушку
        stats = {
            'profile_completeness': 75,
            'response_rate': 85,
            'avg_response_time': '2 часа',
            'total_connections': 12,
            'successful_connections': 8,
            'conversion_rate': 67,
            'customer_rating': 4.5,
            'monthly_views': 45
        }
        
        return jsonify({
            'status': 'success',
            'partner_id': partner_id,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении статистики партнера: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения статистики: {str(e)}'
        }), 500

@partner_bp.route('/crisis-board', methods=['GET'])
def get_crisis_board():
    """
    Получение доски кризисных партнеров (высокая срочность + доступные мощности)
    
    Полезно для быстрого подбора партнеров, которым срочно нужны заказы
    """
    try:
        # Фильтруем партнеров с высокой срочностью и доступными мощностями
        crisis_partners = []
        
        for partner_id, partner in partners_db.items():
            if (partner.get('urgency_level', 0) >= 7 and 
                partner.get('available_capacity', 0) >= 50 and
                partner.get('is_active', True)):
                
                crisis_partners.append({
                    'partner_id': partner_id,
                    'company_name': partner['company_name'],
                    'specializations': partner.get('specializations', []),
                    'regions': partner.get('regions', []),
                    'urgency_level': partner.get('urgency_level', 0),
                    'available_capacity': partner.get('available_capacity', 0),
                    'min_order_size': partner.get('min_order_size', 0),
                    'flexible_pricing': partner.get('flexible_pricing', False),
                    'special_offers': partner.get('special_offers', [])
                })
        
        # Сортировка по уровню срочности и доступности
        crisis_partners.sort(key=lambda x: (x['urgency_level'], x['available_capacity']), reverse=True)
        
        return jsonify({
            'status': 'success',
            'total_crisis_partners': len(crisis_partners),
            'partners': crisis_partners
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении доски кризисных партнеров: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения доски: {str(e)}'
        }), 500

# Вспомогательные функции

def calculate_relevance_score(partner: dict, criteria: dict) -> float:
    """Расчет оценки релевантности партнера критериям поиска"""
    score = 0.0
    max_score = 0.0
    
    # Регион (30%)
    regions = criteria.get('regions', [])
    if regions:
        max_score += 30
        partner_regions = partner.get('regions', [])
        if any(region in partner_regions for region in regions):
            score += 30
        elif partner_regions:
            score += 10  # Частичное совпадение
    
    # Специализация (25%)
    specializations = criteria.get('specializations', [])
    if specializations:
        max_score += 25
        partner_specs = partner.get('specializations', [])
        common_specs = set(specializations) & set(partner_specs)
        if common_specs:
            score += (len(common_specs) / len(specializations)) * 25
    
    # Услуги (20%)
    services = criteria.get('services', [])
    if services:
        max_score += 20
        partner_services = partner.get('services', [])
        common_services = set(services) & set(partner_services)
        if common_services:
            score += (len(common_services) / len(services)) * 20
    
    # Доступная мощность (15%)
    min_capacity = criteria.get('min_available_capacity', 0)
    max_score += 15
    available_capacity = partner.get('available_capacity', 0)
    if available_capacity >= min_capacity:
        score += 15
    elif available_capacity > 0:
        score += (available_capacity / min_capacity) * 15
    
    # Уровень срочности (10%)
    max_urgency = criteria.get('max_urgency_level', 10)
    max_score += 10
    urgency = partner.get('urgency_level', 0)
    if urgency <= max_urgency:
        score += 10
    else:
        score += max(0, 10 - (urgency - max_urgency) * 2)
    
    # Нормализуем оценку
    if max_score > 0:
        normalized_score = score / max_score
    else:
        normalized_score = 0.5  # Базовая оценка если нет критериев
    
    return min(1.0, normalized_score)

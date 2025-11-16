"""
Маршруты для работы с пользователями MATRIX CORE

Регистрация пользователей, управление профилями и обработка запросов.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
import logging

# Создаем Blueprint для пользователей
user_bp = Blueprint('users', __name__)
logger = logging.getLogger(__name__)

# Временное хранилище пользователей
users_db = {}
user_profiles_db = {}
user_requests_db = {}

@user_bp.route('/register', methods=['POST'])
def register_user():
    """
    Регистрация нового пользователя в экосистеме
    
    Пример запроса:
    {
        "user_type": "customer",  # customer, contractor, producer
        "email": "user@example.com",
        "initial_data": {
            "region": "Московская область",
            "preferences": {
                "response_speed": "fast",
                "communication_preference": "bot_first"
            }
        }
    }
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        if 'user_type' not in data or 'email' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Отсутствуют обязательные поля: user_type и email'
            }), 400
        
        user_type = data['user_type']
        email = data['email']
        initial_data = data.get('initial_data', {})
        
        # Проверка типа пользователя
        valid_user_types = ['customer', 'contractor', 'producer']
        if user_type not in valid_user_types:
            return jsonify({
                'status': 'error',
                'message': f'Тип пользователя должен быть одним из: {", ".join(valid_user_types)}'
            }), 400
        
        # Проверка уникальности email
        for user_id, user in users_db.items():
            if user.get('email') == email:
                return jsonify({
                    'status': 'error',
                    'message': 'Пользователь с таким email уже зарегистрирован'
                }), 400
        
        logger.info(f"Регистрация пользователя: {email} ({user_type})")
        
        # Создание пользователя
        user_id = str(uuid.uuid4())
        
        user_data = {
            'user_id': user_id,
            'user_type': user_type,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'is_active': True,
            'verification_status': 'pending'
        }
        
        # Создание профиля пользователя
        user_profile = {
            'user_id': user_id,
            'region': initial_data.get('region', ''),
            'specialization': initial_data.get('specialization', ''),
            'budget_range': initial_data.get('budget_range', ''),
            'timeline': initial_data.get('timeline', ''),
            'preferences': initial_data.get('preferences', {}),
            'interaction_history': [],
            'crisis_indicators': {
                'urgency_level': initial_data.get('urgency_level', 0),
                'available_capacity': initial_data.get('available_capacity', 100),
                'flexible_pricing': initial_data.get('flexible_pricing', False),
                'special_conditions': initial_data.get('special_conditions', [])
            }
        }
        
        # Сохраняем данные
        users_db[user_id] = user_data
        user_profiles_db[user_id] = user_profile
        
        logger.info(f"Пользователь зарегистрирован: {user_id}")
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'user_type': user_type,
            'message': 'Пользователь успешно зарегистрирован',
            'next_steps': {
                'customer': ['Создайте первый запрос', 'Уточните ваши потребности'],
                'contractor': ['Заполните профиль компании', 'Настройте уведомления'],
                'producer': ['Укажите каталог продукции', 'Настройте условия поставок']
            }.get(user_type, [])
        })
        
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка регистрации: {str(e)}'
        }), 500

@user_bp.route('/<user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    """Получение профиля пользователя"""
    try:
        if user_id not in users_db:
            return jsonify({
                'status': 'error',
                'message': 'Пользователь не найден'
            }), 404
        
        user_data = users_db[user_id]
        user_profile = user_profiles_db.get(user_id, {})
        
        # Объединяем данные пользователя и профиля
        profile = {**user_data, **user_profile}
        
        # Убираем системные поля
        public_fields = ['user_id', 'user_type', 'email', 'region', 'specialization', 
                        'budget_range', 'timeline', 'preferences', 'interaction_history',
                        'crisis_indicators', 'created_at']
        
        public_profile = {k: v for k, v in profile.items() if k in public_fields}
        
        return jsonify({
            'status': 'success',
            'user': public_profile
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении профиля пользователя: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения профиля: {str(e)}'
        }), 500

@user_bp.route('/<user_id>/profile', methods=['PUT'])
def update_user_profile(user_id):
    """Обновление профиля пользователя"""
    try:
        if user_id not in users_db:
            return jsonify({
                'status': 'error',
                'message': 'Пользователь не найден'
            }), 404
        
        data = request.get_json()
        user_profile = user_profiles_db.get(user_id, {})
        
        # Обновляем разрешенные поля
        updatable_fields = [
            'region', 'specialization', 'budget_range', 'timeline', 'preferences'
        ]
        
        crisis_fields = [
            'urgency_level', 'available_capacity', 'flexible_pricing', 'special_conditions'
        ]
        
        updates_made = 0
        
        # Обновление основных полей
        for field in updatable_fields:
            if field in data:
                user_profile[field] = data[field]
                updates_made += 1
        
        # Обновление кризисных показателей
        crisis_data = data.get('crisis_indicators', {})
        for field in crisis_fields:
            if field in crisis_data:
                user_profile.setdefault('crisis_indicators', {})[field] = crisis_data[field]
                updates_made += 1
        
        # Сохраняем обновленный профиль
        user_profiles_db[user_id] = user_profile
        users_db[user_id]['updated_at'] = datetime.now().isoformat()
        
        logger.info(f"Профиль пользователя {user_id} обновлен: {updates_made} полей")
        
        return jsonify({
            'status': 'success',
            'message': f'Профиль успешно обновлен ({updates_made} полей)',
            'updated_at': users_db[user_id]['updated_at']
        })
        
    except Exception as e:
        logger.error(f"Ошибка при обновлении профиля пользователя: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка обновления: {str(e)}'
        }), 500

@user_bp.route('/<user_id>/request', methods=['POST'])
def create_user_request(user_id):
    """
    Создание пользовательского запроса
    
    Пример запроса:
    {
        "request_type": "partner_search",
        "request_data": {
            "region": "Московская область",
            "specialization": "каркасные дома",
            "budget_range": "1-3 млн",
            "timeline": "3 месяца",
            "urgency_level": 5
        },
        "source": "umniko_bot"  # umniko_bot, tilda_lk, flexbe_site
    }
    """
    try:
        if user_id not in users_db:
            return jsonify({
                'status': 'error',
                'message': 'Пользователь не найден'
            }), 404
        
        data = request.get_json()
        
        if 'request_type' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Отсутствует тип запроса'
            }), 400
        
        request_type = data['request_type']
        request_data = data.get('request_data', {})
        source = data.get('source', 'unknown')
        
        logger.info(f"Создание запроса от пользователя {user_id}: {request_type}")
        
        # Создаем запрос
        request_id = str(uuid.uuid4())
        
        user_request = {
            'request_id': request_id,
            'user_id': user_id,
            'request_type': request_type,
            'request_data': request_data,
            'source': source,
            'created_at': datetime.now().isoformat(),
            'status': 'pending',
            'matched_partners': [],
            'response_data': {}
        }
        
        # Сохраняем запрос
        user_requests_db[request_id] = user_request
        
        # Обновляем историю взаимодействий в профиле
        user_profile = user_profiles_db.get(user_id, {})
        interaction_history = user_profile.get('interaction_history', [])
        interaction_history.append({
            'type': 'request_created',
            'request_id': request_id,
            'request_type': request_type,
            'timestamp': datetime.now().isoformat()
        })
        user_profile['interaction_history'] = interaction_history[-50:]  # Храним последние 50
        
        # Обновляем профиль на основе запроса
        if request_data:
            user_profile.update_from_request(request_data)  # Это будет реализовано позже в моделях
        
        logger.info(f"Запрос создан: {request_id}")
        
        return jsonify({
            'status': 'success',
            'request_id': request_id,
            'message': 'Запрос успешно создан',
            'next_step': 'Ожидайте подбора партнеров'
        })
        
    except Exception as e:
        logger.error(f"Ошибка при создании запроса пользователя: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка создания запроса: {str(e)}'
        }), 500

@user_bp.route('/<user_id>/requests', methods=['GET'])
def get_user_requests(user_id):
    """Получение истории запросов пользователя"""
    try:
        if user_id not in users_db:
            return jsonify({
                'status': 'error',
                'message': 'Пользователь не найден'
            }), 404
        
        # Находим все запросы пользователя
        user_requests = []
        for req_id, request_data in user_requests_db.items():
            if request_data.get('user_id') == user_id:
                # Убираем внутренние данные для публичного ответа
                public_request = {
                    'request_id': request_data['request_id'],
                    'request_type': request_data['request_type'],
                    'status': request_data['status'],
                    'created_at': request_data['created_at'],
                    'matched_partners_count': len(request_data.get('matched_partners', []))
                }
                user_requests.append(public_request)
        
        # Сортировка по дате создания (новые сначала)
        user_requests.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'total_requests': len(user_requests),
            'requests': user_requests
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении запросов пользователя: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения запросов: {str(e)}'
        }), 500

@user_bp.route('/<user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    """Получение статистики пользователя"""
    try:
        if user_id not in users_db:
            return jsonify({
                'status': 'error',
                'message': 'Пользователь не найден'
            }), 404
        
        user_data = users_db[user_id]
        user_type = user_data.get('user_type', 'customer')
        
        # Собираем статистику
        total_requests = sum(1 for req in user_requests_db.values() 
                           if req.get('user_id') == user_id)
        
        completed_requests = sum(1 for req in user_requests_db.values() 
                               if req.get('user_id') == user_id and req.get('status') == 'completed')
        
        # Временная статистика (позже заменим на реальные данные)
        stats = {
            'profile_completeness': calculate_profile_completeness(user_id),
            'total_requests': total_requests,
            'completed_requests': completed_requests,
            'success_rate': (completed_requests / total_requests * 100) if total_requests > 0 else 0,
            'active_since': user_data.get('created_at', ''),
            'last_activity': get_last_activity(user_id)
        }
        
        # Добавляем специфичную статистику по типам пользователей
        if user_type == 'customer':
            stats.update({
                'partners_contacted': 15,  # Заглушка
                'avg_response_time': '2 часа',
                'satisfaction_score': 4.2
            })
        elif user_type == 'contractor':
            stats.update({
                'leads_received': 25,  # Заглушка
                'conversion_rate': 32,
                'response_rate': 88
            })
        elif user_type == 'producer':
            stats.update({
                'inquiries_received': 18,  # Заглушка
                'partnerships_formed': 7,
                'catalog_views': 156
            })
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'user_type': user_type,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении статистики пользователя: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения статистики: {str(e)}'
        }), 500

@user_bp.route('/<user_id>/recommendations', methods=['GET'])
def get_user_recommendations(user_id):
    """Получение персонализированных рекомендаций для пользователя"""
    try:
        if user_id not in users_db:
            return jsonify({
                'status': 'error',
                'message': 'Пользователь не найден'
            }), 404
        
        user_data = users_db[user_id]
        user_type = user_data.get('user_type')
        
        # Временные рекомендации (позже заменим на AI-рекомендации)
        recommendations = generate_sample_recommendations(user_id, user_type)
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'recommendations': recommendations
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении рекомендаций: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения рекомендаций: {str(e)}'
        }), 500

# Вспомогательные функции

def calculate_profile_completeness(user_id):
    """Расчет полноты профиля пользователя"""
    profile = user_profiles_db.get(user_id, {})
    user_data = users_db.get(user_id, {})
    
    total_fields = 0
    completed_fields = 0
    
    # Проверяем основные поля
    basic_fields = ['region', 'specialization', 'budget_range']
    for field in basic_fields:
        total_fields += 1
        if profile.get(field):
            completed_fields += 1
    
    # Проверяем email
    total_fields += 1
    if user_data.get('email'):
        completed_fields += 1
    
    # Проверяем предпочтения
    total_fields += 1
    if profile.get('preferences'):
        completed_fields += 1
    
    return int((completed_fields / total_fields) * 100) if total_fields > 0 else 0

def get_last_activity(user_id):
    """Получение времени последней активности пользователя"""
    # Ищем последний запрос
    last_request = None
    for req in user_requests_db.values():
        if req.get('user_id') == user_id:
            if not last_request or req['created_at'] > last_request['created_at']:
                last_request = req
    
    return last_request['created_at'] if last_request else users_db[user_id].get('created_at')

def generate_sample_recommendations(user_id, user_type):
    """Генерация примерных рекомендаций"""
    if user_type == 'customer':
        return [
            {
                'type': 'profile_completion',
                'title': 'Заполните профиль',
                'description': 'Полные данные помогут найти лучших подрядчиков',
                'priority': 'high',
                'action': 'update_profile'
            },
            {
                'type': 'popular_search',
                'title': 'Каркасные дома в Подмосковье',
                'description': 'Самый популярный запрос в вашем регионе',
                'priority': 'medium',
                'action': 'search_partners'
            }
        ]
    elif user_type == 'contractor':
        return [
            {
                'type': 'crisis_opportunity',
                'title': 'Срочные заказы в вашем регионе',
                'description': '5 заказчиков ищут подрядчиков прямо сейчас',
                'priority': 'high',
                'action': 'view_crisis_board'
            },
            {
                'type': 'profile_optimization',
                'title': 'Добавьте портфолио',
                'description': 'Проекты с фото увеличивают отклики на 40%',
                'priority': 'medium',
                'action': 'update_portfolio'
            }
        ]
    else:  # producer
        return [
            {
                'type': 'partnership_opportunity',
                'title': 'Подрядчики ищут поставщиков',
                'description': '3 строительные компании запрашивают материалы',
                'priority': 'high',
                'action': 'view_opportunities'
            }
        ]

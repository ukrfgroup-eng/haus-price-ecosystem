"""
Маршруты для управления соединениями между пользователями MATRIX CORE

Установление связей, управление статусами и история взаимодействий.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
import logging

# Создаем Blueprint для соединений
connection_bp = Blueprint('connections', __name__)
logger = logging.getLogger(__name__)

# Временное хранилище соединений
connections_db = {}

@connection_bp.route('/users', methods=['POST'])
def connect_users():
    """
    Установление связи между пользователями
    
    Пример запроса:
    {
        "from_user": "user_123",
        "to_user": "partner_456",
        "context": {
            "request_id": "req_789",
            "reason": "Подбор по специализации каркасные дома",
            "match_score": 0.85,
            "crisis_boost": 0.3
        },
        "connection_type": "recommendation"  # recommendation, direct, introduction
    }
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['from_user', 'to_user']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Отсутствует обязательное поле: {field}'
                }), 400
        
        from_user = data['from_user']
        to_user = data['to_user']
        context = data.get('context', {})
        connection_type = data.get('connection_type', 'recommendation')
        
        logger.info(f"Создание связи: {from_user} -> {to_user} ({connection_type})")
        
        # Проверяем, нет ли уже активной связи
        existing_connection = find_existing_connection(from_user, to_user)
        if existing_connection:
            return jsonify({
                'status': 'error',
                'message': 'Связь между пользователями уже существует',
                'connection_id': existing_connection['connection_id'],
                'status': existing_connection['status']
            }), 400
        
        # Создаем новое соединение
        connection_id = str(uuid.uuid4())
        
        connection = {
            'connection_id': connection_id,
            'from_user': from_user,
            'to_user': to_user,
            'context': context,
            'connection_type': connection_type,
            'status': 'pending',  # pending, accepted, rejected, completed
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'connection_score': context.get('match_score', 0.0),
            'interactions': []
        }
        
        # Сохраняем соединение
        connections_db[connection_id] = connection
        
        logger.info(f"Связь создана: {connection_id}")
        
        return jsonify({
            'status': 'success',
            'connection_id': connection_id,
            'message': 'Связь успешно установлена',
            'next_steps': [
                'Ожидайте подтверждения от получателя',
                'После подтверждения можно обмениваться контактами'
            ]
        })
        
    except Exception as e:
        logger.error(f"Ошибка при создании связи: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка создания связи: {str(e)}'
        }), 500

@connection_bp.route('/<connection_id>/status', methods=['PUT'])
def update_connection_status(connection_id):
    """
    Обновление статуса соединения
    
    Пример запроса:
    {
        "status": "accepted",  # accepted, rejected, completed
        "notes": "Готовы к сотрудничеству"
    }
    """
    try:
        if connection_id not in connections_db:
            return jsonify({
                'status': 'error',
                'message': 'Соединение не найдено'
            }), 404
        
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Отсутствует новый статус'
            }), 400
        
        new_status = data['status']
        valid_statuses = ['pending', 'accepted', 'rejected', 'completed']
        
        if new_status not in valid_statuses:
            return jsonify({
                'status': 'error',
                'message': f'Недопустимый статус. Допустимые: {", ".join(valid_statuses)}'
            }), 400
        
        connection = connections_db[connection_id]
        old_status = connection['status']
        
        # Обновляем статус
        connection['status'] = new_status
        connection['updated_at'] = datetime.now().isoformat()
        
        # Добавляем запись во взаимодействия
        interaction = {
            'type': 'status_change',
            'from_status': old_status,
            'to_status': new_status,
            'timestamp': datetime.now().isoformat(),
            'notes': data.get('notes', '')
        }
        connection['interactions'].append(interaction)
        
        logger.info(f"Статус связи {connection_id} изменен: {old_status} -> {new_status}")
        
        return jsonify({
            'status': 'success',
            'connection_id': connection_id,
            'old_status': old_status,
            'new_status': new_status,
            'message': 'Статус успешно обновлен'
        })
        
    except Exception as e:
        logger.error(f"Ошибка при обновлении статуса связи: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка обновления статуса: {str(e)}'
        }), 500

@connection_bp.route('/user/<user_id>', methods=['GET'])
def get_user_connections(user_id):
    """Получение всех связей пользователя"""
    try:
        user_connections = []
        
        for conn_id, connection in connections_db.items():
            if connection['from_user'] == user_id or connection['to_user'] == user_id:
                # Создаем упрощенную версию для ответа
                simplified_connection = {
                    'connection_id': connection['connection_id'],
                    'from_user': connection['from_user'],
                    'to_user': connection['to_user'],
                    'status': connection['status'],
                    'connection_type': connection['connection_type'],
                    'connection_score': connection.get('connection_score', 0.0),
                    'created_at': connection['created_at'],
                    'updated_at': connection['updated_at']
                }
                
                # Добавляем информацию о другой стороне соединения
                if connection['from_user'] == user_id:
                    simplified_connection['direction'] = 'outgoing'
                    simplified_connection['other_party'] = connection['to_user']
                else:
                    simplified_connection['direction'] = 'incoming'
                    simplified_connection['other_party'] = connection['from_user']
                
                user_connections.append(simplified_connection)
        
        # Группируем по статусу
        connections_by_status = {
            'pending': [c for c in user_connections if c['status'] == 'pending'],
            'active': [c for c in user_connections if c['status'] in ['accepted', 'completed']],
            'rejected': [c for c in user_connections if c['status'] == 'rejected']
        }
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'total_connections': len(user_connections),
            'connections_by_status': connections_by_status,
            'all_connections': user_connections
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении связей пользователя: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения связей: {str(e)}'
        }), 500

@connection_bp.route('/<connection_id>', methods=['GET'])
def get_connection_details(connection_id):
    """Получение детальной информации о соединении"""
    try:
        if connection_id not in connections_db:
            return jsonify({
                'status': 'error',
                'message': 'Соединение не найдено'
            }), 404
        
        connection = connections_db[connection_id]
        
        return jsonify({
            'status': 'success',
            'connection': connection
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении деталей связи: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения деталей: {str(e)}'
        }), 500

@connection_bp.route('/<connection_id>/interaction', methods=['POST'])
def add_interaction(connection_id):
    """
    Добавление взаимодействия к соединению
    
    Пример запроса:
    {
        "interaction_type": "message",  # message, call, meeting, document
        "content": "Обсудили детали проекта",
        "metadata": {
            "duration_minutes": 30,
            "participants": ["user_123", "partner_456"]
        }
    }
    """
    try:
        if connection_id not in connections_db:
            return jsonify({
                'status': 'error',
                'message': 'Соединение не найдено'
            }), 404
        
        data = request.get_json()
        
        if 'interaction_type' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Отсутствует тип взаимодействия'
            }), 400
        
        connection = connections_db[connection_id]
        
        # Создаем запись о взаимодействии
        interaction = {
            'interaction_id': str(uuid.uuid4()),
            'type': data['interaction_type'],
            'content': data.get('content', ''),
            'metadata': data.get('metadata', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        # Добавляем к соединению
        connection['interactions'].append(interaction)
        connection['updated_at'] = datetime.now().isoformat()
        
        logger.info(f"Добавлено взаимодействие к связи {connection_id}: {data['interaction_type']}")
        
        return jsonify({
            'status': 'success',
            'connection_id': connection_id,
            'interaction_id': interaction['interaction_id'],
            'message': 'Взаимодействие успешно добавлено'
        })
        
    except Exception as e:
        logger.error(f"Ошибка при добавлении взаимодействия: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка добавления взаимодействия: {str(e)}'
        }), 500

@connection_bp.route('/stats/overview', methods=['GET'])
def get_connections_stats():
    """Получение общей статистики по соединениям в системе"""
    try:
        total_connections = len(connections_db)
        
        # Статистика по статусам
        status_counts = {}
        for connection in connections_db.values():
            status = connection['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Статистика по типам
        type_counts = {}
        for connection in connections_db.values():
            conn_type = connection['connection_type']
            type_counts[conn_type] = type_counts.get(conn_type, 0) + 1
        
        # Средняя оценка соединений
        total_score = sum(conn.get('connection_score', 0) for conn in connections_db.values())
        avg_score = total_score / total_connections if total_connections > 0 else 0
        
        stats = {
            'total_connections': total_connections,
            'status_distribution': status_counts,
            'type_distribution': type_counts,
            'average_connection_score': round(avg_score, 2),
            'successful_connections': status_counts.get('completed', 0) + status_counts.get('accepted', 0),
            'success_rate': round((status_counts.get('completed', 0) + status_counts.get('accepted', 0)) / total_connections * 100, 1) if total_connections > 0 else 0
        }
        
        return jsonify({
            'status': 'success',
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении статистики соединений: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Ошибка получения статистики: {str(e)}'
        }), 500

# Вспомогательные функции

def find_existing_connection(from_user, to_user):
    """Поиск существующей связи между пользователями"""
    for connection in connections_db.values():
        if ((connection['from_user'] == from_user and connection['to_user'] == to_user) or
            (connection['from_user'] == to_user and connection['to_user'] == from_user)):
            return connection
    return None

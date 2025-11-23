"""
API endpoints для демо-данных MATRIX CORE
"""

from flask import Blueprint, jsonify
import sys
import os

# Добавляем путь для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

demo_bp = Blueprint('demo', __name__)

@demo_bp.route('/demo/data', methods=['GET'])
def get_demo_data():
    """Получение всех демо-данных"""
    try:
        from scripts.seed_demo_data import load_demo_data
        demo_data = load_demo_data()
        
        if demo_data:
            return jsonify({
                "status": "success",
                "data": demo_data
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Демо-данные не найдены"
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка загрузки демо-данных: {str(e)}"
        }), 500

@demo_bp.route('/demo/partners', methods=['GET'])
def get_demo_partners():
    """Получение демо-партнеров"""
    try:
        from scripts.seed_demo_data import load_demo_data
        demo_data = load_demo_data()
        
        if demo_data and 'partners' in demo_data:
            return jsonify({
                "status": "success",
                "partners": demo_data['partners'],
                "total": len(demo_data['partners'])
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Демо-партнеры не найдены"
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка загрузки партнеров: {str(e)}"
        }), 500

@demo_bp.route('/demo/users', methods=['GET'])
def get_demo_users():
    """Получение демо-пользователей"""
    try:
        from scripts.seed_demo_data import load_demo_data
        demo_data = load_demo_data()
        
        if demo_data and 'users' in demo_data:
            return jsonify({
                "status": "success", 
                "users": demo_data['users'],
                "total": len(demo_data['users'])
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Демо-пользователи не найдены"
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка загрузки пользователей: {str(e)}"
        }), 500

@demo_bp.route('/demo/crisis-partners', methods=['GET'])
def get_crisis_partners():
    """Получение партнеров с кризисными показателями"""
    try:
        from scripts.seed_demo_data import load_demo_data
        demo_data = load_demo_data()
        
        if demo_data and 'partners' in demo_data:
            crisis_partners = [
                partner for partner in demo_data['partners']
                if partner.get('crisis_indicators', {}).get('urgency_level', 0) >= 7
            ]
            
            return jsonify({
                "status": "success",
                "partners": crisis_partners,
                "total": len(crisis_partners),
                "crisis_threshold": "urgency_level >= 7"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Демо-партнеры не найдены"
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка загрузки кризисных партнеров: {str(e)}"
        }), 500

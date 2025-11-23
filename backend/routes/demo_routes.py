"""
API endpoints для демо-данных MATRIX CORE
"""

from flask import Blueprint, jsonify

demo_bp = Blueprint('demo_routes', __name__)

@demo_bp.route('/demo/data', methods=['GET'])
def get_demo_data():
    """Получение всех демо-данных"""
    try:
        # Простая заглушка для демонстрации
        demo_data = {
            "status": "success",
            "message": "Демо-данные загружены успешно",
            "data": {
                "users_count": 2,
                "partners_count": 2,
                "requests_count": 1
            }
        }
        return jsonify(demo_data)
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка загрузки демо-данных: {str(e)}"
        }), 500

@demo_bp.route('/demo/partners', methods=['GET'])
def get_demo_partners():
    """Получение демо-партнеров"""
    try:
        # Заглушка с демо-партнерами
        partners = [
            {
                "partner_id": "contractor_001",
                "company_name": "СтройДом Групп",
                "specializations": ["каркасные дома", "деревянные дома"],
                "regions": ["Московская область"],
                "urgency_level": 7
            },
            {
                "partner_id": "contractor_002", 
                "company_name": "ЭкоДом Строй",
                "specializations": ["каркасные дома"],
                "regions": ["Московская область"],
                "urgency_level": 4
            }
        ]
        
        return jsonify({
            "status": "success",
            "partners": partners,
            "total": len(partners)
        })
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка загрузки партнеров: {str(e)}"
        }), 500

@demo_bp.route('/demo/crisis-partners', methods=['GET'])
def get_crisis_partners():
    """Получение партнеров с кризисными показателями"""
    try:
        # Заглушка с кризисными партнерами
        crisis_partners = [
            {
                "partner_id": "contractor_001",
                "company_name": "СтройДом Групп", 
                "urgency_level": 7,
                "available_capacity": 70,
                "special_conditions": ["рассрочка", "скидка 10% при предоплате"]
            }
        ]
        
        return jsonify({
            "status": "success",
            "partners": crisis_partners,
            "total": len(crisis_partners),
            "crisis_threshold": "urgency_level >= 7"
        })
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка загрузки кризисных партнеров: {str(e)}"
        }), 500

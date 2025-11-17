"""
Скрипт для создания демо-данных MATRIX CORE
"""

import sys
import os
from datetime import datetime

# Добавляем путь к backend для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def create_demo_data():
    """Создание демо-данных для показа партнерам"""
    
    print("🧠 СОЗДАНИЕ ДЕМО-ДАННЫХ ДЛЯ MATRIX CORE...")
    
    # Импортируем наши хранилища
    from backend.routes.analysis_routes import analysis_results, user_requests
    from backend.routes.partner_routes import partners_db, partner_profiles
    from backend.routes.user_routes import users_db, user_profiles_db, user_requests_db
    from backend.routes.connection_routes import connections_db
    
    # Очищаем существующие данные
    analysis_results.clear()
    user_requests.clear()
    partners_db.clear()
    partner_profiles.clear()
    users_db.clear()
    user_profiles_db.clear()
    user_requests_db.clear()
    connections_db.clear()
    
    print("✅ Очищены предыдущие данные")
    
    # Создаем тестовых партнеров
    demo_partners = [
        {
            "partner_id": "partner_crisis_1",
            "user_id": "user_contractor_1", 
            "company_name": "СтройДом Экспресс",
            "user_type": "contractor",
            "email": "crisis1@stroydom.ru",
            "specializations": ["каркасные дома", "деревянные дома"],
            "regions": ["Московская область"],
            "current_workload": 20,
            "available_capacity": 80,
            "urgency_level": 9,
            "min_order_size": 500000,
            "flexible_pricing": True,
            "verification_status": "verified"
        }
    ]
    
    for partner in demo_partners:
        partners_db[partner['partner_id']] = partner
        partner_profiles[partner['user_id']] = partner
    
    print("✅ Созданы демо-партнеры")
    
    # Создаем тестовых пользователей
    demo_users = [
        {
            "user_id": "user_customer_1",
            "user_type": "customer",
            "email": "customer1@example.com",
            "created_at": datetime.now().isoformat(),
            "is_active": True
        }
    ]
    
    for user in demo_users:
        users_db[user['user_id']] = user
    
    print("✅ Созданы демо-пользователи")
    
    print("🎉 ДЕМО-ДАННЫЕ СОЗДАНЫ!")

if __name__ == "__main__":
    create_demo_data()

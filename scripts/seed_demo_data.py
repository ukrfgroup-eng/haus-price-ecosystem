"""
Упрощенный скрипт для создания демо-данных MATRIX CORE
"""

import sys
import os
from datetime import datetime

def create_demo_data():
    """Создание упрощенных демо-данных"""
    
    print("🧠 СОЗДАНИЕ УПРОЩЕННЫХ ДЕМО-ДАННЫХ...")
    
    try:
        # Добавляем путь для импортов
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Импортируем хранилища
        from backend.routes.analysis_routes import analysis_results, user_requests
        from backend.routes.partner_routes import partners_db
        from backend.routes.user_routes import users_db
        from backend.routes.connection_routes import connections_db
        
        # Очищаем данные
        analysis_results.clear()
        user_requests.clear()
        partners_db.clear()
        users_db.clear()
        connections_db.clear()
        
        # Простые демо-данные
        users_db["demo_customer"] = {
            "user_id": "demo_customer",
            "user_type": "customer", 
            "email": "demo@example.com",
            "created_at": datetime.now().isoformat()
        }
        
        partners_db["demo_partner"] = {
            "partner_id": "demo_partner",
            "company_name": "Демо Строительная Компания",
            "user_type": "contractor",
            "specializations": ["каркасные дома"],
            "regions": ["Московская область"],
            "urgency_level": 7
        }
        
        print("✅ Демо-данные созданы:")
        print(f"   - Пользователей: {len(users_db)}")
        print(f"   - Партнеров: {len(partners_db)}")
        print(f"   - Анализов: {len(analysis_results)}")
        print(f"   - Соединений: {len(connections_db)}")
        
    except Exception as e:
        print(f"❌ Ошибка создания демо-данных: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = create_demo_data()
    if success:
        print("🎉 ДЕМО-ДАННЫЕ УСПЕШНО СОЗДАНЫ!")
    else:
        print("💥 ОШИБКА СОЗДАНИЯ ДЕМО-ДАННЫХ")
        sys.exit(1)

"""
ДЕМО-ДАННЫЕ ДЛЯ MATRIX CORE - ДОМА-ЦЕНЫ.РФ
Реалистичные тестовые данные для демонстрации партнерам
"""

import json
import os
from datetime import datetime, timedelta

def create_demo_data():
    """Создание реалистичных демо-данных для строительной отрасли"""
    
    demo_data = {
        "users": [
            {
                "user_id": "customer_001",
                "user_type": "customer",
                "email": "ivanov@example.com",
                "profile_data": {
                    "name": "Иван Иванов",
                    "phone": "+7 (999) 123-45-67",
                    "region": "Московская область",
                    "preferences": {
                        "response_speed": "fast",
                        "budget_range": "2-4 млн",
                        "project_type": "каркасный дом"
                    }
                },
                "created_at": (datetime.now() - timedelta(days=10)).isoformat()
            },
            {
                "user_id": "customer_002", 
                "user_type": "customer",
                "email": "petrov@example.com",
                "profile_data": {
                    "name": "Петр Петров",
                    "phone": "+7 (999) 234-56-78", 
                    "region": "Ленинградская область",
                    "preferences": {
                        "response_speed": "medium",
                        "budget_range": "1-2 млн",
                        "project_type": "отделочные работы"
                    }
                },
                "created_at": (datetime.now() - timedelta(days=5)).isoformat()
            }
        ],
        
        "partners": [
            {
                "partner_id": "contractor_001",
                "company_name": "СтройДом Групп",
                "user_type": "contractor",
                "email": "info@stroydom.ru",
                "company_data": {
                    "specializations": ["каркасные дома", "деревянные дома"],
                    "regions": ["Московская область", "Калужская область"],
                    "experience_years": 8,
                    "completed_projects": 45,
                    "team_size": 15,
                    "current_workload": 30,
                    "production_capacity": "до 5 объектов в месяц"
                },
                "crisis_indicators": {
                    "urgency_level": 7,
                    "available_capacity": 70,
                    "flexible_pricing": True,
                    "special_conditions": ["рассрочка", "скидка 10% при предоплате"]
                },
                "verification_status": "verified",
                "is_active": True,
                "created_at": (datetime.now() - timedelta(days=30)).isoformat()
            },
            {
                "partner_id": "contractor_002",
                "company_name": "ЭкоДом Строй",
                "user_type": "contractor", 
                "email": "eco@stroy.ru",
                "company_data": {
                    "specializations": ["каркасные дома", "энергоэффективные дома"],
                    "regions": ["Московская область", "Тверская область"],
                    "experience_years": 5,
                    "completed_projects": 23,
                    "team_size": 8,
                    "current_workload": 80,
                    "production_capacity": "до 2 объектов в месяц"
                },
                "crisis_indicators": {
                    "urgency_level": 4,
                    "available_capacity": 20,
                    "flexible_pricing": False,
                    "special_conditions": []
                },
                "verification_status": "verified",
                "is_active": True,
                "created_at": (datetime.now() - timedelta(days=25)).isoformat()
            },
            {
                "partner_id": "contractor_003",
                "company_name": "Быстрый Дом",
                "user_type": "contractor",
                "email": "fast@house.ru", 
                "company_data": {
                    "specializations": ["каркасные дома", "модульные дома"],
                    "regions": ["Московская область", "Владимирская область"],
                    "experience_years": 3,
                    "completed_projects": 12,
                    "team_size": 6,
                    "current_workload": 20,
                    "production_capacity": "до 3 объектов в месяц"
                },
                "crisis_indicators": {
                    "urgency_level": 9,
                    "available_capacity": 80,
                    "flexible_pricing": True,
                    "special_conditions": ["срочный выезд", "скидка 15% до конца месяца"]
                },
                "verification_status": "verified", 
                "is_active": True,
                "created_at": (datetime.now() - timedelta(days=15)).isoformat()
            },
            {
                "partner_id": "manufacturer_001",
                "company_name": "Деревянные Конструкции",
                "user_type": "manufacturer",
                "email": "wood@construct.ru",
                "company_data": {
                    "specializations": ["производство каркасов", "клееный брус"],
                    "regions": ["вся Россия"],
                    "experience_years": 12,
                    "production_capacity": "1000 м² в месяц",
                    "min_order": "50 м²",
                    "delivery_time": "7-14 дней"
                },
                "crisis_indicators": {
                    "urgency_level": 6,
                    "available_capacity": 60,
                    "flexible_pricing": True,
                    "special_conditions": ["бесплатная доставка по Москве"]
                },
                "verification_status": "verified",
                "is_active": True,
                "created_at": (datetime.now() - timedelta(days=40)).isoformat()
            }
        ],
        
        "user_requests": [
            {
                "request_id": "req_001",
                "user_id": "customer_001", 
                "request_type": "partner_search",
                "request_data": {
                    "message": "Ищу строителя каркасного дома в Московской области до 3 млн рублей",
                    "region": "Московская область",
                    "specialization": "каркасные дома", 
                    "budget_range": "2-3 млн",
                    "timeline": "3-4 месяца",
                    "urgency_level": 7
                },
                "status": "completed",
                "created_at": (datetime.now() - timedelta(days=3)).isoformat(),
                "matched_partners": ["contractor_001", "contractor_003"]
            },
            {
                "request_id": "req_002",
                "user_id": "customer_002",
                "request_type": "partner_search", 
                "request_data": {
                    "message": "Нужен подрядчик для отделки квартиры в Санкт-Петербурге",
                    "region": "Ленинградская область",
                    "specialization": "отделочные работы",
                    "budget_range": "1-1.5 млн", 
                    "timeline": "2 месяца",
                    "urgency_level": 5
                },
                "status": "pending",
                "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "matched_partners": []
            }
        ]
    }
    
    return demo_data

def save_demo_data():
    """Сохранение демо-данных в файл"""
    demo_data = create_demo_data()
    
    # Создаем папку data если ее нет
    os.makedirs('data', exist_ok=True)
    
    # Сохраняем в JSON файл
    with open('data/demo_data.json', 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, ensure_ascii=False, indent=2)
    
    print("✅ Демо-данные сохранены в data/demo_data.json")
    print(f"📊 Создано:")
    print(f"   👤 {len(demo_data['users'])} пользователей")
    print(f"   🤝 {len(demo_data['partners'])} партнеров") 
    print(f"   📝 {len(demo_data['user_requests'])} запросов")

def load_demo_data():
    """Загрузка демо-данных из файла"""
    try:
        with open('data/demo_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Файл с демо-данными не найден. Сначала запустите создание данных.")
        return None

if __name__ == "__main__":
    print("🚀 СОЗДАНИЕ ДЕМО-ДАННЫХ ДЛЯ MATRIX CORE")
    print("=" * 50)
    save_demo_data()

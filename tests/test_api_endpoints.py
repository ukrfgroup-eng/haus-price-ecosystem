"""
ТЕСТИРОВАНИЕ API ENDPOINTS MATRIX CORE
Проверка основных маршрутов системы
"""

import sys
import os
import requests

# Добавляем путь для импорта модулей backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_health_endpoint():
    """Тест endpoint проверки здоровья системы"""
    print("🔍 Тестируем /health endpoint...")
    
    try:
        # Импортируем и запускаем приложение
        from app import app
        
        with app.test_client() as client:
            response = client.get('/health')
            assert response.status_code == 200
            print("✅ /health endpoint работает")
            
    except Exception as e:
        print(f"❌ Ошибка в /health endpoint: {e}")
        raise

def test_api_status():
    """Тест endpoint статуса API"""
    print("🔍 Тестируем /api/v1/status endpoint...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/api/v1/status')
            assert response.status_code == 200
            print("✅ /api/v1/status endpoint работает")
            
    except Exception as e:
        print(f"❌ Ошибка в /api/v1/status: {e}")
        raise

def test_user_registration():
    """Тест регистрации пользователя"""
    print("🔍 Тестируем регистрацию пользователя...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            user_data = {
                "user_type": "customer",
                "email": "test@example.com",
                "initial_data": {
                    "region": "Московская область"
                }
            }
            
            response = client.post('/api/v1/users/register', 
                                 json=user_data)
            
            # Принимаем как 200 (успех), так и 400 (уже существует)
            assert response.status_code in [200, 400]
            print("✅ Регистрация пользователя работает")
            
    except Exception as e:
        print(f"❌ Ошибка регистрации пользователя: {e}")
        raise

def test_partner_search():
    """Тест поиска партнеров"""
    print("🔍 Тестируем поиск партнеров...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            search_data = {
                "criteria": {
                    "regions": ["Московская область"],
                    "specializations": ["каркасные дома"]
                }
            }
            
            response = client.post('/api/v1/partners/search', 
                                 json=search_data)
            
            assert response.status_code == 200
            print("✅ Поиск партнеров работает")
            
    except Exception as e:
        print(f"❌ Ошибка поиска партнеров: {e}")
        raise

def run_all_api_tests():
    """Запуск всех API тестов"""
    print("🚀 ЗАПУСК ТЕСТИРОВАНИЯ API ENDPOINTS")
    print("=" * 60)
    
    tests = [
        test_health_endpoint,
        test_api_status, 
        test_user_registration,
        test_partner_search
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"💥 Тест {test.__name__} упал: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"📊 РЕЗУЛЬТАТ: {passed} пройдено, {failed} упало")
    
    if failed == 0:
        print("🎉 ВСЕ API ENDPOINTS РАБОТАЮТ КОРРЕКТНО!")
        return True
    else:
        print("🔧 Некоторые endpoints требуют доработки")
        return False

if __name__ == "__main__":
    success = run_all_api_tests()
    sys.exit(0 if success else 1)

"""
Быстрая проверка импортов и базовой функциональности MATRIX CORE
"""

import sys
import os

def test_imports():
    """Проверяем что все основные модули импортируются"""
    try:
        # Добавляем корневую директорию в Python path
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from backend.app import create_app
        print("✅ Модуль app импортируется успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта app: {e}")
        return False

def test_models():
    """Проверяем создание моделей"""
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from backend.models.user_models import User
        user = User(user_id="test", user_type="customer", email="test@test.com")
        user_dict = user.to_dict()
        print("✅ Модели пользователей создаются успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка моделей пользователей: {e}")
        return False

def test_ai_helpers():
    """Проверяем AI помощники"""
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from backend.utils.ai_helpers import analyze_user_intent
        result = analyze_user_intent("Ищу строителя дома", "customer")
        print(f"✅ AI помощники работают. Намерение: {result['intent']}")
        return True
    except Exception as e:
        print(f"❌ Ошибка AI помощников: {e}")
        return False

if __name__ == "__main__":
    print("🧪 БЫСТРАЯ ПРОВЕРКА MATRIX CORE...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_models,
        test_ai_helpers
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Тест {test.__name__} упал: {e}")
    
    print("=" * 50)
    print(f"📊 РЕЗУЛЬТАТ: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("🚀 Система готова к демонстрации партнерам!")
    else:
        print("⚠️  Требуется отладка перед демо")
        sys.exit(1)

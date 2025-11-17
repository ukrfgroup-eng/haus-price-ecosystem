"""
Быстрая проверка импортов и базовой функциональности
"""

def test_imports():
    """Проверяем что все основные модули импортируются"""
    try:
        from backend.app import create_app
        from backend.config import TestingConfig
        print("✅ Основные модули импортируются")
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_models():
    """Проверяем создание моделей"""
    try:
        from backend.models.user_models import User
        user = User(user_id="test", user_type="customer", email="test@test.com")
        print("✅ Модели создаются")
        return True
    except Exception as e:
        print(f"❌ Ошибка моделей: {e}")
        return False

if __name__ == "__main__":
    print("🧪 БЫСТРАЯ ПРОВЕРКА СИСТЕМЫ...")
    
    results = [
        test_imports(),
        test_models()
    ]
    
    if all(results):
        print("🎉 Все проверки пройдены! Система готова к работе.")
    else:
        print("⚠️ Есть проблемы, которые нужно исправить.")

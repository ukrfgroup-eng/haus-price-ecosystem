"""
БАЗОВЫЕ ТЕСТЫ API БЕЗ СЛОЖНЫХ ЗАВИСИМОСТЕЙ
"""

import sys
import os

def test_flask_import():
    """Проверяем что Flask импортируется"""
    print("🔍 Проверяем импорт Flask...")
    try:
        import flask
        print("✅ Flask импортируется успешно")
        return True
    except ImportError as e:
        print(f"❌ Ошибка импорта Flask: {e}")
        return False

def test_app_structure():
    """Проверяем структуру приложения"""
    print("🔍 Проверяем структуру приложения...")
    
    # Проверяем существование основных файлов
    required_files = [
        'backend/app.py',
        'backend/config.py', 
        'backend/routes/',
        'backend/models/'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} существует")
        else:
            print(f"❌ {file_path} не найден")
            all_exist = False
    
    return all_exist

def test_simple_flask_app():
    """Пробуем создать простейшее Flask приложение"""
    print("🔍 Тестируем простое Flask приложение...")
    
    try:
        from flask import Flask
        
        # Создаем минимальное приложение
        app = Flask(__name__)
        
        @app.route('/test')
        def test_route():
            return 'OK'
        
        with app.test_client() as client:
            response = client.get('/test')
            assert response.status_code == 200
            assert b'OK' in response.data
        
        print("✅ Простое Flask приложение работает")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в простом Flask приложении: {e}")
        return False

def run_basic_tests():
    """Запуск базовых тестов"""
    print("🚀 ЗАПУСК БАЗОВЫХ ТЕСТОВ API")
    print("=" * 50)
    
    tests = [
        test_flask_import,
        test_app_structure,
        test_simple_flask_app
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 50)
    print(f"📊 РЕЗУЛЬТАТ: {passed} из {len(tests)} тестов пройдено")
    
    if passed == len(tests):
        print("🎉 БАЗОВЫЕ ТЕСТЫ ПРОЙДЕНЫ!")
        return True
    else:
        print("🔧 Требуется установка зависимостей")
        return False

if __name__ == "__main__":
    success = run_basic_tests()
    sys.exit(0 if success else 1)

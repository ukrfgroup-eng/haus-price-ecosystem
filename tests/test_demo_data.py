"""
Тесты для демо-данных MATRIX CORE
"""

import sys
import os
import json

# Добавляем путь для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_demo_data_creation():
    """Тест создания демо-данных"""
    print("🧪 Тестируем создание демо-данных...")
    
    try:
        # Запускаем создание демо-данных
        from scripts.seed_demo_data import create_demo_data, save_demo_data
        
        demo_data = create_demo_data()
        
        # Проверяем структуру данных
        assert 'users' in demo_data
        assert 'partners' in demo_data
        assert 'user_requests' in demo_data
        
        # Проверяем что есть данные
        assert len(demo_data['users']) > 0
        assert len(demo_data['partners']) > 0
        assert len(demo_data['user_requests']) > 0
        
        # Проверяем кризисные показатели
        crisis_partners = [
            p for p in demo_data['partners'] 
            if p.get('crisis_indicators', {}).get('urgency_level', 0) >= 7
        ]
        assert len(crisis_partners) > 0
        
        print("✅ Демо-данные созданы корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания демо-данных: {e}")
        return False

def test_demo_data_save_load():
    """Тест сохранения и загрузки демо-данных"""
    print("🧪 Тестируем сохранение/загрузку демо-данных...")
    
    try:
        from scripts.seed_demo_data import save_demo_data, load_demo_data
        
        # Сохраняем данные
        save_demo_data()
        
        # Загружаем данные
        loaded_data = load_demo_data()
        
        assert loaded_data is not None
        assert 'users' in loaded_data
        assert 'partners' in loaded_data
        
        print("✅ Демо-данные сохраняются и загружаются корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка сохранения/загрузки: {e}")
        return False

def run_demo_tests():
    """Запуск всех тестов демо-данных"""
    print("🚀 ТЕСТИРОВАНИЕ ДЕМО-ДАННЫХ")
    print("=" * 50)
    
    tests = [
        test_demo_data_creation,
        test_demo_data_save_load
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 50)
    print(f"📊 РЕЗУЛЬТАТ: {passed} из {len(tests)} тестов пройдено")
    
    if passed == len(tests):
        print("🎉 ДЕМО-ДАННЫЕ ГОТОВЫ К ИСПОЛЬЗОВАНИЮ!")
        return True
    else:
        print("🔧 Требуется доработка демо-данных")
        return False

if __name__ == "__main__":
    success = run_demo_tests()
    sys.exit(0 if success else 1)

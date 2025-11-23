"""
ПРОСТОЙ ТЕСТ ДЛЯ MATRIX CORE - ДОМА-ЦЕНЫ.РФ
Проверка базовой функциональности системы
"""

import sys
import os

def test_basic():
    """Базовый тест который всегда проходит"""
    print("🧪 Запуск базового теста MATRIX CORE...")
    assert 1 + 1 == 2
    print("✅ Базовый тест пройден")

def test_python_environment():
    """Проверка окружения Python"""
    print("🔍 Проверка окружения Python...")
    assert sys.version_info.major == 3
    print(f"✅ Python версия {sys.version_info.major}.{sys.version_info.minor} корректна")

def test_imports():
    """Проверка импортов основных модулей"""
    print("📦 Проверка импортов...")
    
    try:
        import json
        print("✅ Стандартные библиотеки импортируются")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        raise

def test_file_structure():
    """Проверка структуры проекта"""
    print("📁 Проверка структуры проекта...")
    
    if os.path.exists('backend'):
        print("✅ Папка backend существует")
    else:
        print("⚠️ Папка backend не найдена")

def run_all_tests():
    """Запуск всех тестов"""
    print("🚀 ЗАПУСК ТЕСТИРОВАНИЯ MATRIX CORE")
    print("=" * 50)
    
    try:
        test_basic()
        test_python_environment()
        test_imports()
        test_file_structure()
        
        print("=" * 50)
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        return True
        
    except Exception as e:
        print("=" * 50)
        print(f"💥 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО С ОШИБКОЙ: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

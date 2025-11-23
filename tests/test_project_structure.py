"""
ТЕСТ СТРУКТУРЫ ПРОЕКТА
Проверяем что все необходимые файлы и папки существуют
"""

import os
import sys

def test_project_structure():
    """Проверка структуры проекта"""
    print("📁 ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА")
    print("=" * 50)
    
    required_items = [
        # Папки
        ('backend', 'папка'),
        ('tests', 'папка'),
        ('backend/routes', 'папка'),
        ('backend/models', 'папка'),
        
        # Файлы
        ('backend/__init__.py', 'файл'),
        ('tests/__init__.py', 'файл'),
        ('backend/app.py', 'файл'),
        ('backend/config.py', 'файл'),
        ('requirements.txt', 'файл'),
        ('.github/workflows/simple-test.yml', 'файл'),
    ]
    
    all_exist = True
    
    for path, item_type in required_items:
        if os.path.exists(path):
            print(f"✅ {item_type} {path} существует")
        else:
            print(f"❌ {item_type} {path} не найден")
            all_exist = False
    
    print("=" * 50)
    
    if all_exist:
        print("🎉 СТРУКТУРА ПРОЕКТА КОРРЕКТНА!")
        return True
    else:
        print("🔧 Требуется создать отсутствующие файлы/папки")
        return False

if __name__ == "__main__":
    success = test_project_structure()
    sys.exit(0 if success else 1)

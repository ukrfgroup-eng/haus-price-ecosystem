"""
Скрипт для принудительного создания структуры проекта
"""

import os

def create_missing_structure():
    print("🔧 Создание отсутствующей структуры...")
    
    # Создаем папку models если ее нет
    models_path = "backend/models"
    if not os.path.exists(models_path):
        print(f"📁 Создаем папку: {models_path}")
        os.makedirs(models_path, exist_ok=True)
    
    # Создаем __init__.py в models если его нет
    models_init = os.path.join(models_path, "__init__.py")
    if not os.path.exists(models_init):
        print(f"📄 Создаем файл: {models_init}")
        with open(models_init, 'w') as f:
            f.write('"""Models package"""\n')
    
    print("✅ Структура создана!")

if __name__ == "__main__":
    create_missing_structure()

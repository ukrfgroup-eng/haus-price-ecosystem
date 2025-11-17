"""
Скрипт проверки корректности Python файлов
"""

import os
import sys

def check_python_files():
    """Проверяем что все .py файлы имеют корректный синтаксис"""
    print("🔍 Проверка корректности Python файлов...")
    
    problem_files = []
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Пробуем скомпилировать для проверки синтаксиса
                    compile(content, filepath, 'exec')
                    print(f"   ✅ {filepath}")
                    
                except SyntaxError as e:
                    print(f"   ❌ {filepath} - синтаксическая ошибка: {e}")
                    problem_files.append(filepath)
                except Exception as e:
                    print(f"   ⚠️  {filepath} - ошибка чтения: {e}")
    
    if problem_files:
        print(f"\n⚠️  Найдены проблемы в {len(problem_files)} файлах:")
        for file in problem_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Все Python файлы корректны!")
        return True

def check_init_files():
    """Проверяем что все __init__.py файлы корректны"""
    print("\n📦 Проверка __init__.py файлов...")
    
    init_files = []
    for root, dirs, files in os.walk('.'):
        if '__init__.py' in files:
            init_files.append(os.path.join(root, '__init__.py'))
    
    for init_file in init_files:
        try:
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем что файл не содержит явных ошибок
            if content.strip() and not content.startswith('python'):
                compile(content, init_file, 'exec')
                print(f"   ✅ {init_file}")
            elif content.strip() and content.startswith('python'):
                print(f"   ❌ {init_file} - содержит некорректное содержимое")
                return False
            else:
                print(f"   ✅ {init_file} (пустой)")
                
        except Exception as e:
            print(f"   ❌ {init_file} - ошибка: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🛠️ ПРОВЕРКА КОРРЕКТНОСТИ ФАЙЛОВ ПРОЕКТА")
    print("=" * 50)
    
    checks = [
        ("Python файлы", check_python_files()),
        ("__init__.py файлы", check_init_files()),
    ]
    
    print("=" * 50)
    all_passed = all(result for _, result in checks)
    
    if all_passed:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("🚀 Файлы проекта корректны!")
        sys.exit(0)
    else:
        print("❌ Обнаружены проблемы в файлах!")
        sys.exit(1)

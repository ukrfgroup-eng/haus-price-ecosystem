#!/usr/bin/env python3
"""
Скрипт для проверки работоспособности тестового сервера
"""

import requests
import time
import sys

def check_server():
    print("🔍 Проверка тестового сервера HAUS-PRICE ECOSYSTEM...")
    
    endpoints = [
        ("Главная страница", "/"),
        ("Проверка здоровья", "/health"),
        ("Статус системы", "/status"),
        ("Демо-данные", "/api/v1/demo/partners")
    ]
    
    base_url = "http://localhost:5000"
    all_ok = True
    
    for name, endpoint in endpoints:
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            elapsed = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                print(f"✅ {name}: {response.status_code} ({elapsed:.0f}ms)")
            else:
                print(f"❌ {name}: Ошибка {response.status_code}")
                all_ok = False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Сервер не отвечает")
            all_ok = False
        except Exception as e:
            print(f"❌ {name}: Ошибка - {e}")
            all_ok = False
    
    return all_ok

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 ТЕСТОВЫЙ СЕРВЕР HAUS-PRICE ECOSYSTEM")
    print("="*50)
    
    if check_server():
        print("\n🎉 Все проверки пройдены! Сервер работает корректно.")
        print("\n📋 Доступные endpoints:")
        print("   • http://localhost:5000/ - Главная страница")
        print("   • http://localhost:5000/health - Проверка здоровья")
        print("   • http://localhost:5000/status - Статус системы")
        print("   • http://localhost:5000/api/v1/demo/partners - Демо-данные")
    else:
        print("\n⚠️  Обнаружены проблемы с сервером!")
        print("   Убедитесь что сервер запущен: python backend/app.py")
        sys.exit(1)

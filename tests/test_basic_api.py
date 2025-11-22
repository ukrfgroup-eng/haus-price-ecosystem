"""
Базовые тесты API для MATRIX CORE - ДОМА-ЦЕНЫ.РФ
Проверяем, что основные endpoints работают корректно
"""

import pytest
import json
import sys
import os

# Добавляем backend в путь для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from config import TestingConfig

class TestBasicAPI:
    """Базовые тесты API системы"""
    
    @pytest.fixture
    def app(self):
        """Создаем тестовое приложение"""
        app = create_app(config_class=TestingConfig)
        return app
    
    @pytest.fixture
    def client(self, app):
        """Создаем тестового клиента"""
        return app.test_client()
    
    def test_health_endpoint(self, client):
        """Тест проверки здоровья системы"""
        print("🔍 Тестируем /health endpoint...")
        response = client.get('/health')
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        data = json.loads(response.data)
        assert 'status' in data, "В ответе отсутствует поле 'status'"
        assert data['status'] == 'healthy', f"Статус не 'healthy': {data['status']}"
        assert 'timestamp' in data, "В ответе отсутствует поле 'timestamp'"
        
        print("✅ /health endpoint работает корректно")
    
    def test_api_status(self, client):
        """Тест статуса API"""
        print("🔍 Тестируем /api/v1/status...")
        response = client.get('/api/v1/status')
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        data = json.loads(response.data)
        assert 'system' in data, "В ответе отсутствует поле 'system'"
        assert 'version' in data, "В ответе отсутствует поле 'version'"
        
        print("✅ /api/v1/status работает корректно")
    
    def test_home_page(self, client):
        """Тест главной страницы"""
        print("🔍 Тестируем главную страницу / ...")
        response = client.get('/')
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        print("✅ Главная страница доступна")

def test_environment():
    """Тест окружения"""
    print("🔍 Проверяем тестовое окружение...")
    
    # Проверяем, что можем импортировать основные модули
    try:
        from app import create_app
        from config import TestingConfig
        print("✅ Основные модули импортируются")
    except ImportError as e:
        pytest.fail(f"❌ Ошибка импорта модулей: {e}")

if __name__ == "__main__":
    # Запуск тестов напрямую
    pytest.main([__file__, "-v"])

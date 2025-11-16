"""
Базовые тесты для MATRIX CORE API
"""

import pytest
import json
from backend.app import create_app
from backend.config import TestingConfig

@pytest.fixture
def app():
    """Создание тестового приложения"""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """Тестовый клиент"""
    return app.test_client()

class TestBasicEndpoints:
    """Тесты базовых endpoints"""
    
    def test_health_check(self, client):
        """Тест проверки здоровья системы"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_api_status(self, client):
        """Тест статуса API"""
        response = client.get('/api/v1/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['system'] == 'MATRIX CORE'
        assert 'statistics' in data
    
    def test_home_page(self, client):
        """Тест главной страницы"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'

class TestUserRegistration:
    """Тесты регистрации пользователей"""
    
    def test_register_customer(self, client):
        """Тест регистрации заказчика"""
        user_data = {
            "user_type": "customer",
            "email": "test_customer@example.com",
            "initial_data": {
                "region": "Московская область",
                "preferences": {"response_speed": "fast"}
            }
        }
        
        response = client.post('/api/v1/users/register', 
                             json=user_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'user_id' in data
        assert data['user_type'] == 'customer'
    
    def test_register_contractor(self, client):
        """Тест регистрации подрядчика"""
        user_data = {
            "user_type": "contractor", 
            "email": "test_contractor@example.com",
            "initial_data": {
                "region": "Московская область",
                "specialization": "каркасные дома"
            }
        }
        
        response = client.post('/api/v1/users/register',
                             json=user_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'

class TestAnalysisWorkflow:
    """Тесты workflow анализа запросов"""
    
    def test_analyze_request(self, client):
        """Тест анализа пользовательского запроса"""
        request_data = {
            "user_id": "test_user_1",
            "user_type": "customer",
            "message": "Ищу строителя каркасного дома в Московской области до 3 млн рублей",
            "user_data": {
                "region": "Московская область",
                "budget_range": "1-3 млн"
            }
        }
        
        response = client.post('/api/v1/analyze/request',
                             json=request_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'analysis_id' in data
        assert 'relevant_partners_count' in data
        assert 'recommendations' in data
    
    def test_crisis_matching(self, client):
        """Тест кризисного подбора"""
        crisis_data = {
            "customer_id": "test_customer_1",
            "requirements": {
                "region": "Московская область", 
                "specialization": "каркасные дома",
                "urgency_level": 8
            }
        }
        
        response = client.post('/api/v1/analyze/crisis-match',
                             json=crisis_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'crisis_matches' in data

class TestPartnerWorkflow:
    """Тесты workflow партнеров"""
    
    def test_register_partner(self, client):
        """Тест регистрации партнера"""
        partner_data = {
            "company_name": "Тестовая Строительная Компания",
            "user_type": "contractor",
            "email": "partner@testcompany.ru",
            "company_data": {
                "specializations": ["каркасные дома", "отделочные работы"],
                "regions": ["Московская область"],
                "current_workload": 30,
                "urgency_level": 7,
                "production_capacity": "до 3 объектов в месяц"
            }
        }
        
        response = client.post('/api/v1/partners/register',
                             json=partner_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'partner_id' in data
        assert data['verification_status'] == 'pending'
    
    def test_search_partners(self, client):
        """Тест поиска партнеров"""
        search_criteria = {
            "criteria": {
                "regions": ["Московская область"],
                "specializations": ["каркасные дома"],
                "min_available_capacity": 50
            },
            "limit": 5
        }
        
        response = client.post('/api/v1/partners/search',
                             json=search_criteria,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'partners' in data
        assert 'total_found' in data

class TestWebhookIntegration:
    """Тесты интеграций через вебхуки"""
    
    def test_umniko_webhook(self, client):
        """Тест вебхука ProTalk"""
        webhook_data = {
            "user_id": "protalk_user_123",
            "message": "Ищу строителя дома в Подмосковье",
            "user_data": {
                "user_type": "customer",
                "region": "Московская область"
            },
            "session_id": "session_456"
        }
        
        response = client.post('/webhook/umniko',
                             json=webhook_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # Вебхук должен вернуть структурированный ответ для бота
    
    def test_tilda_webhook(self, client):
        """Тест вебхука Tilda"""
        form_data = {
            "form_id": "partner_registration",
            "fields": {
                "company_name": "Тест из Tilda",
                "email": "tilda_test@example.com",
                "user_type": "contractor",
                "specializations": ["каркасные дома"]
            }
        }
        
        response = client.post('/webhook/tilda',
                             json=form_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'

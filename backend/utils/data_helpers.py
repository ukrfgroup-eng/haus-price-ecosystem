"""
Утилиты для работы с данными в MATRIX CORE

Нормализация, валидация и форматирование данных.
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    """Валидатор данных для системы"""
    
    @staticmethod
    def validate_user_registration(data: Dict) -> Dict:
        """
        Валидация данных регистрации пользователя
        
        Args:
            data: Данные регистрации
        
        Returns:
            Словарь с результатами валидации
        """
        errors = []
        warnings = []
        
        # Проверка обязательных полей
        required_fields = ['user_type', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Отсутствует обязательное поле: {field}")
        
        # Валидация email
        if 'email' in data:
            email = data['email']
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                errors.append("Некорректный формат email")
        
        # Валидация типа пользователя
        valid_user_types = ['customer', 'contractor', 'producer']
        if 'user_type' in data and data['user_type'] not in valid_user_types:
            errors.append(f"Недопустимый тип пользователя. Допустимые: {', '.join(valid_user_types)}")
        
        # Проверка дополнительных данных
        if 'initial_data' in data:
            initial_errors = DataValidator._validate_initial_data(data['initial_data'])
            errors.extend(initial_errors)
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @staticmethod
    def validate_partner_registration(data: Dict) -> Dict:
        """
        Валидация данных регистрации партнера
        
        Args:
            data: Данные регистрации партнера
        
        Returns:
            Словарь с результатами валидации
        """
        errors = []
        warnings = []
        
        # Проверка обязательных полей
        required_fields = ['company_name', 'user_type', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Отсутствует обязательное поле: {field}")
        
        # Валидация company_data
        if 'company_data' in data:
            company_errors = DataValidator._validate_company_data(data['company_data'])
            errors.extend(company_errors)
        else:
            warnings.append("Рекомендуется заполнить информацию о компании")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @staticmethod
    def _validate_initial_data(data: Dict) -> List[str]:
        """Валидация начальных данных пользователя"""
        errors = []
        
        if 'region' in data and data['region']:
            if len(data['region']) < 2:
                errors.append("Регион должен содержать не менее 2 символов")
        
        if 'budget_range' in data and data['budget_range']:
            if not re.match(r'^[\d\s\-млнтысруб]+$', data['budget_range'].lower()):
                errors.append("Некорректный формат бюджетного диапазона")
        
        return errors
    
    @staticmethod
    def _validate_company_data(data: Dict) -> List[str]:
        """Валидация данных компании"""
        errors = []
        
        if 'specializations' in data:
            if not isinstance(data['specializations'], list):
                errors.append("Специализации должны быть списком")
            elif len(data['specializations']) == 0:
                errors.append("Укажите хотя бы одну специализацию")
        
        if 'regions' in data:
            if not isinstance(data['regions'], list):
                errors.append("Регионы должны быть списком")
            elif len(data['regions']) == 0:
                warnings = ["Рекомендуется указать регионы работы"]
        
        if 'current_workload' in data:
            workload = data['current_workload']
            if not isinstance(workload, (int, float)) or workload < 0 or workload > 100:
                errors.append("Загрузка мощностей должна быть числом от 0 до 100")
        
        return errors

class DataNormalizer:
    """Нормализатор данных для системы"""
    
    @staticmethod
    def normalize_user_data(data: Dict) -> Dict:
        """
        Нормализация данных пользователя
        
        Args:
            data: Исходные данные пользователя
        
        Returns:
            Нормализованные данные
        """
        normalized = data.copy()
        
        # Нормализация email
        if 'email' in normalized:
            normalized['email'] = normalized['email'].strip().lower()
        
        # Нормализация региона
        if 'region' in normalized:
            normalized['region'] = DataNormalizer._normalize_region(normalized['region'])
        
        # Нормализация специализации
        if 'specialization' in normalized:
            normalized['specialization'] = DataNormalizer._normalize_specialization(normalized['specialization'])
        
        # Нормализация бюджетного диапазона
        if 'budget_range' in normalized:
            normalized['budget_range'] = DataNormalizer._normalize_budget(normalized['budget_range'])
        
        return normalized
    
    @staticmethod
    def normalize_partner_data(data: Dict) -> Dict:
        """
        Нормализация данных партнера
        
        Args:
            data: Исходные данные партнера
        
        Returns:
            Нормализованные данные
        """
        normalized = data.copy()
        
        # Нормализация названия компании
        if 'company_name' in normalized:
            normalized['company_name'] = DataNormalizer._normalize_company_name(normalized['company_name'])
        
        # Нормализация специализаций
        if 'specializations' in normalized and isinstance(normalized['specializations'], list):
            normalized['specializations'] = [
                DataNormalizer._normalize_specialization(spec) 
                for spec in normalized['specializations']
            ]
        
        # Нормализация регионов
        if 'regions' in normalized and isinstance(normalized['regions'], list):
            normalized['regions'] = [
                DataNormalizer._normalize_region(region) 
                for region in normalized['regions']
            ]
        
        # Расчет доступной мощности
        if 'current_workload' in normalized:
            workload = normalized['current_workload']
            if isinstance(workload, (int, float)):
                normalized['available_capacity'] = 100 - workload
        
        return normalized
    
    @staticmethod
    def _normalize_region(region: str) -> str:
        """Нормализация названия региона"""
        if not region:
            return ""
        
        region = region.strip()
        
        # Приведение к стандартному формату
        region_mapping = {
            'москва': 'Московская область',
            'подмосковье': 'Московская область',
            'спб': 'Санкт-Петербург',
            'питер': 'Санкт-Петербург'
        }
        
        region_lower = region.lower()
        for key, value in region_mapping.items():
            if key in region_lower:
                return value
        
        # Капитализация первого символа
        return region.capitalize()
    
    @staticmethod
    def _normalize_specialization(specialization: str) -> str:
        """Нормализация специализации"""
        if not specialization:
            return ""
        
        specialization = specialization.strip().lower()
        
        # Приведение к стандартному формату
        spec_mapping = {
            'каркас': 'каркасные дома',
            'дерево': 'деревянные дома',
            'кирпич': 'кирпичные дома',
            'отделка': 'отделочные работы',
            'ремонт': 'ремонтные работы',
            'кровля': 'кровельные работы'
        }
        
        for key, value in spec_mapping.items():
            if key in specialization:
                return value
        
        return specialization.capitalize()
    
    @staticmethod
    def _normalize_budget(budget: str) -> str:
        """Нормализация бюджетного диапазона"""
        if not budget:
            return ""
        
        budget = budget.strip().lower()
        
        # Приведение к стандартному формату
        if 'млн' in budget or 'million' in budget:
            budget = budget.replace('million', 'млн')
            if 'руб' not in budget:
                budget += ' рублей'
        elif 'тыс' in budget or 'thousand' in budget:
            budget = budget.replace('thousand', 'тыс')
            if 'руб' not in budget:
                budget += ' рублей'
        
        return budget
    
    @staticmethod
    def _normalize_company_name(name: str) -> str:
        """Нормализация названия компании"""
        if not name:
            return ""
        
        name = name.strip()
        
        # Удаление лишних пробелов и капитализация
        name = ' '.join(word.capitalize() for word in name.split())
        
        return name

class ResponseFormatter:
    """Форматирование ответов API"""
    
    @staticmethod
    def format_success_response(data: Dict = None, message: str = "Успешно", 
                              status_code: int = 200) -> Dict:
        """
        Форматирование успешного ответа
        
        Args:
            data: Данные ответа
            message: Сообщение
            status_code: HTTP статус код
        
        Returns:
            Форматированный ответ
        """
        response = {
            'status': 'success',
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        if data:
            response['data'] = data
        
        return response
    
    @staticmethod
    def format_error_response(message: str, errors: List[str] = None, 
                            status_code: int = 400) -> Dict:
        """
        Форматирование ответа с ошибкой
        
        Args:
            message: Основное сообщение об ошибке
            errors: Детальные ошибки
            status_code: HTTP статус код
        
        Returns:
            Форматированный ответ
        """
        response = {
            'status': 'error',
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        if errors:
            response['errors'] = errors
        
        return response
    
    @staticmethod
    def format_analysis_response(analysis_result: Dict, relevant_partners: List[Dict]) -> Dict:
        """
        Форматирование ответа анализа
        
        Args:
            analysis_result: Результат анализа
            relevant_partners: Подобранные партнеры
        
        Returns:
            Форматированный ответ
        """
        return {
            'status': 'success',
            'analysis_id': analysis_result.get('analysis_id'),
            'intent': analysis_result.get('intent'),
            'confidence': analysis_result.get('confidence'),
            'entities_found': analysis_result.get('entities', {}),
            'relevant_partners_count': len(relevant_partners),
            'top_recommendations': [
                {
                    'partner_id': p['partner_id'],
                    'company_name': p['company_name'],
                    'specializations': p.get('specializations', [])[:2],
                    'match_score': p.get('match_score', 0),
                    'urgency_level': p.get('urgency_level', 0),
                    'available_capacity': p.get('available_capacity', 0)
                }
                for p in relevant_partners[:3]
            ],
            'crisis_match_score': analysis_result.get('crisis_match_score', 0),
            'timestamp': datetime.now().isoformat()
        }

# Глобальные экземпляры для использования
data_validator = DataValidator()
data_normalizer = DataNormalizer()
response_formatter = ResponseFormatter()

# Функции для импорта
def validate_request(data: Dict, request_type: str) -> Dict:
    """Валидация входящего запроса"""
    if request_type == 'user_registration':
        return data_validator.validate_user_registration(data)
    elif request_type == 'partner_registration':
        return data_validator.validate_partner_registration(data)
    else:
        return {'is_valid': True, 'errors': [], 'warnings': []}

def normalize_user_data(data: Dict) -> Dict:
    """Нормализация данных пользователя"""
    return data_normalizer.normalize_user_data(data)

def normalize_partner_data(data: Dict) -> Dict:
    """Нормализация данных партнера"""
    return data_normalizer.normalize_partner_data(data)

def format_response(data: Dict = None, message: str = "Успешно", 
                   status: str = "success") -> Dict:
    """Форматирование ответа"""
    if status == "success":
        return response_formatter.format_success_response(data, message)
    else:
        return response_formatter.format_error_response(message)

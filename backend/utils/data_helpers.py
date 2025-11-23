"""
Вспомогательные функции для работы с данными
"""

def validate_user_data(user_data):
    """Валидация данных пользователя"""
    if not user_data.get("email"):
        return False, "Email обязателен"
    return True, ""

def normalize_region(region):
    """Нормализация названия региона"""
    region_mapping = {
        "москва": "Московская область",
        "подмосковье": "Московская область", 
        "мск": "Московская область"
    }
    return region_mapping.get(region.lower(), region)

def normalize_specialization(specialization):
    """Нормализация специализации"""
    return specialization.lower()

def extract_budget_range(budget_text):
    """Извлечение диапазона бюджета из текста"""
    return {"min": 1000000, "max": 3000000}  # Заглушка

def sanitize_input_data(data):
    """Очистка входных данных"""
    if isinstance(data, str):
        return data.strip()
    return data

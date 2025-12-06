"""
Сервис для работы с API Федеральной Налоговой Службы
Проверка ИНН и верификация компаний
"""

import os
import json
import requests
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
import redis

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CompanyInfo:
    """Информация о компании из реестра ФНС"""
    inn: str
    company_name: str = ""
    ogrn: str = ""
    ogrn_date: str = ""
    status: str = ""
    address: str = ""
    okved: str = ""
    director: str = ""
    is_active: bool = False
    verification_date: datetime = None
    source: str = "fns_api"


class FNSService:
    """Сервис для работы с API ФНС"""
    
    def __init__(self):
        # Получаем ключ API из переменных окружения
        self.api_key = os.getenv('FNS_API_KEY')
        if not self.api_key:
            logger.error("FNS_API_KEY не установлен в переменных окружения")
            raise ValueError("Не указан ключ API ФНС")
        
        self.base_url = "https://api-fns.ru/api"
        self.session = requests.Session()
        
        # Настройка Redis для кэширования
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            logger.info("Redis подключен успешно")
        except Exception as e:
            logger.warning(f"Redis не доступен: {e}. Будет использоваться in-memory кэш.")
            self.redis_client = None
            self.memory_cache = {}
        
        # Лимиты API
        self.daily_limit = int(os.getenv('FNS_API_DAILY_LIMIT', 100))
        self.cache_ttl = int(os.getenv('CACHE_TTL', 86400))
        
        # Статистика использования
        self.usage_stats = {
            'today': 0,
            'last_reset': datetime.now().date()
        }
        self._load_usage_stats()
    
    def _get_cache_key(self, inn: str) -> str:
        """Генерация ключа для кэша"""
        return f"fns:{hashlib.md5(inn.encode()).hexdigest()}"
    
    def _save_to_cache(self, inn: str, data: Dict):
        """Сохранение данных в кэш"""
        cache_key = self._get_cache_key(inn)
        cache_data = {
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            if self.redis_client:
                self.redis_client.setex(
                    cache_key,
                    self.cache_ttl,
                    json.dumps(cache_data, ensure_ascii=False)
                )
            else:
                self.memory_cache[cache_key] = cache_data
        except Exception as e:
            logger.error(f"Ошибка сохранения в кэш: {e}")
    
    def _get_from_cache(self, inn: str) -> Optional[Dict]:
        """Получение данных из кэша"""
        cache_key = self._get_cache_key(inn)
        
        try:
            if self.redis_client:
                cached = self.redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            else:
                return self.memory_cache.get(cache_key)
        except Exception as e:
            logger.error(f"Ошибка чтения из кэша: {e}")
        
        return None
    
    def _load_usage_stats(self):
        """Загрузка статистики использования из кэша"""
        try:
            if self.redis_client:
                stats = self.redis_client.get('fns:usage_stats')
                if stats:
                    self.usage_stats = json.loads(stats)
                    # Проверяем, не сбросить ли счетчик на новый день
                    last_reset = datetime.fromisoformat(self.usage_stats['last_reset']).date()
                    if last_reset < datetime.now().date():
                        self.usage_stats = {
                            'today': 0,
                            'last_reset': datetime.now().date().isoformat()
                        }
                        self._save_usage_stats()
        except Exception as e:
            logger.error(f"Ошибка загрузки статистики: {e}")
    
    def _save_usage_stats(self):
        """Сохранение статистики использования"""
        try:
            if self.redis_client:
                self.redis_client.setex(
                    'fns:usage_stats',
                    86400,  # 24 часа
                    json.dumps(self.usage_stats, default=str)
                )
        except Exception as e:
            logger.error(f"Ошибка сохранения статистики: {e}")
    
    def _increment_usage(self):
        """Увеличение счетчика использования"""
        self.usage_stats['today'] += 1
        self._save_usage_stats()
        
        # Логирование при приближении к лимиту
        if self.usage_stats['today'] >= self.daily_limit * 0.8:
            logger.warning(f"Использовано {self.usage_stats['today']} из {self.daily_limit} запросов к API ФНС")
    
    def validate_inn_format(self, inn: str) -> Tuple[bool, str]:
        """
        Валидация формата ИНН
        
        Args:
            inn: ИНН для проверки
            
        Returns:
            Tuple[bool, str]: (валидность, сообщение об ошибке)
        """
        # Проверка на пустое значение
        if not inn:
            return False, "ИНН не может быть пустым"
        
        # Проверка на цифры
        if not inn.isdigit():
            return False, "ИНН должен содержать только цифры"
        
        # Проверка длины
        if len(inn) == 10:
            # Юридическое лицо
            coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8]
            check_sum = sum(int(inn[i]) * coefficients[i] for i in range(9)) % 11
            if check_sum > 9:
                check_sum = check_sum % 10
            if check_sum != int(inn[9]):
                return False, "Неверная контрольная сумма ИНН"
                
        elif len(inn) == 12:
            # Индивидуальный предприниматель
            # Первая контрольная сумма
            coefficients1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
            check_sum1 = sum(int(inn[i]) * coefficients1[i] for i in range(10)) % 11
            if check_sum1 > 9:
                check_sum1 = check_sum1 % 10
            if check_sum1 != int(inn[10]):
                return False, "Неверная контрольная сумма ИНН (первая)"
            
            # Вторая контрольная сумма
            coefficients2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
            check_sum2 = sum(int(inn[i]) * coefficients2[i] for i in range(11)) % 11
            if check_sum2 > 9:
                check_sum2 = check_sum2 % 10
            if check_sum2 != int(inn[11]):
                return False, "Неверная контрольная сумма ИНН (вторая)"
        else:
            return False, "ИНН должен содержать 10 цифр (юр.лицо) или 12 цифр (ИП)"
        
        return True, ""
    
    def check_inn(self, inn: str, force_refresh: bool = False) -> Dict:
        """
        Проверка ИНН через API ФНС
        
        Args:
            inn: ИНН для проверки
            force_refresh: Игнорировать кэш и сделать новый запрос
            
        Returns:
            Dict: Результат проверки
        """
        # Проверка формата ИНН
        is_valid, error_message = self.validate_inn_format(inn)
        if not is_valid:
            return {
                "success": False,
                "error": error_message,
                "inn": inn,
                "cached": False
            }
        
        # Проверка кэша (если не force_refresh)
        if not force_refresh:
            cached_data = self._get_from_cache(inn)
            if cached_data:
                logger.info(f"ИНН {inn} найден в кэше")
                return {
                    "success": True,
                    "data": cached_data['data'],
                    "inn": inn,
                    "cached": True
                }
        
        # Проверка лимитов API
        if self.usage_stats['today'] >= self.daily_limit:
            logger.error(f"Достигнут дневной лимит API: {self.usage_stats['today']}/{self.daily_limit}")
            return {
                "success": False,
                "error": "Достигнут дневной лимит проверок. Попробуйте завтра.",
                "inn": inn,
                "cached": False
            }
        
        try:
            # Формирование запроса к API ФНС
            url = f"{self.base_url}/egr"
            params = {
                "req": inn,
                "key": self.api_key
            }
            
            logger.info(f"Запрос к API ФНС для ИНН: {inn}")
            
            # Отправка запроса
            response = self.session.get(url, params=params, timeout=15)
            
            # Увеличиваем счетчик использования
            self._increment_usage()
            
            # Проверка статуса ответа
            if response.status_code != 200:
                logger.error(f"Ошибка API ФНС: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"Ошибка API ФНС: {response.status_code}",
                    "inn": inn,
                    "cached": False
                }
            
            # Парсинг ответа
            try:
                data = response.json()
            except json.JSONDecodeError:
                logger.error(f"Некорректный JSON от API ФНС: {response.text}")
                return {
                    "success": False,
                    "error": "Некорректный ответ от сервера ФНС",
                    "inn": inn,
                    "cached": False
                }
            
            # Обработка ответа
            if not data:
                return {
                    "success": False,
                    "error": "ИНН не найден в реестре ФНС",
                    "inn": inn,
                    "cached": False
                }
            
            # Нормализация данных
            normalized_data = self._normalize_response(data, inn)
            
            # Сохранение в кэш
            self._save_to_cache(inn, normalized_data)
            
            logger.info(f"Успешная проверка ИНН: {inn}")
            return {
                "success": True,
                "data": normalized_data,
                "inn": inn,
                "cached": False
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"Таймаут при проверке ИНН: {inn}")
            return {
                "success": False,
                "error": "Таймаут при обращении к серверу ФНС",
                "inn": inn,
                "cached": False
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети при проверке ИНН {inn}: {str(e)}")
            return {
                "success": False,
                "error": f"Ошибка сети: {str(e)}",
                "inn": inn,
                "cached": False
            }
        except Exception as e:
            logger.error(f"Неожиданная ошибка при проверке ИНН {inn}: {str(e)}")
            return {
                "success": False,
                "error": f"Внутренняя ошибка: {str(e)}",
                "inn": inn,
                "cached": False
            }
    
    def _normalize_response(self, data: Dict, inn: str) -> Dict:
        """
        Нормализация ответа от API ФНС
        
        Args:
            data: Сырые данные от API
            inn: ИНН
            
        Returns:
            Dict: Нормализованные данные
        """
        # Если ответ содержит массив, берем первый элемент
        if isinstance(data, list):
            data = data[0] if data else {}
        
        # Определение типа организации
        org_type = "Юридическое лицо" if len(inn) == 10 else "Индивидуальный предприниматель"
        
        # Базовые данные
        normalized = {
            "inn": inn,
            "org_type": org_type,
            "verification_date": datetime.now().isoformat(),
            "source": "api_fns"
        }
        
        # Для юр.лиц
        if "НаимЮЛ" in data:
            normalized.update({
                "company_name": data.get("НаимЮЛ", "").strip(),
                "short_name": data.get("СокрНаимЮЛ", ""),
                "ogrn": data.get("ОГРН", ""),
                "ogrn_date": data.get("ДатаОГРН", ""),
                "status": data.get("Статус", ""),
                "address": data.get("Адрес", ""),
                "okved": data.get("ОКВЭД", ""),
                "okved_desc": data.get("ТекстОКВЭД", ""),
                "director": data.get("Руководитель", ""),
                "founders": data.get("Учредители", ""),
                "authorized_capital": data.get("УстКап", ""),
            })
        # Для ИП
        elif "ФИО" in data:
            normalized.update({
                "full_name": data.get("ФИО", "").strip(),
                "ogrn_ip": data.get("ОГРНИП", ""),
                "ogrn_ip_date": data.get("ДатаОГРНИП", ""),
                "status": data.get("Статус", ""),
                "address": data.get("Адрес", ""),
                "okved": data.get("ОКВЭД", ""),
                "okved_desc": data.get("ТекстОКВЭД", ""),
            })
        else:
            # Если формат неизвестен, сохраняем сырые данные
            normalized["raw_data"] = data
        
        # Определение статуса активности
        status = normalized.get("status", "").lower()
        normalized["is_active"] = any(active_word in status for active_word in ["действ", "действующ"])
        
        return normalized
    
    def batch_check(self, inns: List[str]) -> Dict:
        """
        Массовая проверка ИНН
        
        Args:
            inns: Список ИНН для проверки
            
        Returns:
            Dict: Результаты проверки
        """
        results = []
        successful = 0
        failed = 0
        
        for inn in inns:
            result = self.check_inn(inn)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
        
        return {
            "total": len(inns),
            "successful": successful,
            "failed": failed,
            "results": results,
            "usage_today": self.usage_stats['today'],
            "daily_limit": self.daily_limit
        }
    
    def get_usage_stats(self) -> Dict:
        """Получение статистики использования API"""
        return {
            "used_today": self.usage_stats['today'],
            "daily_limit": self.daily_limit,
            "remaining": self.daily_limit - self.usage_stats['today'],
            "last_reset": self.usage_stats['last_reset']
        }
    
    def clear_cache(self, inn: str = None):
        """Очистка кэша"""
        try:
            if inn:
                cache_key = self._get_cache_key(inn)
                if self.redis_client:
                    self.redis_client.delete(cache_key)
                elif cache_key in self.memory_cache:
                    del self.memory_cache[cache_key]
                logger.info(f"Кэш для ИНН {inn} очищен")
            else:
                if self.redis_client:
                    # Удаляем все ключи начинающиеся с fns:
                    keys = self.redis_client.keys("fns:*")
                    if keys:
                        self.redis_client.delete(*keys)
                else:
                    self.memory_cache.clear()
                logger.info("Весь кэш ФНС очищен")
        except Exception as e:
            logger.error(f"Ошибка очистки кэша: {e}")


# Создаем глобальный экземпляр сервиса
fns_service = FNSService()

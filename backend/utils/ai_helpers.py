"""
AI-помощники для MATRIX CORE

Функции анализа намерений, извлечения сущностей и интеллектуального подбора партнеров.
"""

import re
import logging
from typing import Dict, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """Анализатор пользовательских запросов"""
    
    def __init__(self):
        self.intent_patterns = {
            'partner_search': [
                r'(ищу|нужен|найти|подобрать|помогите найти)\s+(строителя|подрядчика|производителя|специалиста)',
                r'(строитель|подрядчик|производитель|мастер)\s+(для|на)\s+',
                r'(хочу|планирую|собираюсь)\s+(строить|построить|сделать|создать)',
                r'(порекомендуйте|посоветуйте)\s+(строителя|подрядчика)'
            ],
            'info_query': [
                r'(сколько|стоимость|цена)\s+(стоит|строительства|строить)',
                r'(информация|консультация|расчет)\s+(по|о)',
                r'(как|какой|что)\s+(лучше|дешевле|надежнее)',
                r'(сроки|время)\s+(строительства|реализации)'
            ],
            'connection_request': [
                r'(связаться|связь|контакт|созвониться)\s+с',
                r'(позвонить|написать)\s+(мне|нам)',
                r'(обсудить|поговорить)\s+(детали|проект)'
            ]
        }
        
        self.entity_patterns = {
            'region': [
                r'(в|на)\s+([А-Яа-я]+\s*[область|край|республика]*)',
                r'(москв|подмосков|питер|спб|казан|новосибирск|екатеринбург)',
                r'(московская|ленинградская|нижегородская|свердловская)\s+область'
            ],
            'budget': [
                r'(\d+[\s]*[тыс| thousand]*)',
                r'(\d+[\s]*[млн| million| млн]*)',
                r'(\d+\s*-\s*\d+\s*[тыс|млн])',
                r'(бюджет|стоимость|цена)\s*(\d+)'
            ],
            'specialization': [
                r'(каркасн|деревян|кирпич|газобетон|пеноблок)',
                r'(отделк|ремонт|дизайн|проект)',
                r'(кровл|крыш|фундамент)',
                r'(сантехник|электр|отоплен)'
            ],
            'timeline': [
                r'(\d+\s*[месяц|недел|дн|год])',
                r'(срочн|быстр|скорее)',
                r'(к|до)\s*(\d+[\s\.]*(январ|феврал|март|апрел|май|июн|июл|август|сентябр|октябр|ноябр|декабр))'
            ]
        }
    
    def analyze_intent(self, message: str, user_type: str) -> Dict:
        """
        Анализ намерения пользователя на основе сообщения
        
        Args:
            message: Текст сообщения пользователя
            user_type: Тип пользователя (customer, contractor, producer)
        
        Returns:
            Словарь с определенным намерением и уверенностью
        """
        message_lower = message.lower()
        
        # Базовые намерения по умолчанию
        default_intents = {
            'customer': 'partner_search',
            'contractor': 'connection_request', 
            'producer': 'connection_request'
        }
        
        detected_intent = default_intents.get(user_type, 'info_query')
        confidence = 0.5
        matched_pattern = ""
        
        # Поиск совпадений с паттернами
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    detected_intent = intent
                    confidence = 0.8
                    matched_pattern = pattern
                    break
            if confidence > 0.5:
                break
        
        # Повышаем уверенность для определенных ключевых слов
        strong_indicators = {
            'partner_search': ['срочно', 'нужен', 'ищу', 'подрядчик'],
            'info_query': ['сколько', 'стоимость', 'информация', 'консультация'],
            'connection_request': ['связаться', 'контакт', 'телефон', 'звоните']
        }
        
        for intent, indicators in strong_indicators.items():
            for indicator in indicators:
                if indicator in message_lower:
                    if intent == detected_intent:
                        confidence = min(1.0, confidence + 0.2)
                    break
        
        logger.info(f"Определено намерение: {detected_intent} (уверенность: {confidence})")
        
        return {
            'intent': detected_intent,
            'confidence': round(confidence, 2),
            'user_type': user_type,
            'matched_pattern': matched_pattern
        }
    
    def extract_entities(self, message: str, user_data: Dict = None) -> Dict:
        """
        Извлечение сущностей из текста сообщения
        
        Args:
            message: Текст сообщения
            user_data: Дополнительные данные пользователя
        
        Returns:
            Словарь с извлеченными сущностями
        """
        if user_data is None:
            user_data = {}
        
        message_lower = message.lower()
        entities = user_data.copy()
        
        # Извлечение региона
        entities['region'] = self._extract_region(message_lower, user_data.get('region'))
        
        # Извлечение специализации
        entities['specialization'] = self._extract_specialization(message_lower, user_data.get('specialization'))
        
        # Извлечение бюджета
        entities['budget_range'] = self._extract_budget(message_lower, user_data.get('budget_range'))
        
        # Извлечение сроков
        entities['timeline'] = self._extract_timeline(message_lower, user_data.get('timeline'))
        
        # Дополнительные сущности
        entities['urgency_level'] = self._detect_urgency(message_lower)
        entities['project_scale'] = self._detect_project_scale(message_lower)
        
        logger.info(f"Извлечены сущности: { {k: v for k, v in entities.items() if v} }")
        
        return entities
    
    def _extract_region(self, message: str, default_region: str = None) -> str:
        """Извлечение региона из текста"""
        if default_region:
            return default_region
        
        region_mapping = {
            'москв': 'Московская область',
            'подмосков': 'Московская область', 
            'питер': 'Санкт-Петербург',
            'спб': 'Санкт-Петербург',
            'казан': 'Казань',
            'новосибирск': 'Новосибирск',
            'екатеринбург': 'Екатеринбург'
        }
        
        for keyword, region in region_mapping.items():
            if keyword in message:
                return region
        
        return ""
    
    def _extract_specialization(self, message: str, default_spec: str = None) -> str:
        """Извлечение специализации"""
        if default_spec:
            return default_spec
        
        spec_mapping = {
            'каркасн': 'каркасные дома',
            'деревян': 'деревянные дома',
            'кирпич': 'кирпичные дома',
            'отделк': 'отделочные работы',
            'ремонт': 'ремонт',
            'кровл': 'кровельные работы',
            'фундамент': 'фундаменты',
            'сантехник': 'сантехнические работы',
            'электр': 'электромонтажные работы'
        }
        
        for keyword, specialization in spec_mapping.items():
            if keyword in message:
                return specialization
        
        return ""
    
    def _extract_budget(self, message: str, default_budget: str = None) -> str:
        """Извлечение бюджетного диапазона"""
        if default_budget:
            return default_budget
        
        # Поиск числовых значений с указанием валюты
        budget_patterns = [
            r'(\d+[\s]*[тт]ыс[яч]?)',
            r'(\d+[\s]*[мм]лн)',
            r'(\d+\s*-\s*\d+\s*[тм])',
            r'[бБ]юджет\s*[доОт]*\s*(\d+)'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, message)
            if match:
                amount = match.group(1)
                if 'млн' in pattern or 'м' in pattern:
                    return f"{amount} млн рублей"
                else:
                    return f"{amount} тысяч рублей"
        
        return ""
    
    def _extract_timeline(self, message: str, default_timeline: str = None) -> str:
        """Извлечение сроков"""
        if default_timeline:
            return default_timeline
        
        timeline_patterns = [
            r'(\d+)\s*[мМ]есяц',
            r'(\d+)\s*[нН]ед',
            r'[сС]рок\s*[доОт]*\s*(\d+)',
            r'[кК]\s*(\d+\s*[яфмаиисонд][а-я]*)'
        ]
        
        for pattern in timeline_patterns:
            match = re.search(pattern, message)
            if match:
                return f"{match.group(1)} месяцев"
        
        if 'срочн' in message or 'быстр' in message:
            return "срочно"
        
        return ""
    
    def _detect_urgency(self, message: str) -> int:
        """Определение уровня срочности"""
        urgency_indicators = {
            'очень срочно': 9,
            'срочно': 7,
            'как можно скорее': 8,
            'в ближайшее время': 6,
            'не срочно': 3
        }
        
        for indicator, level in urgency_indicators.items():
            if indicator in message:
                return level
        
        # Определение по контексту
        if 'срочн' in message or 'быстр' in message or 'скорее' in message:
            return 7
        
        return 5  # Средняя срочность по умолчанию
    
    def _detect_project_scale(self, message: str) -> str:
        """Определение масштаба проекта"""
        if 'коттедж' in message or 'дом' in message:
            return 'частный дом'
        elif 'квартир' in message or 'апартамент' in message:
            return 'квартира'
        elif 'коммерч' in message or 'офис' in message or 'магазин' in message:
            return 'коммерческий объект'
        elif 'промышлен' in message:
            return 'промышленный объект'
        
        return 'не определен'

class PartnerMatcher:
    """Система подбора партнеров"""
    
    def __init__(self):
        self.criteria_weights = {
            'specialization': 0.25,
            'region': 0.20,
            'budget': 0.15,
            'timeline': 0.10,
            'urgency': 0.15,
            'capacity': 0.15
        }
    
    def find_relevant_partners(self, intent_analysis: Dict, entities: Dict, 
                              user_type: str, partners_db: Dict) -> List[Dict]:
        """
        Поиск релевантных партнеров на основе анализа
        
        Args:
            intent_analysis: Результат анализа намерения
            entities: Извлеченные сущности
            user_type: Тип пользователя
            partners_db: База данных партнеров
        
        Returns:
            Список подходящих партнеров с оценками
        """
        relevant_partners = []
        
        for partner_id, partner in partners_db.items():
            if not partner.get('is_active', True):
                continue
            
            # Расчет оценки соответствия
            match_score = self._calculate_match_score(partner, entities, user_type)
            
            if match_score > 0.3:  # Минимальный порог соответствия
                partner_copy = partner.copy()
                partner_copy['match_score'] = round(match_score, 2)
                partner_copy['crisis_boost'] = self._calculate_crisis_boost(partner, entities)
                relevant_partners.append(partner_copy)
        
        # Сортировка по оценке соответствия
        relevant_partners.sort(key=lambda x: x['match_score'], reverse=True)
        
        logger.info(f"Найдено релевантных партнеров: {len(relevant_partners)}")
        
        return relevant_partners
    
    def _calculate_match_score(self, partner: Dict, entities: Dict, user_type: str) -> float:
        """Расчет оценки соответствия партнера критериям"""
        total_score = 0.0
        
        # Совпадение специализации
        spec_score = self._match_specialization(partner, entities)
        total_score += spec_score * self.criteria_weights['specialization']
        
        # Совпадение региона
        region_score = self._match_region(partner, entities)
        total_score += region_score * self.criteria_weights['region']
        
        # Совпадение по бюджету
        budget_score = self._match_budget(partner, entities)
        total_score += budget_score * self.criteria_weights['budget']
        
        # Совпадение по срокам
        timeline_score = self._match_timeline(partner, entities)
        total_score += timeline_score * self.criteria_weights['timeline']
        
        # Совпадение по срочности
        urgency_score = self._match_urgency(partner, entities)
        total_score += urgency_score * self.criteria_weights['urgency']
        
        # Совпадение по мощностям
        capacity_score = self._match_capacity(partner, entities)
        total_score += capacity_score * self.criteria_weights['capacity']
        
        return min(1.0, total_score)
    
    def _match_specialization(self, partner: Dict, entities: Dict) -> float:
        """Совпадение специализации"""
        partner_specs = partner.get('specializations', [])
        required_spec = entities.get('specialization', '')
        
        if not required_spec:
            return 0.5  # Нейтральная оценка если специализация не указана
        
        for spec in partner_specs:
            if required_spec.lower() in spec.lower():
                return 1.0
        
        return 0.0
    
    def _match_region(self, partner: Dict, entities: Dict) -> float:
        """Совпадение региона"""
        partner_regions = partner.get('regions', [])
        required_region = entities.get('region', '')
        
        if not required_region:
            return 0.5  # Нейтральная оценка если регион не указан
        
        for region in partner_regions:
            if required_region.lower() in region.lower():
                return 1.0
        
        # Проверка возможности командировок
        if partner.get('willing_to_travel', False):
            return 0.7
        
        return 0.0
    
    def _match_budget(self, partner: Dict, entities: Dict) -> float:
        """Совпадение по бюджету"""
        # Упрощенная логика - в реальной системе будет сложнее
        partner_min_order = partner.get('min_order_size', 0)
        budget_mentioned = entities.get('budget_range')
        
        if not budget_mentioned:
            return 0.5
        
        # Если бюджет упомянут, даем базовое совпадение
        return 0.8
    
    def _match_timeline(self, partner: Dict, entities: Dict) -> float:
        """Совпадение по срокам"""
        timeline = entities.get('timeline', '')
        
        if not timeline:
            return 0.5
        
        # Если сроки срочные, предпочитаем партнеров с высокой доступностью
        if 'срочн' in timeline.lower():
            available_capacity = partner.get('available_capacity', 0)
            if available_capacity >= 70:
                return 1.0
            elif available_capacity >= 40:
                return 0.7
            else:
                return 0.3
        
        return 0.8
    
    def _match_urgency(self, partner: Dict, entities: Dict) -> float:
        """Совпадение по срочности"""
        customer_urgency = entities.get('urgency_level', 5)
        partner_urgency = partner.get('urgency_level', 5)
        
        # Чем выше срочность у обеих сторон, тем лучше совпадение
        urgency_diff = abs(customer_urgency - partner_urgency)
        return max(0.0, 1.0 - (urgency_diff / 10))
    
    def _match_capacity(self, partner: Dict, entities: Dict) -> float:
        """Совпадение по доступным мощностям"""
        available_capacity = partner.get('available_capacity', 0)
        
        # Чем больше доступных мощностей, тем лучше
        return available_capacity / 100.0
    
    def _calculate_crisis_boost(self, partner: Dict, entities: Dict) -> float:
        """Расчет кризисного бонуса для партнеров"""
        crisis_boost = 0.0
        
        # Бонус за высокую срочность
        if partner.get('urgency_level', 0) >= 8:
            crisis_boost += 0.3
        
        # Бонус за высокую доступность мощностей
        if partner.get('available_capacity', 0) >= 80:
            crisis_boost += 0.2
        
        # Бонус за гибкие условия
        if partner.get('flexible_pricing', False):
            crisis_boost += 0.1
        
        return min(0.5, crisis_boost)

# Глобальные экземпляры для использования
ai_analyzer = AIAnalyzer()
partner_matcher = PartnerMatcher()

# Функции для импорта
def analyze_user_intent(message: str, user_type: str) -> Dict:
    """Анализ намерения пользователя"""
    return ai_analyzer.analyze_intent(message, user_type)

def extract_entities(message: str, user_data: Dict = None) -> Dict:
    """Извлечение сущностей из сообщения"""
    return ai_analyzer.extract_entities(message, user_data)

def find_relevant_partners(intent_analysis: Dict, entities: Dict, 
                          user_type: str, partners_db: Dict) -> List[Dict]:
    """Поиск релевантных партнеров"""
    return partner_matcher.find_relevant_partners(intent_analysis, entities, user_type, partners_db)

def build_response(intent_analysis: Dict, entities: Dict, relevant_partners: List[Dict]) -> Dict:
    """
    Построение ответа для пользователя
    
    Args:
        intent_analysis: Анализ намерения
        entities: Извлеченные сущности
        relevant_partners: Подобранные партнеры
    
    Returns:
        Структурированный ответ
    """
    intent = intent_analysis.get('intent', 'unknown')
    confidence = intent_analysis.get('confidence', 0.0)
    
    response = {
        'intent': intent,
        'confidence': confidence,
        'entities_found': {k: v for k, v in entities.items() if v},
        'partners_count': len(relevant_partners),
        'recommendations': []
    }
    
    # Генерация текстового ответа в зависимости от намерения
    if intent == 'partner_search':
        if relevant_partners:
            response['message'] = f"Нашлось {len(relevant_partners)} подходящих партнеров. Рекомендую обратить внимание на:"
            response['recommendations'] = [
                {
                    'partner_id': p['partner_id'],
                    'company_name': p['company_name'],
                    'specializations': p.get('specializations', [])[:2],
                    'match_score': p.get('match_score', 0),
                    'reason': f"Совпадение по специализации и региону ({p.get('match_score', 0)*100}%)"
                }
                for p in relevant_partners[:3]  # Топ-3 рекомендации
            ]
        else:
            response['message'] = "К сожалению, по вашим критериям не найдено подходящих партнеров. Попробуйте изменить параметры поиска."
    
    elif intent == 'info_query':
        response['message'] = "По вашему запросу могу предоставить следующую информацию:"
        response['recommendations'] = [
            {
                'type': 'general_info',
                'title': 'Общая информация',
                'content': 'Средние сроки строительства: 3-6 месяцев. Стоимость: от 50 000 руб/м².'
            }
        ]
    
    elif intent == 'connection_request':
        response['message'] = "Готов помочь с установлением связи. Вот наиболее подходящие контакты:"
        response['recommendations'] = [
            {
                'partner_id': p['partner_id'],
                'company_name': p['company_name'],
                'contact_reason': 'Высокий рейтинг и отзывы',
                'preferred_contact': 'через платформу'
            }
            for p in relevant_partners[:2]
        ]
    
    else:
        response['message'] = "Понял ваш запрос. Чем еще могу помочь?"
    
    return response

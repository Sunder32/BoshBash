"""
Keyword-based Emergency Advisor Service
Простой сервис для анализа чрезвычайных ситуаций на основе ключевых слов
"""
from typing import Dict, List, Any, Optional
import re
from datetime import datetime


class KeywordAdvisor:
    """Сервис анализа и советов на основе ключевых слов"""
    
    def __init__(self):
        self.keywords = self._load_keywords()
    
    def _load_keywords(self) -> Dict[str, Dict[str, Any]]:
        """Загрузка ключевых слов для каждого типа ЧС"""
        return {
            "fire": {
                "name": "Пожар",
                "keywords": [
                    "пожар", "горит", "огонь", "дым", "задымление", "возгорание",
                    "пламя", "искры", "тушить", "горение", "пожарный", "задыхаюсь",
                    "угарный", "газ", "взрыв", "вспышка"
                ],
                "priority": 1,
                "severity": "critical",
                "immediate_actions": [
                    "Немедленно покиньте здание",
                    "Закройте все двери за собой",
                    "Не используйте лифты",
                    "Позвоните 101 (пожарная служба)",
                    "Предупредите соседей",
                    "Ждите спасателей в безопасном месте"
                ],
                "required_resources": [
                    "Пожарная бригада",
                    "Спасательная техника",
                    "Медицинская помощь"
                ],
                "safety_tips": [
                    "Не возвращайтесь в горящее здание",
                    "Закройте нос и рот мокрой тканью",
                    "Передвигайтесь пригнувшись или ползком",
                    "Не открывайте окна - это усилит огонь"
                ],
                "warning": "⚠️ КРИТИЧЕСКАЯ ОПАСНОСТЬ! Действуйте немедленно!"
            },
            
            "medical": {
                "name": "Медицинская помощь",
                "keywords": [
                    "боль", "сердце", "приступ", "кровь", "травма", "перелом",
                    "ранение", "обморок", "потеря сознания", "давление", "инфаркт",
                    "инсульт", "аллергия", "удушье", "дышать", "температура",
                    "рвота", "отравление", "судороги", "диабет", "беременность"
                ],
                "priority": 1,
                "severity": "high",
                "immediate_actions": [
                    "Позвоните 103 (скорая помощь)",
                    "Обеспечьте покой пострадавшему",
                    "Не давайте воду/еду без разрешения врача",
                    "При кровотечении - наложите давящую повязку",
                    "При переломе - обездвижьте конечность",
                    "Следите за дыханием и пульсом"
                ],
                "required_resources": [
                    "Бригада скорой помощи",
                    "Реанимация (при необходимости)",
                    "Госпитализация"
                ],
                "safety_tips": [
                    "Не перемещайте пострадавшего без крайней необходимости",
                    "Держите человека в тепле",
                    "Успокаивайте пострадавшего",
                    "Запомните время начала симптомов"
                ],
                "warning": "⚠️ При остановке дыхания начинайте СЛР немедленно!"
            },
            
            "police": {
                "name": "Полиция",
                "keywords": [
                    "кража", "грабеж", "напали", "угроза", "избили", "нападение",
                    "преступление", "вор", "разбой", "насилие", "похищение",
                    "драка", "стреляют", "оружие", "опасность", "террор",
                    "подозрительный", "преследуют", "домогательство"
                ],
                "priority": 2,
                "severity": "high",
                "immediate_actions": [
                    "Позвоните 102 (полиция)",
                    "Переместитесь в безопасное место",
                    "Не вступайте в контакт с преступниками",
                    "Запомните приметы нарушителей",
                    "Не трогайте улики",
                    "Дождитесь прибытия полиции"
                ],
                "required_resources": [
                    "Полицейский наряд",
                    "Следственная группа",
                    "Медицинская помощь (при необходимости)"
                ],
                "safety_tips": [
                    "Ваша безопасность - главный приоритет",
                    "Не преследуйте преступников самостоятельно",
                    "Зафиксируйте все детали происшествия",
                    "Сохраняйте спокойствие"
                ],
                "warning": "⚠️ При угрозе жизни немедленно покиньте опасную зону!"
            },
            
            "water_rescue": {
                "name": "Спасение на воде",
                "keywords": [
                    "тонет", "вода", "река", "озеро", "море", "бассейн", "утопление",
                    "течение", "волна", "лед", "провалился", "унесло", "не выплыть",
                    "помогите", "спасите"
                ],
                "priority": 1,
                "severity": "critical",
                "immediate_actions": [
                    "Позвоните 112 (экстренные службы)",
                    "Бросьте тонущему спасательный круг/веревку",
                    "НЕ прыгайте в воду без подготовки",
                    "Кричите, привлекайте внимание других",
                    "Если достали из воды - начните СЛР",
                    "Согрейте пострадавшего"
                ],
                "required_resources": [
                    "Спасатели на воде",
                    "Водолазная группа",
                    "Медицинская помощь"
                ],
                "safety_tips": [
                    "Не подплывайте к тонущему спереди",
                    "Используйте плавсредства для спасения",
                    "При спасении на льду - ложитесь плашмя",
                    "Вызывайте помощь до попытки спасения"
                ],
                "warning": "⚠️ КРИТИЧЕСКАЯ СИТУАЦИЯ! Счет идет на секунды!"
            },
            
            "mountain_rescue": {
                "name": "Горная спасательная",
                "keywords": [
                    "лавина", "гора", "скала", "альпинизм", "застрял", "сорвался",
                    "высота", "обрыв", "ущелье", "снег", "камнепад", "травма",
                    "не могу спуститься", "потерялся"
                ],
                "priority": 2,
                "severity": "high",
                "immediate_actions": [
                    "Позвоните 112 (экстренные службы)",
                    "Передайте точные координаты",
                    "Оставайтесь на месте, если не угрожает опасность",
                    "Подавайте световые/звуковые сигналы",
                    "Экономьте силы и тепло",
                    "Не пытайтесь спуститься самостоятельно"
                ],
                "required_resources": [
                    "Горноспасательная служба",
                    "Вертолет (при необходимости)",
                    "Альпинистское снаряжение"
                ],
                "safety_tips": [
                    "Соорудите укрытие от ветра",
                    "Используйте сигнальные средства",
                    "Не расходуйте заряд телефона",
                    "Держитесь вместе с группой"
                ],
                "warning": "⚠️ Сообщите о вашей последней известной позиции!"
            },
            
            "search_rescue": {
                "name": "Поисково-спасательная",
                "keywords": [
                    "потерялся", "заблудился", "пропал", "не могу найти",
                    "лес", "ребенок", "человек", "исчез", "поиск", "пожилой",
                    "не вышел на связь", "не вернулся"
                ],
                "priority": 2,
                "severity": "medium",
                "immediate_actions": [
                    "Позвоните 112 (экстренные службы)",
                    "Сообщите последнее известное местонахождение",
                    "Предоставьте описание одежды",
                    "Укажите особые приметы",
                    "Сообщите о состоянии здоровья",
                    "Не начинайте самостоятельные поиски в темное время"
                ],
                "required_resources": [
                    "Поисково-спасательный отряд",
                    "Кинологическая служба",
                    "Дроны/вертолет"
                ],
                "safety_tips": [
                    "Если вы потерялись - оставайтесь на месте",
                    "Подавайте световые/звуковые сигналы",
                    "Оставляйте заметные следы",
                    "Не паникуйте, экономьте силы"
                ],
                "warning": "⚠️ Время критично! Чем раньше начнется поиск, тем лучше!"
            },
            
            "ecological": {
                "name": "Экологическая угроза",
                "keywords": [
                    "химикаты", "выброс", "газ", "утечка", "загрязнение",
                    "радиация", "токсичный", "ядовитый", "испарения", "разлив",
                    "авария", "промышленность", "завод", "запах", "отравление"
                ],
                "priority": 2,
                "severity": "high",
                "immediate_actions": [
                    "Немедленно покиньте зону заражения",
                    "Двигайтесь перпендикулярно ветру",
                    "Позвоните 112 (экстренные службы)",
                    "Закройте окна и двери",
                    "Используйте средства защиты дыхания",
                    "Не трогайте подозрительные вещества"
                ],
                "required_resources": [
                    "МЧС (химическая защита)",
                    "Экологическая служба",
                    "Медицинская помощь"
                ],
                "safety_tips": [
                    "Избегайте низин - там скапливается газ",
                    "Не входите в облако/дым",
                    "Снимите загрязненную одежду",
                    "Примите душ при возможности"
                ],
                "warning": "⚠️ Экологическая опасность! Немедленно эвакуируйтесь!"
            },
            
            "general": {
                "name": "Общая ЧС",
                "keywords": [
                    "помогите", "срочно", "чрезвычайная", "авария", "катастрофа",
                    "происшествие", "беда", "sos", "спасите"
                ],
                "priority": 3,
                "severity": "medium",
                "immediate_actions": [
                    "Позвоните 112 (единая служба)",
                    "Сохраняйте спокойствие",
                    "Оцените уровень опасности",
                    "Переместитесь в безопасное место",
                    "Подробно опишите ситуацию диспетчеру",
                    "Следуйте инструкциям оператора"
                ],
                "required_resources": [
                    "Спасательная служба",
                    "Дополнительные ресурсы по необходимости"
                ],
                "safety_tips": [
                    "Не паникуйте",
                    "Помогайте другим, если это безопасно",
                    "Держите телефон заряженным",
                    "Запоминайте детали происшествия"
                ],
                "warning": "⚠️ Оставайтесь на связи со службами спасения!"
            }
        }
    
    def analyze(self, description: str) -> Dict[str, Any]:
        """
        Анализ описания ЧС и предоставление советов
        
        Args:
            description: Описание ситуации от пользователя
            
        Returns:
            Словарь с типом ЧС, приоритетом и советами
        """
        if not description:
            return self._get_default_response()
        
        description_lower = description.lower()
        
        # Подсчет совпадений для каждого типа ЧС
        matches = {}
        for emergency_type, data in self.keywords.items():
            count = 0
            matched_keywords = []
            
            for keyword in data["keywords"]:
                if keyword in description_lower:
                    count += 1
                    matched_keywords.append(keyword)
            
            if count > 0:
                matches[emergency_type] = {
                    "count": count,
                    "keywords": matched_keywords,
                    "data": data
                }
        
        # Если найдены совпадения
        if matches:
            # Выбираем тип с максимальным количеством совпадений
            best_match = max(matches.items(), key=lambda x: x[1]["count"])
            emergency_type = best_match[0]
            match_data = best_match[1]
            
            return self._build_response(
                emergency_type=emergency_type,
                data=match_data["data"],
                matched_keywords=match_data["keywords"],
                confidence=min(match_data["count"] / 5.0, 1.0)  # Максимум 1.0
            )
        
        # Если совпадений нет - возвращаем общие советы
        return self._build_response(
            emergency_type="general",
            data=self.keywords["general"],
            matched_keywords=[],
            confidence=0.3
        )
    
    def _build_response(
        self,
        emergency_type: str,
        data: Dict[str, Any],
        matched_keywords: List[str],
        confidence: float
    ) -> Dict[str, Any]:
        """Формирование ответа с советами"""
        
        # Определяем дополнительные типы если есть совпадения
        secondary_types = []
        for etype, edata in self.keywords.items():
            if etype == emergency_type:
                continue
            for keyword in matched_keywords:
                if keyword in edata["keywords"]:
                    secondary_types.append(edata["name"])
                    break
        
        return {
            "success": True,
            "detected_type": emergency_type,
            "type_name": data["name"],
            "priority": data["priority"],
            "severity": data["severity"],
            "confidence": round(confidence, 2),
            "matched_keywords": matched_keywords,
            "secondary_types": list(set(secondary_types)),
            "immediate_actions": data["immediate_actions"],
            "required_resources": data["required_resources"],
            "safety_tips": data["safety_tips"],
            "warning": data["warning"],
            "emergency_numbers": {
                "единая_служба": "112",
                "пожарная": "101",
                "полиция": "102",
                "скорая": "103"
            },
            "analyzed_at": datetime.utcnow().isoformat(),
            "method": "keyword_matching"
        }
    
    def _get_default_response(self) -> Dict[str, Any]:
        """Ответ по умолчанию при пустом описании"""
        data = self.keywords["general"]
        return {
            "success": True,
            "detected_type": "general",
            "type_name": data["name"],
            "priority": 3,
            "severity": "medium",
            "confidence": 0.0,
            "matched_keywords": [],
            "secondary_types": [],
            "immediate_actions": data["immediate_actions"],
            "required_resources": data["required_resources"],
            "safety_tips": data["safety_tips"],
            "warning": "⚠️ Предоставьте описание ситуации для точного анализа",
            "emergency_numbers": {
                "единая_служба": "112",
                "пожарная": "101",
                "полиция": "102",
                "скорая": "103"
            },
            "analyzed_at": datetime.utcnow().isoformat(),
            "method": "keyword_matching"
        }
    
    def get_advice_by_type(self, emergency_type: str) -> Dict[str, Any]:
        """
        Получить советы для конкретного типа ЧС
        
        Args:
            emergency_type: Тип чрезвычайной ситуации
            
        Returns:
            Словарь с советами
        """
        if emergency_type not in self.keywords:
            emergency_type = "general"
        
        data = self.keywords[emergency_type]
        return {
            "success": True,
            "emergency_type": emergency_type,
            "type_name": data["name"],
            "priority": data["priority"],
            "severity": data["severity"],
            "immediate_actions": data["immediate_actions"],
            "required_resources": data["required_resources"],
            "safety_tips": data["safety_tips"],
            "warning": data["warning"],
            "emergency_numbers": {
                "единая_служба": "112",
                "пожарная": "101",
                "полиция": "102",
                "скорая": "103"
            }
        }


# Глобальный экземпляр сервиса
keyword_advisor = KeywordAdvisor()

"""Упрощенное тестирование системы приоритетов"""
import sys
sys.path.insert(0, 'app')

# Минимальный тест логики расчета приоритетов
priority_keywords = {
    1: [  # КРИТИЧЕСКИЙ
        "умирает", "не дышит", "взрыв", "много крови", "без сознания",
        "горим заживо", "заблокированы", "задыхаемся", "много пострадавших"
    ],
    2: [  # ВЫСОКИЙ
        "сильная боль", "кровотечение", "боль в сердце", "боль в груди",
        "инфаркт", "инсульт", "пожар", "горит", "дым"
    ],
    3: [  # СРЕДНИЙ
        "болит", "боль", "украли", "подозрительный", "температура"
    ],
    4: [  # НИЗКИЙ
        "хроническое", "постоянно", "уже давно"
    ],
    5: [  # ОЧЕНЬ НИЗКИЙ
        "как", "что делать", "посоветуйте"
    ]
}

def calculate_priority(description: str, base_priority: int = 3) -> tuple[int, str]:
    """Вычисление приоритета"""
    description_lower = description.lower()
    
    # Критический приоритет
    for keyword in priority_keywords[1]:
        if keyword in description_lower:
            found_keywords = [kw for kw in priority_keywords[1] if kw in description_lower]
            return 1, f"КРИТИЧЕСКАЯ СИТУАЦИЯ! Обнаружены критические признаки: {', '.join(found_keywords[:3])}"
    
    # Высокий приоритет
    high_priority_count = sum(1 for keyword in priority_keywords[2] if keyword in description_lower)
    if high_priority_count >= 2:
        return 1, "Множественные признаки высокого приоритета"
    elif high_priority_count >= 1:
        found_keywords = [kw for kw in priority_keywords[2] if kw in description_lower]
        return 2, f"Высокий приоритет из-за: {', '.join(found_keywords[:3])}"
    
    # Средний приоритет
    medium_priority_count = sum(1 for keyword in priority_keywords[3] if keyword in description_lower)
    if medium_priority_count >= 3:
        return 2, "Множественные признаки среднего приоритета"
    elif medium_priority_count >= 1:
        found_keywords = [kw for kw in priority_keywords[3] if kw in description_lower]
        return 3, f"Средний приоритет. Обнаружены признаки: {', '.join(found_keywords[:3])}"
    
    # Низкий приоритет
    for keyword in priority_keywords[4]:
        if keyword in description_lower:
            return 4, "Низкий приоритет. Ситуация не требует немедленного реагирования"
    
    # Очень низкий приоритет
    for keyword in priority_keywords[5]:
        if keyword in description_lower:
            return 5, "Информационный запрос"
    
    return base_priority, f"Приоритет определен на основе типа ЧС (приоритет {base_priority})"


# Тестовые сценарии
test_cases = [
    {
        "description": "Человек умирает, не дышит, много крови!",
        "expected_priority": 1,
        "scenario": "Критическая ситуация"
    },
    {
        "description": "Взрыв в здании, много пострадавших",
        "expected_priority": 1,
        "scenario": "Массовая авария"
    },
    {
        "description": "Горим заживо, заблокированы в квартире, задыхаемся от дыма",
        "expected_priority": 1,
        "scenario": "Пожар с угрозой жизни"
    },
    {
        "description": "Сильная боль в груди, давит, холодный пот",
        "expected_priority": 2,
        "scenario": "Вероятный инфаркт"
    },
    {
        "description": "Кровотечение из раны, не останавливается",
        "expected_priority": 2,
        "scenario": "Серьезная травма"
    },
    {
        "description": "Пожар в соседней квартире, пахнет дымом",
        "expected_priority": 2,
        "scenario": "Пожар рядом"
    },
    {
        "description": "Болит голова и температура",
        "expected_priority": 3,
        "scenario": "Общее недомогание"
    },
    {
        "description": "Украли телефон на улице",
        "expected_priority": 3,
        "scenario": "Кража"
    },
    {
        "description": "Подозрительный человек возле дома",
        "expected_priority": 3,
        "scenario": "Подозрительная активность"
    },
    {
        "description": "Хроническая боль в спине, беспокоит уже давно",
        "expected_priority": 4,
        "scenario": "Хроническое состояние"
    },
    {
        "description": "Как правильно оказать первую помощь?",
        "expected_priority": 5,
        "scenario": "Информационный запрос"
    }
]

print("=" * 80)
print("ТЕСТИРОВАНИЕ ЛОГИКИ ДИНАМИЧЕСКИХ ПРИОРИТЕТОВ")
print("=" * 80)
print()

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    print(f"Тест #{i}: {test['scenario']}")
    print(f"Описание: \"{test['description']}\"")
    
    # Анализируем
    actual_priority, reason = calculate_priority(test['description'])
    expected_priority = test['expected_priority']
    
    # Проверяем результат
    status = "✅ PASS" if actual_priority == expected_priority else "❌ FAIL"
    if actual_priority == expected_priority:
        passed += 1
    else:
        failed += 1
    
    print(f"Ожидаемый приоритет: {expected_priority}")
    print(f"Полученный приоритет: {actual_priority}")
    print(f"Причина: {reason}")
    print(f"Статус: {status}")
    print("-" * 80)
    print()

print("=" * 80)
print(f"ИТОГО: {passed} успешных тестов, {failed} провалов из {len(test_cases)}")
print(f"Процент успеха: {(passed/len(test_cases)*100):.1f}%")
print("=" * 80)

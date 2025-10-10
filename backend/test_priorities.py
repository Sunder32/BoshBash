"""Тестирование системы динамических приоритетов"""
from app.services.keyword_advisor import keyword_advisor

# Тестовые сценарии с разными уровнями приоритета
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
        "description": "Горим, заблокированы в квартире, задыхаемся от дыма",
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
        "description": "Хроническая боль в спине, беспокоит уже неделю",
        "expected_priority": 4,
        "scenario": "Хроническое состояние"
    },
    {
        "description": "Как правильно оказать первую помощь?",
        "expected_priority": 4,
        "scenario": "Информационный запрос"
    }
]

print("=" * 80)
print("ТЕСТИРОВАНИЕ СИСТЕМЫ ДИНАМИЧЕСКИХ ПРИОРИТЕТОВ")
print("=" * 80)
print()

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    print(f"Тест #{i}: {test['scenario']}")
    print(f"Описание: \"{test['description']}\"")
    
    # Анализируем
    result = keyword_advisor.analyze(test['description'])
    
    actual_priority = result.get('priority')
    expected_priority = test['expected_priority']
    
    # Проверяем результат
    status = "✅ PASS" if actual_priority == expected_priority else "❌ FAIL"
    if actual_priority == expected_priority:
        passed += 1
    else:
        failed += 1
    
    print(f"Ожидаемый приоритет: {expected_priority}")
    print(f"Полученный приоритет: {actual_priority}")
    print(f"Тип ЧС: {result.get('type_name')}")
    print(f"Степень опасности: {result.get('severity')}")
    print(f"Уверенность: {result.get('confidence')}")
    print(f"Совпавшие ключевые слова: {', '.join(result.get('matched_keywords', [])[:5])}")
    
    # Выводим объяснение приоритета, если есть
    if 'priority_reason' in result:
        print(f"Причина приоритета: {result['priority_reason']}")
    
    print(f"Статус: {status}")
    print("-" * 80)
    print()

print("=" * 80)
print(f"ИТОГО: {passed} успешных тестов, {failed} провалов из {len(test_cases)}")
print(f"Процент успеха: {(passed/len(test_cases)*100):.1f}%")
print("=" * 80)

"""
Emergency Advisory API Endpoints
Анализ на основе ключевых слов и выдача советов
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from app.services.keyword_advisor import keyword_advisor
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


class AnalysisRequest(BaseModel):
    description: str
    emergency_type: Optional[str] = None


@router.post("/analyze")
async def analyze_emergency(request: AnalysisRequest):
    """
    Анализ описания ЧС на основе ключевых слов
    
    - **description**: Описание ситуации
    - **emergency_type**: (Опционально) Предполагаемый тип ЧС
    
    Возвращает:
    - Определенный тип ЧС
    - Приоритет (1-5)
    - Уровень серьезности
    - Немедленные действия
    - Необходимые ресурсы
    - Советы по безопасности
    - Экстренные номера
    """
    try:
        result = keyword_advisor.analyze(request.description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка анализа: {str(e)}")


@router.get("/advice/{emergency_type}")
async def get_advice_by_type(emergency_type: str):
    """
    Получить советы для конкретного типа ЧС
    
    - **emergency_type**: fire | medical | police | water_rescue | mountain_rescue | search_rescue | ecological | general
    
    Возвращает подробные инструкции и советы для указанного типа чрезвычайной ситуации
    """
    try:
        result = keyword_advisor.get_advice_by_type(emergency_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения советов: {str(e)}")


@router.get("/types")
async def get_emergency_types():
    """
    Получить список всех типов ЧС с описаниями
    
    Возвращает полный список поддерживаемых типов чрезвычайных ситуаций
    """
    try:
        types = []
        for etype, data in keyword_advisor.keywords.items():
            types.append({
                "code": etype,
                "name": data["name"],
                "priority": data["priority"],
                "severity": data["severity"],
                "keywords_count": len(data["keywords"])
            })
        return {
            "success": True,
            "emergency_types": types,
            "total": len(types)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")


@router.get("/emergency-numbers")
async def get_emergency_numbers():
    """
    Получить список экстренных номеров
    
    Возвращает актуальные номера служб спасения
    """
    return {
        "success": True,
        "numbers": {
            "единая_служба_спасения": {
                "number": "112",
                "description": "Единая служба экстренной помощи (работает даже без SIM-карты)"
            },
            "пожарная_охрана": {
                "number": "101",
                "description": "Пожарная охрана и спасатели"
            },
            "полиция": {
                "number": "102",
                "description": "Полиция"
            },
            "скорая_помощь": {
                "number": "103",
                "description": "Скорая медицинская помощь"
            },
            "газовая_служба": {
                "number": "104",
                "description": "Аварийная газовая служба"
            }
        },
        "note": "При звонке с мобильного телефона все номера работают, даже если нет сим-карты или денег на балансе"
    }


@router.get("/test")
async def test_advisor_service():
    """
    Проверка работоспособности сервиса советов
    """
    test_description = "У нас пожар в здании, много дыма"
    result = keyword_advisor.analyze(test_description)
    
    return {
        "success": True,
        "service": "Keyword-based Emergency Advisor",
        "status": "operational",
        "method": "keyword_matching",
        "supported_types": list(keyword_advisor.keywords.keys()),
        "test_analysis": result
    }

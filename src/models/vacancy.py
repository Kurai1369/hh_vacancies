"""Модель вакансии"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Vacancy:
    """Модель вакансии с hh.ru"""

    hh_id: int
    name: str
    url: str
    employer_id: Optional[int] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    salary_currency: Optional[str] = None
    salary_gross: Optional[bool] = None
    description: Optional[str] = None
    experience: Optional[str] = None
    employment: Optional[str] = None
    area_name: Optional[str] = None
    published_at: Optional[datetime] = None

    @classmethod
    # добавляем аннотацию типа для data
    def from_api_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        """Создаёт объект из ответа API"""
        salary = data.get("salary") or {}
        published = data.get("published_at")

        # безопасный парсинг даты
        published_dt: Optional[datetime] = None
        if published:
            try:
                published_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                published_dt = None

        return cls(
            hh_id=data["id"],
            name=data["name"],
            # alternate_url — это ссылка на вакансию для пользователя
            url=data.get("alternate_url") or data.get("url", ""),
            salary_from=salary.get("from"),
            salary_to=salary.get("to"),
            salary_currency=salary.get("currency"),
            salary_gross=salary.get("gross"),
            description=data.get("description"),
            experience=(
                data.get("experience", {}).get("name")
                if data.get("experience")
                else None
            ),
            employment=(
                data.get("employment", {}).get("name")
                if data.get("employment")
                else None
            ),
            area_name=data.get("area", {}).get("name") if data.get("area") else None,
            published_at=published_dt,
        )

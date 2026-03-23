"""Модель компании"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Company:
    """Модель компании с hh.ru"""

    hh_id: int
    name: str
    url: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    site_url: Optional[str] = None

    @classmethod
    # добавляем аннотацию типа для data
    def from_api_dict(cls, data: Dict[str, Any]) -> "Company":
        """Создаёт объект из ответа API."""
        # используем .get() для безопасного доступа к полям
        logo_urls = data.get("logo_urls") or {}
        return cls(
            hh_id=data["id"],
            name=data["name"],
            # используем alternate_url как основной, fallback на url
            url=data.get("alternate_url") or data.get("url", ""),
            logo_url=logo_urls.get("original") or logo_urls.get("90"),
            description=data.get("description"),
            site_url=data.get("site_url"),
        )

"""Скрипт для поиска работодателей по названию."""

from typing import Any, Dict, List

import requests

from src.config import Config


def search_employers(query: str, count: int = 10) -> List[Dict[str, Any]]:
    """
    Поиск работодателей по названию

    :param query: поисковый запрос
    :param count: максимальное количество результатов
    :return: список найденных работодателей
    """
    url = "https://api.hh.ru/employers"
    headers = {"User-Agent": Config.HH_USER_AGENT}
    params = {"text": query, "per_page": count}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    if response.status_code == 200:
        data = response.json()
        results: List[Dict[str, Any]] = []
        for item in data.get("items", []):
            results.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "url": item.get("alternate_url") or item.get("url", ""),
                }
            )
            print(f"ID: {item['id']}, Название: {item['name']}")
        return results
    else:
        print(f"Ошибка: {response.status_code} - {response.text[:100]}")
        return []


if __name__ == "__main__":
    # добавляем аннотацию для main-блока
    print("🔍 Поиск работодателей...")
    for company_name in ["Яндекс", "Сбер", "Тинькофф"]:
        print(f"\n📋 {company_name}:")
        search_employers(company_name, count=3)

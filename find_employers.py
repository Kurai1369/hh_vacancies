"""Поиск employer_id по названию компании через API hh.ru"""

import requests

from src.config import Config


def find_employer_id(company_name: str) -> list[dict]:
    """
    Ищет работодателей по названию и возвращает их ID

    :param company_name: название компании для поиска
    :return: список словарей с id, name и url
    """
    url = f"{Config.HH_API_BASE_URL}/employers"
    headers = {"User-Agent": Config.HH_USER_AGENT}
    params = {"text": company_name, "per_page": 10}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            results.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "url": item.get("alternate_url") or item.get("url", ""),
                }
            )
            print(f"✅ ID: {item['id']:>6} | {item['name']}")

        return results

    except requests.RequestException as e:
        print(f"⚠️ Ошибка поиска: {e}")
        return []


if __name__ == "__main__":
    print("🔍 Поиск employer_id по названию компании\n")

    # компании, которые нам интересны
    companies_to_find = [
        "Hoff",
        "Lamoda",
        "ТОКИО-CITY",
        "РусГидро",
        "Золотое Яблоко",
        "DNS",
        "ИНВИТРО",
        "ДОБРОЦЕН",
        "Офисмаг",
        "Комус",
    ]

    found_ids = []
    for company in companies_to_find:
        print(f"\n📋 Поиск: {company}")
        results = find_employer_id(company)
        if results:
            found_ids.append(results[0]["id"])  # Берём первый результат
        else:
            print(f"   ⚠️ Не найдено")

    # Выводим список для копирования в main.py
    if found_ids:
        print("\n" + "=" * 60)
        print("📋 Скопируйте этот список в main.py:")
        print("TARGET_EMPLOYERS = [")
        for emp_id in found_ids:
            print(f"    {emp_id},")
        print("]")
        print("=" * 60)

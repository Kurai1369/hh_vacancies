"""Клиент для работы с API HeadHunter"""

import time
from typing import List, Optional

import requests

from src.config import Config
from src.models.company import Company
from src.models.vacancy import Vacancy


class HHClient:
    """Клиент для получения данных с API hh.ru"""

    def __init__(self, base_url: str = Config.HH_API_BASE_URL) -> None:
        """
        Инициализирует клиент.

        :param base_url: базовый URL API
        """
        self.base_url = base_url
        self.session = requests.Session()
        # 🔧 FIX: устанавливаем User-Agent при инициализации сессии
        self.session.headers.update({"User-Agent": Config.HH_USER_AGENT})

    def get_employer(self, employer_id: int) -> Optional[Company]:
        """
        Получает информацию о работодателе по ID.

        :param employer_id: ID работодателя на hh.ru
        :return: объект Company или None
        """
        url = f"{self.base_url}/employers/{employer_id}"

        # отладочный вывод
        # print(f"🔍 Запрос: {url}")
        # print(f"🔍 Заголовки: {self.session.headers}")

        try:
            # явно передаём User-Agent в каждом запросе
            response = self.session.get(
                url, headers={"User-Agent": Config.HH_USER_AGENT}, timeout=10
            )

            # обрабатываем конкретные коды ошибок
            if response.status_code == 404:
                print(f"⚠️ Работодатель {employer_id} не найден (404)")
                return None
            if response.status_code == 400:
                # выводим ответ сервера для отладки
                print(f"⚠️ Ошибка 400 для работодателя {employer_id}")
                print(f"   Ответ API: {response.text[:150]}")
                return None

            response.raise_for_status()
            data = response.json()
            return Company.from_api_dict(data)

        except requests.RequestException as e:
            print(f"⚠️ Ошибка при получении работодателя {employer_id}: {e}")
            return None

    def get_employer_vacancies(
        self, employer_id: int, per_page: int = 100
    ) -> List[Vacancy]:
        """
        Получает список вакансий работодателя

        :param employer_id: ID работодателя
        :param per_page: количество вакансий на странице
        :return: список объектов Vacancy
        """
        vacancies: List[Vacancy] = []
        page = 0

        while True:
            url = f"{self.base_url}/vacancies"  # исправлено с "vacencies"
            params = {"employer_id": employer_id, "page": page, "per_page": per_page}

            try:
                response = self.session.get(
                    url,
                    params=params,
                    headers={"User-Agent": Config.HH_USER_AGENT},
                    timeout=10,
                )

                if response.status_code == 400:
                    print("⚠️ Ошибка 400 при получении вакансий")
                    # разбиваем длинную строку
                    print(f"   Ответ: {response.text[:100]}")
                    break

                response.raise_for_status()
                data = response.json()

                items = data.get("items", [])
                if not items:
                    break

                for item in items:
                    vacancy = Vacancy.from_api_dict(item)
                    vacancy.employer_id = employer_id
                    vacancies.append(vacancy)

                if len(items) < per_page:
                    break
                page += 1

                # Задержка между запросами
                time.sleep(0.5)

            except requests.RequestException as e:
                print(f"⚠️ Ошибка при получении вакансий: {e}")
                break

        return vacancies

"""Менеджер для работы с базой данных."""

from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from src.config import Config


class DBManager:
    """
    Класс для управления данными в базе PostgreSQL

    Предоставляет методы для получения статистики и поиска вакансий.
    """

    def __init__(self, db_name: str = Config.DB_NAME) -> None:
        """
        Инициализирует менеджер подключения к БД

        :param db_name: имя базы данных
        """
        self.db_name = db_name

    # добавляем аннотацию возврата типа
    def _get_connection(self) -> psycopg2.extensions.connection:
        """Возвращает подключение к базе данных."""
        return psycopg2.connect(dsn=Config.get_dsn())

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        """
        Получает список всех компаний и количество вакансий у каждой

        :return: список словарей с названием компании и количеством вакансий
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT
                        c.name AS company_name,
                        COUNT(v.id) AS vacancies_count
                    FROM companies c
                    LEFT JOIN vacancies v ON c.id = v.company_id
                    GROUP BY c.id, c.name
                    ORDER BY vacancies_count DESC;
                """
                )
                return [dict(row) for row in cur.fetchall()]

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """
        Получает список всех вакансий с информацией о компании

        :return: список словарей с данными о вакансиях
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT
                        c.name AS company_name,
                        v.name AS vacancy_name,
                        v.salary_from,
                        v.salary_to,
                        v.salary_currency,
                        v.url AS vacancy_url
                    FROM vacancies v
                    JOIN companies c ON v.company_id = c.id
                    ORDER BY v.published_at DESC;
                """
                )
                return [dict(row) for row in cur.fetchall()]

    def get_avg_salary(self) -> Optional[float]:
        """Получает среднюю зарплату по всем вакансиям"""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT AVG(COALESCE(salary_from, salary_to, 0)) AS avg_salary
                    FROM vacancies
                    WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
                """
                )
                result = cur.fetchone()
                # конвертируем Decimal в float
                if result and result[0] is not None:
                    return float(result[0])
                return None

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """
        Получает вакансии с зарплатой выше средней

        :return: список вакансий с зарплатой выше средней
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    WITH avg_sal AS (
                        SELECT AVG(
                            COALESCE(salary_from, salary_to, 0)
                        ) AS value
                        FROM vacancies
                        WHERE salary_from IS NOT NULL
                           OR salary_to IS NOT NULL
                    )
                    SELECT
                        c.name AS company_name,
                        v.name AS vacancy_name,
                        v.salary_from,
                        v.salary_to,
                        v.salary_currency,
                        v.url AS vacancy_url
                    FROM vacancies v
                    JOIN companies c ON v.company_id = c.id
                    CROSS JOIN avg_sal
                    WHERE COALESCE(v.salary_from, v.salary_to, 0) > avg_sal.value
                    ORDER BY
                        COALESCE(v.salary_from, v.salary_to) DESC;
                """
                )
                return [dict(row) for row in cur.fetchall()]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Ищет вакансии по ключевому слову в названии

        :param keyword: слово для поиска (например, "python")
        :return: список найденных вакансий
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT
                        c.name AS company_name,
                        v.name AS vacancy_name,
                        v.salary_from,
                        v.salary_to,
                        v.salary_currency,
                        v.url AS vacancy_url
                    FROM vacancies v
                    JOIN companies c ON v.company_id = c.id
                    WHERE v.name ILIKE %s
                    ORDER BY v.published_at DESC;
                """,
                    (f"%{keyword}%",),
                )
                return [dict(row) for row in cur.fetchall()]

    # добавляем аннотации типов для параметров
    def insert_company(self, company: Any) -> int:
        """
        Вставляет компанию в БД и возвращает её ID

        :param company: объект модели Company
        :return: ID записи в БД
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO companies
                    (hh_id, name, url, logo_url, description, site_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (hh_id) DO UPDATE
                    SET name = EXCLUDED.name
                    RETURNING id;
                """,
                    (
                        company.hh_id,
                        company.name,
                        company.url,
                        company.logo_url,
                        company.description,
                        company.site_url,
                    ),
                )
                conn.commit()
                result = cur.fetchone()
                # 🔧 FIX: явное приведение типа
                return int(result[0]) if result else 0

    # добавляем аннотации типов для параметров
    def insert_vacancy(self, vacancy: Any, company_id: int) -> None:
        """
        Вставляет вакансию в БД

        :param vacancy: объект модели Vacancy
        :param company_id: ID компании в БД
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO vacancies
                    (hh_id, company_id, name, url, salary_from, salary_to,
                     salary_currency, salary_gross, description, experience,
                     employment, area_name, published_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (hh_id) DO NOTHING;
                """,
                    (
                        vacancy.hh_id,
                        company_id,
                        vacancy.name,
                        vacancy.url,
                        vacancy.salary_from,
                        vacancy.salary_to,
                        vacancy.salary_currency,
                        vacancy.salary_gross,
                        vacancy.description,
                        vacancy.experience,
                        vacancy.employment,
                        vacancy.area_name,
                        vacancy.published_at,
                    ),
                )
                conn.commit()

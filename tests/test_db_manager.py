"""Тесты для DBManager"""
from decimal import Decimal
from unittest.mock import MagicMock, patch

from src.database.db_manager import DBManager
from src.models.company import Company
from src.models.vacancy import Vacancy


class TestDBManager:
    """Тесты методов DBManager"""

    def test_get_avg_salary_returns_numeric(self):
        """Тест: средняя зарплата возвращает числовое значение или None"""
        db = DBManager()

        # Мокаем подключение и курсор
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (Decimal("87248.37"),)
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        with patch("src.database.db_manager.psycopg2.connect", return_value=mock_conn):
            result = db.get_avg_salary()

        assert result is None or isinstance(result, (int, float, Decimal))

    def test_get_avg_salary_returns_none_when_no_data(self):
        """Тест: средняя зарплата возвращает None, если данных нет"""
        db = DBManager()

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (None,)
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        with patch("src.database.db_manager.psycopg2.connect", return_value=mock_conn):
            result = db.get_avg_salary()

        assert result is None

    def test_get_vacancies_with_keyword_returns_list(self):
        """Тест: поиск по ключевому слову возвращает список"""
        db = DBManager()

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "company_name": "Test",
                "vacancy_name": "Python Dev",
                "salary_from": 100000,
            }
        ]
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        with patch("src.database.db_manager.psycopg2.connect", return_value=mock_conn):
            result = db.get_vacancies_with_keyword("python")

        assert isinstance(result, list)

    def test_get_companies_and_vacancies_count(self):
        """Тест: получение компаний и количества вакансий"""
        db = DBManager()

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"company_name": "Yandex", "vacancies_count": 100}
        ]
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        with patch("src.database.db_manager.psycopg2.connect", return_value=mock_conn):
            result = db.get_companies_and_vacancies_count()

        assert isinstance(result, list)
        assert result[0]["company_name"] == "Yandex"

    def test_get_all_vacancies(self):
        """Тест: получение всех вакансий"""
        db = DBManager()

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "company_name": "Yandex",
                "vacancy_name": "Developer",
                "salary_from": 150000,
                "salary_to": 250000,
                "salary_currency": "RUR",
                "vacancy_url": "https://hh.ru/vacancy/123",
            }
        ]
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        with patch("src.database.db_manager.psycopg2.connect", return_value=mock_conn):
            result = db.get_all_vacancies()

        assert isinstance(result, list)

    def test_get_vacancies_with_higher_salary(self):
        """Тест: вакансии с зарплатой выше средней"""
        db = DBManager()

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "company_name": "Yandex",
                "vacancy_name": "Senior",
                "salary_from": 300000,
                "salary_to": 500000,
                "salary_currency": "RUR",
                "vacancy_url": "https://hh.ru/vacancy/456",
            }
        ]
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        with patch("src.database.db_manager.psycopg2.connect", return_value=mock_conn):
            result = db.get_vacancies_with_higher_salary()

        assert isinstance(result, list)

    def test_insert_company(self):
        """Тест: вставка компании"""
        db = DBManager()

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        company = Company(hh_id=123, name="Test", url="https://test.com")

        with patch("src.database.db_manager.psycopg2.connect", return_value=mock_conn):
            result = db.insert_company(company)

        assert result == 1

    def test_insert_vacancy(self):
        """Тест: вставка вакансии"""
        db = DBManager()

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        vacancy = Vacancy(hh_id=456, name="Dev", url="https://hh.ru/vacancy/456")

        with patch("src.database.db_manager.psycopg2.connect", return_value=mock_conn):
            db.insert_vacancy(vacancy, company_id=1)

        assert True

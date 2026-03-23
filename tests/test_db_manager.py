"""Тесты для DBManager"""

import pytest

from src.database.db_manager import DBManager


class TestDBManager:
    """Тесты методов DBManager"""

    @pytest.fixture
    def db_manager(self):
        """Фикстура с экземпляром менеджера"""
        return DBManager()

    def test_get_avg_salary_returns_float(self, db_manager):
        """Тест: средняя зарплата возвращает float или None"""
        result = db_manager.get_avg_salary()
        assert result is None or isinstance(result, (int, float))

    def test_get_vacancies_with_keyword_returns_list(self, db_manager):
        """Тест: поиск по ключевому слову возвращает список"""
        result = db_manager.get_vacancies_with_keyword("python")
        assert isinstance(result, list)

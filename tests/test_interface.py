"""Тесты для пользовательского интерфейса"""
from unittest.mock import Mock, patch

from src.cli.interface import format_salary, run_interface, show_menu


class TestInterface:
    """Тесты пользовательского интерфейса"""

    def test_format_salary_none(self):
        """Тест: зарплата не указана"""
        result = format_salary(None, None, None)
        assert result == "Зарплата не указана"

    def test_format_salary_equal(self):
        """Тест: зарплата равна (фиксированная)"""
        result = format_salary(100000, 100000, "RUR")
        assert result == "100,000 RUR"

    def test_format_salary_range(self):
        """Тест: зарплата диапазон"""
        result = format_salary(100000, 150000, "RUR")
        assert result == "100,000 – 150,000 RUR"

    def test_format_salary_from_only(self):
        """Тест: зарплата от"""
        result = format_salary(100000, None, "RUR")
        assert result == "от 100,000 RUR"

    def test_format_salary_to_only(self):
        """Тест: зарплата до"""
        result = format_salary(None, 150000, "RUR")
        assert result == "до 150,000 RUR"

    def test_format_salary_default_currency(self):
        """Тест: валюта по умолчанию"""
        result = format_salary(100000, 150000, None)
        assert "RUR" in result

    def test_format_salary_kzt(self):
        """Тест: валюта KZT"""
        result = format_salary(500000, 700000, "KZT")
        assert "KZT" in result

    def test_show_menu(self, capsys):
        """Тест: отображение меню"""
        show_menu()
        captured = capsys.readouterr()

        assert "АНАЛИЗ ВАКАНСИЙ HH.RU" in captured.out
        assert "1. Показать компании" in captured.out
        assert "0. Выход" in captured.out

    def test_run_interface_exit(self):
        """Тест: выход из интерфейса"""
        mock_db = Mock()

        with patch("builtins.input", side_effect=["0"]):
            run_interface(mock_db)

        # Если не упало — тест прошёл

    def test_run_interface_invalid_choice(self):
        """Тест: неверный выбор меню"""
        mock_db = Mock()
        mock_db.get_companies_and_vacancies_count.return_value = []

        with patch("builtins.input", side_effect=["99", "", "0", ""]):
            run_interface(mock_db)

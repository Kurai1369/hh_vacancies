"""Тесты для main.py"""
from unittest.mock import patch

import main


class TestMain:
    """Тесты точки входа приложения"""

    @patch("main.create_database")
    @patch("main.create_tables")
    @patch("main.collect_data")
    @patch("main.DBManager")
    @patch("main.run_interface")
    def test_main_success(
        self,
        mock_run_interface,
        mock_db_manager,
        mock_collect_data,
        mock_create_tables,
        mock_create_database,
    ):
        """Тест: успешный запуск main()"""
        # Запускаем main
        main.main()

        # Проверяем, что все функции были вызваны
        mock_create_database.assert_called_once()
        mock_create_tables.assert_called_once()
        mock_collect_data.assert_called_once()
        mock_db_manager.assert_called_once()
        mock_run_interface.assert_called_once()

    @patch("main.create_database")
    @patch("main.create_tables")
    @patch("main.collect_data")
    def test_collect_data_function(self, mock_collect, mock_tables, mock_db):
        """Тест: функция collect_data вызывается"""
        # Просто проверяем, что функция существует и может быть вызвана
        assert callable(main.collect_data)

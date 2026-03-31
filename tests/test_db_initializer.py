"""Тесты для db_initializer."""
from unittest.mock import MagicMock, patch

from src.database.db_initializer import create_database, create_tables


class TestDatabaseInitializer:
    """Тесты инициализации базы данных"""

    def test_create_database_new(self):
        """Тест: создание новой базы данных"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None  # БД не существует
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None
        mock_conn.autocommit = True

        with patch(
            "src.database.db_initializer.psycopg2.connect", return_value=mock_conn
        ):
            create_database("test_db")

        assert mock_cursor.execute.called

    def test_create_database_exists(self):
        """Тест: база данных уже существует"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None
        mock_conn.autocommit = True

        with patch(
            "src.database.db_initializer.psycopg2.connect", return_value=mock_conn
        ):
            create_database("existing_db")

        calls = [str(call) for call in mock_cursor.execute.call_args_list]
        assert not any("CREATE DATABASE" in c for c in calls)

    def test_create_tables(self):
        """Тест: создание таблиц."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        with patch(
            "src.database.db_initializer.psycopg2.connect", return_value=mock_conn
        ):
            create_tables()

        assert mock_cursor.execute.call_count >= 2

"""Тесты для конфигурации"""
from src.config import Config


class TestConfig:
    """Тесты конфигурации приложения"""

    def test_config_db_host_default(self):
        """Тест: хост БД по умолчанию"""
        assert Config.DB_HOST == "localhost"

    def test_config_db_port_default(self):
        """Тест: порт БД по умолчанию"""
        assert Config.DB_PORT == 5432

    def test_config_db_name_default(self):
        """Тест: имя БД по умолчанию"""
        assert Config.DB_NAME == "hh_vacancies_db"

    def test_config_get_dsn(self):
        """Тест: получение DSN строки"""
        dsn = Config.get_dsn()

        assert "host=" in dsn
        assert "port=" in dsn
        assert "dbname=" in dsn
        assert "user=" in dsn
        assert "password=" in dsn

    def test_config_hh_api_url(self):
        """Тест: URL API hh.ru"""
        assert Config.HH_API_BASE_URL == "https://api.hh.ru"

    def test_config_user_agent_not_empty(self):
        """Тест: User-Agent не пустой"""
        assert len(Config.HH_USER_AGENT) > 0
        assert "Mozilla" in Config.HH_USER_AGENT or "HH" in Config.HH_USER_AGENT

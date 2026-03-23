"""Конфигурация приложения."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Конфигурация приложения"""

    # Настройки БД
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "hh_vacancies_db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    @classmethod
    def get_dsn(cls) -> str:
        """Возвращает DSN для подключения к БД"""
        return (
            f"host={cls.DB_HOST} "
            f"port={cls.DB_PORT} "
            f"dbname={cls.DB_NAME} "
            f"user={cls.DB_USER} "
            f"password={cls.DB_PASSWORD}"
        )

    # Настройки API
    HH_API_BASE_URL: str = os.getenv("HH_API_BASE_URL", "https://api.hh.ru")

    # Используем браузерный User-Agent, чтобы hh.ru не блокировал запросы
    # Формат из документации: Приложение/Версия (контакт)
    # Но если блокируют — используем реалистичный браузерный заголовок
    HH_USER_AGENT: str = os.getenv(
        "HH_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )

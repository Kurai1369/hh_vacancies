"""Модуль для инициализации базы данных и таблиц"""

import psycopg2
from psycopg2 import sql

from src.config import Config


def create_database(db_name: str) -> None:
    """
    Создаёт базу данных, если она не существует.

    :param db_name: имя базы данных
    """
    # Подключаемся к postgres для создания БД
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname="postgres",
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
    )
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"✅ База данных '{db_name}' создана")
        else:
            print(f"ℹ️ База данных '{db_name}' уже существует")

    conn.close()


def create_tables() -> None:
    """
    Создаёт таблицы companies и vacancies с внешним ключом
    """
    with psycopg2.connect(dsn=Config.get_dsn()) as conn:
        with conn.cursor() as cur:
            # Таблица компаний
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    hh_id INTEGER UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(500) NOT NULL,
                    logo_url VARCHAR(500),
                    description TEXT,
                    site_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # Таблица вакансий с внешним ключом
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    hh_id INTEGER UNIQUE NOT NULL,
                    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(500) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    salary_currency VARCHAR(10),
                    salary_gross BOOLEAN,
                    description TEXT,
                    experience VARCHAR(100),
                    employment VARCHAR(100),
                    area_name VARCHAR(100),
                    published_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # Индексы для ускорения поиска
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_vacancies_company_id
                ON vacancies(company_id);
            """
            )
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_vacancies_name
                ON vacancies USING gin(to_tsvector('russian', name));
            """
            )

            conn.commit()
            print("✅ Таблицы созданы")

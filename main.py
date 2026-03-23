"""Точка входа в приложение"""

#import logging

from src.api.hh_client import HHClient
from src.cli.interface import run_interface
from src.config import Config
from src.database.db_initializer import create_database, create_tables
from src.database.db_manager import DBManager

#logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

# Список ID компаний для сбора данных
# проверенные employer_id (актуальные на 2026)
# Получены через https://api.hh.ru/employers?text=яндекс&per_page=5
TARGET_EMPLOYERS = [
    158720,
    780654,
    924205,
    8434,
    776314,
    5920492,
    599429,
    40493,
    840485,
    5694,
]


def collect_data() -> None:
    """Собирает данные с API и сохраняет в БД"""
    print("🔄 Запуск сбора данных...")

    client = HHClient()
    db = DBManager()

    for emp_id in TARGET_EMPLOYERS:
        print(f"📥 Обработка работодателя #{emp_id}...")

        # Получаем компанию
        company = client.get_employer(emp_id)
        if not company:
            continue

        # Сохраняем компанию и получаем её ID в БД
        company_db_id = db.insert_company(company)

        # Получаем и сохраняем вакансии
        vacancies = client.get_employer_vacancies(emp_id)
        for vac in vacancies:
            db.insert_vacancy(vac, company_db_id)

        print(f"✅ {company.name}: {len(vacancies)} вакансий сохранено")

    print("🎉 Сбор данных завершён!")


def main() -> None:
    """Основная функция приложения"""
    # 1. Создаём БД и таблицы
    print("🗄️ Инициализация базы данных...")
    create_database(Config.DB_NAME)
    create_tables()

    # 2. Собираем данные (можно закомментировать после первого запуска)
    collect_data()

    # 3. Запускаем пользовательский интерфейс
    db_manager = DBManager()
    run_interface(db_manager)


if __name__ == "__main__":
    main()

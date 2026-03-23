"""Пользовательский интерфейс для взаимодействия с данными"""

from typing import Optional

from src.database.db_manager import DBManager


def format_salary(
    from_val: Optional[int], to_val: Optional[int], currency: Optional[str]
) -> str:
    """Форматирует зарплату в человекочитаемый вид"""
    if from_val is None and to_val is None:
        return "Зарплата не указана"

    currency = currency or "RUR"
    if from_val and to_val and from_val == to_val:
        return f"{from_val:,} {currency}"
    elif from_val and to_val:
        return f"{from_val:,} – {to_val:,} {currency}"
    elif from_val:
        return f"от {from_val:,} {currency}"
    else:
        return f"до {to_val:,} {currency}"


def show_menu() -> None:
    """Отображает главное меню"""
    print("\n" + "=" * 60)
    print("📊 АНАЛИЗ ВАКАНСИЙ HH.RU")
    print("=" * 60)
    print("1. Показать компании и количество вакансий")
    print("2. Показать все вакансии")
    print("3. Показать среднюю зарплату")
    print("4. Показать вакансии с зарплатой выше средней")
    print("5. Поиск вакансий по ключевому слову")
    print("0. Выход")
    print("-" * 60)


def run_interface(db_manager: DBManager) -> None:
    """
    Запускает интерактивный интерфейс

    :param db_manager: экземпляр DBManager
    """
    while True:
        show_menu()
        choice = input("Выберите пункт меню (0-5): ").strip()

        if choice == "1":
            print("\n📋 Компании и количество вакансий:")
            for item in db_manager.get_companies_and_vacancies_count():
                print(
                    f"  • {item['company_name']}: "
                    f"{item['vacancies_count']} вакансий"
                )

        elif choice == "2":
            print("\n📋 Все вакансии (первые 20):")
            all_vacancies = db_manager.get_all_vacancies()
            for vacancy in all_vacancies[:20]:
                salary = format_salary(
                    vacancy["salary_from"],
                    vacancy["salary_to"],
                    vacancy["salary_currency"],
                )
                print(f"  • {vacancy['vacancy_name']} " f"в {vacancy['company_name']}")
                print(f"    💰 {salary} | 🔗 {vacancy['vacancy_url']}\n")

        elif choice == "3":
            avg = db_manager.get_avg_salary()
            if avg:
                print(f"\n💰 Средняя зарплата: {avg:,.0f} RUB")
            else:
                print("\n⚠️ Нет данных о зарплатах")

        elif choice == "4":
            print("\n🔥 Вакансии с зарплатой выше средней (первые 10):")
            for vacancy in db_manager.get_vacancies_with_higher_salary()[:10]:
                salary = format_salary(
                    vacancy["salary_from"],
                    vacancy["salary_to"],
                    vacancy["salary_currency"],
                )
                print(f"  • {vacancy['vacancy_name']} " f"в {vacancy['company_name']}")
                print(f"    💰 {salary}\n")

        elif choice == "5":
            keyword = input("Введите ключевое слово (например, python): ").strip()
            if keyword:
                results = db_manager.get_vacancies_with_keyword(keyword)
                print(
                    f"\n🔍 Найдено вакансий по запросу '{keyword}': " f"{len(results)}"
                )
                for vacancy in results[:10]:
                    salary = format_salary(
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["salary_currency"],
                    )
                    print(
                        f"  • {vacancy['vacancy_name']} " f"в {vacancy['company_name']}"
                    )
                    print(f"    💰 {salary}\n")

        elif choice == "0":
            print("\n👋 До свидания!")
            break

        else:
            print("\n⚠️ Неверный выбор, попробуйте снова")

        input("\nНажмите Enter для продолжения...")

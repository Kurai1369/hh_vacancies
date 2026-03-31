"""Тесты для моделей данных"""
from src.models.company import Company
from src.models.vacancy import Vacancy


class TestCompany:
    """Тесты модели Company"""

    def test_company_creation(self):
        """Тест: создание компании"""
        company = Company(
            hh_id=123, name="Test Company", url="https://hh.ru/employer/123"
        )

        assert company.hh_id == 123
        assert company.name == "Test Company"
        assert company.url == "https://hh.ru/employer/123"
        assert company.logo_url is None
        assert company.description is None

    def test_company_from_api_dict(self):
        """Тест: создание компании из ответа API"""
        api_data = {
            "id": 456,
            "name": "Yandex",
            "alternate_url": "https://hh.ru/employer/456",
            "url": "https://api.hh.ru/employers/456",
            "logo_urls": {"original": "https://logo.png", "90": "https://logo_90.png"},
            "description": "Test description",
            "site_url": "https://yandex.ru",
        }

        company = Company.from_api_dict(api_data)

        assert company.hh_id == 456
        assert company.name == "Yandex"
        assert company.logo_url == "https://logo.png"
        assert company.description == "Test description"
        assert company.site_url == "https://yandex.ru"

    def test_company_from_api_dict_minimal(self):
        """Тест: создание компании из минимального ответа API"""
        api_data = {"id": 789, "name": "Minimal Company"}

        company = Company.from_api_dict(api_data)

        assert company.hh_id == 789
        assert company.name == "Minimal Company"
        assert company.url == ""


class TestVacancy:
    """Тесты модели Vacancy"""

    def test_vacancy_creation(self):
        """Тест: создание вакансии"""
        vacancy = Vacancy(
            hh_id=123,
            name="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
        )

        assert vacancy.hh_id == 123
        assert vacancy.name == "Python Developer"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000

    def test_vacancy_from_api_dict(self):
        """Тест: создание вакансии из ответа API"""
        api_data = {
            "id": 456,
            "name": "Java Developer",
            "alternate_url": "https://hh.ru/vacancy/456",
            "salary": {"from": 200000, "to": 300000, "currency": "RUR", "gross": True},
            "description": "Test description",
            "experience": {"name": "More than 3 years"},
            "employment": {"name": "Full time"},
            "area": {"name": "Moscow"},
            "published_at": "2024-01-01T10:00:00+0000",
        }

        vacancy = Vacancy.from_api_dict(api_data)

        assert vacancy.hh_id == 456
        assert vacancy.name == "Java Developer"
        assert vacancy.salary_from == 200000
        assert vacancy.salary_to == 300000
        assert vacancy.salary_currency == "RUR"
        assert vacancy.experience == "More than 3 years"
        assert vacancy.employment == "Full time"
        assert vacancy.area_name == "Moscow"

    def test_vacancy_from_api_dict_no_salary(self):
        """Тест: создание вакансии без зарплаты"""
        api_data = {
            "id": 789,
            "name": "Intern",
            "alternate_url": "https://hh.ru/vacancy/789",
            "salary": None,
        }

        vacancy = Vacancy.from_api_dict(api_data)

        assert vacancy.salary_from is None
        assert vacancy.salary_to is None

    def test_vacancy_from_api_dict_invalid_date(self):
        """Тест: создание вакансии с некорректной датой"""
        api_data = {
            "id": 101,
            "name": "Test",
            "alternate_url": "https://hh.ru/vacancy/101",
            "published_at": "invalid-date",
        }

        vacancy = Vacancy.from_api_dict(api_data)

        assert vacancy.published_at is None

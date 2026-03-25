"""Тесты для HHClient"""
from unittest.mock import Mock, patch

import requests

from src.api.hh_client import HHClient
from src.models.company import Company


class TestHHClient:
    """Тесты клиента hh.ru API"""

    def test_client_initialization(self):
        """Тест: инициализация клиента"""
        client = HHClient()
        assert client.base_url == "https://api.hh.ru"
        assert client.session is not None

    def test_get_employer_success(self):
        """Тест: успешное получение работодателя"""
        client = HHClient()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 123,
            "name": "Test Company",
            "alternate_url": "https://hh.ru/employer/123",
            "description": "Test",
            "site_url": "https://test.com",
        }
        mock_response.text = '{"id": 123, "name": "Test"}'

        with patch.object(client.session, "get", return_value=mock_response):
            result = client.get_employer(123)

        assert result is not None
        assert isinstance(result, Company)
        assert result.hh_id == 123

    def test_get_employer_404(self):
        """Тест: работодатель не найден (404)"""
        client = HHClient()
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        with patch.object(client.session, "get", return_value=mock_response):
            result = client.get_employer(999)

        assert result is None

    def test_get_employer_400(self):
        """Тест: ошибка запроса (400)"""
        client = HHClient()
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"

        with patch.object(client.session, "get", return_value=mock_response):
            result = client.get_employer(123)

        assert result is None

    def test_get_employer_request_exception(self):
        """Тест: исключение при запросе"""
        client = HHClient()
        with patch.object(
            client.session, "get", side_effect=requests.RequestException("Error")
        ):
            result = client.get_employer(123)
        assert result is None

    def test_get_employer_vacancies_success(self):
        """Тест: успешное получение вакансий"""
        client = HHClient()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "id": 1,
                    "name": "Developer",
                    "alternate_url": "https://hh.ru/vacancy/1",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "published_at": "2024-01-01T00:00:00+0000",
                }
            ],
            "pages": 1,
            "page": 0,
            "per_page": 100,
            "found": 1,
        }
        mock_response.text = '{"items": [...]}'

        with patch.object(client.session, "get", return_value=mock_response):
            result = client.get_employer_vacancies(123)

        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_employer_vacancies_empty(self):
        """Тест: пустой список вакансий"""
        client = HHClient()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_response.text = '{"items": []}'

        with patch.object(client.session, "get", return_value=mock_response):
            result = client.get_employer_vacancies(123)

        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_employer_vacancies_400(self):
        """Тест: ошибка при получении вакансий"""
        client = HHClient()
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"

        with patch.object(client.session, "get", return_value=mock_response):
            result = client.get_employer_vacancies(123)

        assert isinstance(result, list)
        assert len(result) == 0

from typing import Any, Dict, List
import allure

from src.endpoints.base_endpoint import BaseEndpoint

class GetItemEndpoint(BaseEndpoint):
    """Ручка получения объявления"""

    @allure.step("Получаем объявление по Id: {item_id}")
    def action(self, item_id: str) -> List[Dict[str, Any]]:
        """Получения объявления по Id"""
        self.response = self.session.get(f"{self.base_url}/api/1/item/{item_id}")
        self.response_json = self.response.json() if self.response.text else []
        self.check_status_code(200)
        return self.response_json

    @allure.step("Получаем объявление по Id (Ожидаем, что не найдет): {item_id}")
    def action_expect_not_found(self, item_id: str) -> None:
        """Попытка получить объявление с ошибкой 404"""
        self.response = self.session.get(f"{self.base_url}/api/1/item/{item_id}")
        self.check_status_code(404)

    @allure.step("Получаем объявление по Id (Ожидаем, что запрос плохой): {item_id}")
    def action_expect_bad_request(self, item_id: str) -> None:
        """Попытка получить объявление с плохим запросом"""
        self.response = self.session.get(f"{self.base_url}/api/1/item/{item_id}")
        self.check_status_code(400)
from typing import Any, Dict, List
import allure

from src.endpoints.base_endpoint import BaseEndpoint

class GetStatisticEndpoint(BaseEndpoint):
    """Ручка для получения статистики"""

    @allure.step("Получить статистику по Id: {item_id}")
    def action(self, item_id: str) -> List[Dict[str, Any]]:
        """Получить статистику по Id"""
        self.response = self.session.get(f"{self.base_url}/api/2/statistic/{item_id}")
        self.response_json = self.response.json() if self.response.text else []
        self.check_status_code(200)
        return self.response_json

    @allure.step("Получить статистику по Id (Ожидаем, что Id нет такого): {item_id}")
    def action_expect_not_found(self, item_id: str) -> None:
        """Получаем статистику с ошибкой 404"""
        self.response = self.session.get(f"{self.base_url}/api/2/statistic/{item_id}")
        self.check_status_code(404)

    @allure.step("Получить статистику по Id (Ожидаем, что запрос плохой): {item_id}")
    def action_expect_bad_request(self, item_id: str) -> None:
        """Получаем статистику с ошибкой 400"""
        self.response = self.session.get(f"{self.base_url}/api/2/statistic/{item_id}")
        self.check_status_code(400)
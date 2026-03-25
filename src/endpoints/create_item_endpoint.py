from typing import Any, Dict
import allure

from src.endpoints.base_endpoint import BaseEndpoint

class CreateItemEndpoint(BaseEndpoint):
    """Ручка для создания объявлений"""

    @allure.step("Create new item")
    def action(self, payload: Dict[str, Any]) -> str:
        """Создание объявления и получение его Id"""
        self.response = self.session.post(
            f"{self.base_url}/api/1/item",
            json=payload,
        )
        self.response_json = self.response.json() if self.response.text else {}
        self.check_status_code(200)
        item_id = self.extract_item_id()
        assert item_id, "Не получилось получить Id"
        return item_id

    @allure.step("Создание нового объявления с ошибкой (expecting error)")
    def action_expect_error(self, payload: Dict[str, Any], expected_code: int) -> Dict[str, Any]:
        """Create an item expecting error."""
        self.response = self.session.post(
            f"{self.base_url}/api/1/item",
            json=payload,
        )
        self.response_json = self.response.json() if self.response.text else {}
        self.check_status_code(expected_code)
        return self.response_json
from typing import Any, Dict, List
import allure

from src.endpoints.base_endpoint import BaseEndpoint

class GetItemsBySellerEndpoint(BaseEndpoint):
    """Ручка для получения объявлений по Id продавца"""

    @allure.step("Получает список объявлений по Id продавца: {seller_id}")
    def action(self, seller_id: int) -> List[Dict[str, Any]]:
        """Получение объявлений по Id продавца"""
        self.response = self.session.get(f"{self.base_url}/api/1/{seller_id}/item")
        self.response_json = self.response.json() if self.response.text else []
        self.check_status_code(200)
        return self.response_json

    @allure.step("Получаем список объявлений, но запрос плохой: {seller_id}")
    def action_expect_bad_request(self, seller_id: str) -> None:
        """Получение объявлений с ошибкой 400 - Bad Request"""
        self.response = self.session.get(f"{self.base_url}/api/1/{seller_id}/item")
        self.check_status_code(400)
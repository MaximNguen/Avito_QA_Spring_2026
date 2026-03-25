import allure
from src.endpoints.base_endpoint import BaseEndpoint

class DeleteItemEndpoint(BaseEndpoint):
    """Ручка для удаления объявлений"""

    @allure.step("Удаляем объявление по Id: {item_id}")
    def action(self, item_id: str) -> None:
        """Удаление объявления по Id"""
        self.response = self.session.delete(f"{self.base_url}/api/2/item/{item_id}")
        self.check_status_code(200)

    @allure.step("Удаляем объявление по id, но по id нет такого: {item_id}")
    def action_expect_not_found(self, item_id: str) -> None:
        """Удаление объявления по Id с ошибкой 404"""
        self.response = self.session.delete(f"{self.base_url}/api/2/item/{item_id}")
        self.check_status_code(404)

    @allure.step("Удаляем объявление по id, но запрос плохой: {item_id}")
    def action_expect_bad_request(self, item_id: str) -> None:
        """Удаление объявления по Id с ошибкой 400"""
        self.response = self.session.delete(f"{self.base_url}/api/2/item/{item_id}")
        self.check_status_code(400)

    @allure.step("Подтверждаем, что удалили: {item_id}")
    def verify_deleted(self, item_id: str) -> None:
        """Подтверждение удаления"""
        self.response = self.session.get(f"{self.base_url}/api/1/item/{item_id}")
        self.check_status_code(404)
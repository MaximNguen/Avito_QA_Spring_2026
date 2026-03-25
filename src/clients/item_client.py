from typing import Any, Dict, Optional

from src.clients.base_client import BaseClient


class ItemClient(BaseClient):
    """API запросы для ручек"""

    def create_item(self, payload: Dict[str, Any]) -> Any:
        """Создать объявление"""
        return self.request("POST", "/api/1/item", json=payload)

    def get_item_by_id(self, item_id: str) -> Any:
        """Получить по ID"""
        return self.request("GET", f"/api/1/item/{item_id}")

    def get_items_by_seller(self, seller_id: int) -> Any:
        """Получить по ID продавца"""
        return self.request("GET", f"/api/1/{seller_id}/item")

    def delete_item(self, item_id: str) -> Any:
        """Удалить по ID"""
        return self.request("DELETE", f"/api/2/item/{item_id}")

    def get_statistic(self, item_id: str) -> Any:
        """Получить статистику"""
        return self.request("GET", f"/api/2/statistic/{item_id}")
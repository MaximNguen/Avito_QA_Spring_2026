from typing import Any

from src.clients.base_client import BaseClient

class StatisticClient(BaseClient):
    """API запросы для статистики"""

    def get_statistic(self, item_id: str) -> Any:
        """Get statistics by item identifier."""
        return self.request("GET", f"/api/2/statistic/{item_id}")
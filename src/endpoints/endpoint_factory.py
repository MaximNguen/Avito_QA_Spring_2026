from typing import Dict, Optional, Type

from src.endpoints.base_endpoint import BaseEndpoint
from src.endpoints.create_item_endpoint import CreateItemEndpoint
from src.endpoints.delete_item_endpoint import DeleteItemEndpoint
from src.endpoints.get_item_endpoint import GetItemEndpoint
from src.endpoints.get_items_by_seller_endpoint import GetItemsBySellerEndpoint
from src.endpoints.get_statistic_endpoint import GetStatisticEndpoint

class EndpointFactory:
    """Класс-фабрика для контроля ручек - Page Factory паттерн"""

    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url
        self._cache: Dict[str, BaseEndpoint] = {}

    def _get_endpoint(self, endpoint_class: Type[BaseEndpoint], name: str) -> BaseEndpoint:
        if name not in self._cache:
            self._cache[name] = (
                endpoint_class(self.base_url) if self.base_url else endpoint_class()
            )
        return self._cache[name]

    def create_endpoint(self) -> CreateItemEndpoint:
        return self._get_endpoint(CreateItemEndpoint, "create")

    def get_endpoint(self) -> GetItemEndpoint:
        return self._get_endpoint(GetItemEndpoint, "get")

    def get_all_endpoint(self) -> GetItemsBySellerEndpoint:
        return self._get_endpoint(GetItemsBySellerEndpoint, "get_all")

    def get_stat_endpoint(self) -> GetStatisticEndpoint:
        return self._get_endpoint(GetStatisticEndpoint, "stat")

    def delete_endpoint(self) -> DeleteItemEndpoint:
        return self._get_endpoint(DeleteItemEndpoint, "delete")

    def clear_cache(self) -> None:
        self._cache.clear()
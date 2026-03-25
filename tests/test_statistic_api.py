import uuid

import allure

from src.clients.item_client import ItemClient
from src.clients.statistic_client import StatisticClient
from src.utils.payloads import build_item_payload


@allure.feature("Statistic API")
@allure.story("Statistics операции")
class TestStatisticAPI:
    """Тесты для ручек статистики."""

    @allure.title("Успешное получение статистики")
    def test_get_statistic_success(
        self,
        item_client: ItemClient,
        statistic_client: StatisticClient,
    ) -> None:
        payload = build_item_payload()
        create_response = item_client.create_item(payload)
        assert create_response.status_code == 200

        create_data = create_response.json()
        if isinstance(create_data, dict) and "id" in create_data:
            item_id = create_data["id"]
        elif isinstance(create_data, dict) and "status" in create_data:
            import re

            match = re.search(
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                create_data["status"],
            )
            item_id = match.group(0) if match else None
        else:
            item_id = None

        assert item_id

        try:
            stat_response = statistic_client.get_statistic(item_id)
            assert stat_response.status_code == 200
            stats = stat_response.json()
            assert isinstance(stats, list)
            assert stats
            assert set(stats[0].keys()) == {"likes", "viewCount", "contacts"}
        finally:
            item_client.delete_item(item_id)

    @allure.title("Не найдены статистики")
    def test_get_statistic_not_found(self, statistic_client: StatisticClient) -> None:
        response = statistic_client.get_statistic(str(uuid.uuid4()))
        assert response.status_code == 404

    @allure.title("Получение статистики по неверному формату")
    def test_get_statistic_invalid_format(self, statistic_client: StatisticClient) -> None:
        response = statistic_client.get_statistic("invalid-id")
        assert response.status_code == 404

    @allure.title("Получение статистики - пустой ID")
    def test_get_statistic_empty_id(self, statistic_client: StatisticClient) -> None:
        response = statistic_client.get_statistic("")
        assert response.status_code == 404
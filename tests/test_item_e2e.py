import allure

from src.clients.item_client import ItemClient
from src.clients.statistic_client import StatisticClient
from src.utils.generators import Generator
from src.utils.payloads import build_item_payload

@allure.feature("Avito API")
@allure.story("End-to-end тестирование")
class TestItemFlow:
    """E2E Тест-класс для показа полного жизненного цикла объявления"""

    @allure.title("Полный цикл: create -> get -> stats -> delete")
    def test_complete_item_lifecycle(
        self,
        item_client: ItemClient,
        statistic_client: StatisticClient,
    ) -> None:
        """Создаем, ловим, читаем, удаляем"""
        with allure.step("Создаем объявление"):
            payload = build_item_payload()
            create_response = item_client.create_item(payload)
            assert create_response.status_code == 200

            with allure.step("Ловим Id"):
                data = create_response.json()
                if isinstance(data, dict) and "id" in data:
                    item_id = data["id"]
                else:
                    import re

                    match = re.search(
                        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                        str(data.get("status", "")),
                    )
                    item_id = match.group(0) if match else None

                assert item_id

            with allure.step(f"Получаем данные по id: {item_id}"):
                get_response = item_client.get_item_by_id(item_id)
                assert get_response.status_code == 200
                items = get_response.json()
                assert isinstance(items, list)
                assert len(items) > 0
                assert items[0]["id"] == item_id

            with allure.step(f"Получаем статистику по Id: {item_id}"):
                stat_response = statistic_client.get_statistic(item_id)
                assert stat_response.status_code == 200
                stats = stat_response.json()
                assert isinstance(stats, list)
                assert "likes" in stats[0]
                assert "viewCount" in stats[0]
                assert "contacts" in stats[0]

            with allure.step(f"Удаляем объявление по id: {item_id}"):
                delete_response = item_client.delete_item(item_id)
                assert delete_response.status_code == 200

            with allure.step(f"Подтверждаем, что по Id {item_id} объявление удален"):
                missing_response = item_client.get_item_by_id(item_id)
                assert missing_response.status_code == 404

    @allure.title("Создание нескольких объявлений для одного продавца")
    def test_multiple_items_for_seller(
            self,
            item_client: ItemClient,
    ) -> None:
        """Create multiple items for same seller and verify all are returned."""
        seller_id = Generator.generate_seller_id()
        item_ids = []

        with allure.step(f"Создание 3 объявлений для продавца {seller_id}"):
            for i in range(3):
                payload = build_item_payload(seller_id=seller_id)
                response = item_client.create_item(payload)
                assert response.status_code == 200

                data = response.json()
                if isinstance(data, dict) and "id" in data:
                    item_id = data["id"]
                elif isinstance(data, dict) and "status" in data:
                    import re
                    match = re.search(
                        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                        data["status"],
                    )
                    item_id = match.group(0) if match else None
                else:
                    item_id = None

                assert item_id
                item_ids.append(item_id)

        try:
            with allure.step(f"Получение всех объявлений продавца {seller_id}"):
                get_response = item_client.get_items_by_seller(seller_id)
                assert get_response.status_code == 200
                items = get_response.json()
                assert isinstance(items, list)
                assert len(items) == 3

                # Verify all created items are in response
                returned_ids = [item["id"] for item in items]
                for item_id in item_ids:
                    assert item_id in returned_ids

        finally:
            with allure.step("Очистка - удаление всех созданных объявлений"):
                for item_id in item_ids:
                    item_client.delete_item(item_id)

    @allure.title("Создание и удаление нескольких объявлений")
    def test_create_and_delete_multiple_items(
            self,
            item_client: ItemClient,
    ) -> None:
        seller_id = Generator.generate_seller_id()
        item_ids = []

        with allure.step("Создание 5 объявлений"):
            for i in range(5):
                payload = build_item_payload(seller_id=seller_id)
                response = item_client.create_item(payload)
                assert response.status_code == 200

                data = response.json()
                if isinstance(data, dict) and "id" in data:
                    item_id = data["id"]
                elif isinstance(data, dict) and "status" in data:
                    import re
                    match = re.search(
                        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                        data["status"],
                    )
                    item_id = match.group(0) if match else None
                else:
                    item_id = None

                assert item_id
                item_ids.append(item_id)

        with allure.step("Удаление всех объявлений"):
            for item_id in item_ids:
                delete_response = item_client.delete_item(item_id)
                assert delete_response.status_code == 200

        with allure.step("Проверка удаления всех объявлений"):
            for item_id in item_ids:
                get_response = item_client.get_item_by_id(item_id)
                assert get_response.status_code == 404
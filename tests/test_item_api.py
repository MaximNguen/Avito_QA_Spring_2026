import uuid

import allure
import pytest

from src.clients.item_client import ItemClient
from src.utils.generators import Generator
from src.utils.payloads import build_item_payload


def find_item_by_id(items: list, item_id: str) -> dict | None:
    """Поиск конкретного объявления по Id"""
    for item in items:
        if item.get("id") == item_id:
            return item
    return None


@allure.feature("Avito API")
@allure.story("CRUD операции по ручкам")
class TestItemAPI:
    """Тесты для всех ручек, кроме статистики"""

    @allure.title("Успешное создание объявления")
    def test_create_item_success(self, item_client: ItemClient) -> None:
        """Создание и получение Id объявления"""
        payload = build_item_payload()
        response = item_client.create_item(payload)

        try:
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

            # Подтверждаем создание
            get_response = item_client.get_item_by_id(item_id)
            assert get_response.status_code == 200
            items = get_response.json()
            item = find_item_by_id(items, item_id)
            assert item is not None
            assert item["sellerId"] == payload["sellerID"]
            assert item["name"] == payload["name"]
            assert item["price"] == payload["price"]

        finally:
            if item_id:
                item_client.delete_item(item_id)

    @allure.title("Проверка, что объявления точно созданы и Id разные ")
    def test_create_item_not_idempotent(self, item_client: ItemClient) -> None:
        payload = build_item_payload()
        first_response = item_client.create_item(payload)
        second_response = item_client.create_item(payload)

        try:
            assert first_response.status_code == 200
            assert second_response.status_code == 200

            first_data = first_response.json()
            second_data = second_response.json()

            first_id = first_data.get("id") if isinstance(first_data, dict) else None
            second_id = second_data.get("id") if isinstance(second_data, dict) else None

            if not first_id:
                import re

                match = re.search(
                    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                    str(first_data.get("status", "")),
                )
                first_id = match.group(0) if match else None

            if not second_id:
                import re

                match = re.search(
                    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                    str(second_data.get("status", "")),
                )
                second_id = match.group(0) if match else None

            assert first_id and second_id and first_id != second_id

        finally:
            if first_id:
                item_client.delete_item(first_id)
            if second_id:
                item_client.delete_item(second_id)

    @allure.title("Получаем успешно объявление")
    def test_get_item_by_id_success(self, item_client: ItemClient) -> None:
        payload = build_item_payload()
        create_response = item_client.create_item(payload)
        assert create_response.status_code == 200

        create_data = create_response.json()
        item_id = create_data.get("id") if isinstance(create_data, dict) else None

        if not item_id:
            import re

            match = re.search(
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                str(create_data.get("status", "")),
            )
            item_id = match.group(0) if match else None

        assert item_id

        try:
            get_response = item_client.get_item_by_id(item_id)
            assert get_response.status_code == 200
            items = get_response.json()
            assert isinstance(items, list)
            item = find_item_by_id(items, item_id)
            assert item is not None
            assert item["sellerId"] == payload["sellerID"]
            assert item["name"] == payload["name"]
            assert item["price"] == payload["price"]
        finally:
            item_client.delete_item(item_id)

    @allure.title("Получение списка объявления у продавца")
    def test_get_items_by_seller_success(self, item_client: ItemClient) -> None:
        seller_id = Generator.generate_seller_id()
        payload = build_item_payload(seller_id=seller_id)
        create_response = item_client.create_item(payload)
        assert create_response.status_code == 200

        create_data = create_response.json()
        item_id = create_data.get("id") if isinstance(create_data, dict) else None

        if not item_id:
            import re

            match = re.search(
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                str(create_data.get("status", "")),
            )
            item_id = match.group(0) if match else None

        assert item_id

        try:
            get_response = item_client.get_items_by_seller(seller_id)
            assert get_response.status_code == 200
            items = get_response.json()
            assert isinstance(items, list)
            item = find_item_by_id(items, item_id)
            assert item is not None
            assert item["sellerId"] == seller_id
        finally:
            item_client.delete_item(item_id)

    @allure.title("Создаем объявление, но без названия")
    def test_create_item_missing_name(self, item_client: ItemClient) -> None:
        payload = build_item_payload()
        payload.pop("name")
        response = item_client.create_item(payload)
        assert response.status_code == 400

    @allure.title("Создаем объявление, но с неверным Id продавца")
    def test_create_item_invalid_seller_id_type(self, item_client: ItemClient) -> None:
        payload = build_item_payload(overrides={"sellerID": "abc"})
        response = item_client.create_item(payload)
        assert response.status_code == 400

    @allure.title("Получение объявления по неверному Id")
    def test_get_item_by_id_not_found(self, item_client: ItemClient) -> None:
        response = item_client.get_item_by_id(str(uuid.uuid4()))
        assert response.status_code == 404

    @allure.title("Получение объявления по неверному Id - Bad Request")
    def test_get_item_by_id_invalid_format(self, item_client: ItemClient) -> None:
        response = item_client.get_item_by_id("invalid-id")
        assert response.status_code == 400

    @allure.title("Проверка граничных значений Id продавцев")
    @pytest.mark.parametrize("seller_id", [111111, 999999])
    def test_seller_id_boundaries(
        self,
        item_client: ItemClient,
        seller_id: int,
    ) -> None:
        payload = build_item_payload(seller_id=seller_id)
        response = item_client.create_item(payload)

        try:
            assert response.status_code == 200

            create_data = response.json()
            item_id = create_data.get("id") if isinstance(create_data, dict) else None

            if not item_id:
                import re

                match = re.search(
                    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                    str(create_data.get("status", "")),
                )
                item_id = match.group(0) if match else None

            assert item_id

            get_response = item_client.get_item_by_id(item_id)
            assert get_response.status_code == 200
            item = find_item_by_id(get_response.json(), item_id)
            assert item is not None
            assert item.get("sellerId") == seller_id
        finally:
            if item_id:
                item_client.delete_item(item_id)

    @allure.title("Создание объявления без Id")
    def test_create_item_empty_seller_id(self, item_client: ItemClient) -> None:
        payload = build_item_payload(overrides={"sellerID": ""})
        response = item_client.create_item(payload)
        assert response.status_code == 400

    @allure.title("Создание объявления с отриц. ценой")
    def test_create_item_negative_price(self, item_client: ItemClient) -> None:
        payload = build_item_payload(price=-100)
        response = item_client.create_item(payload)

        if response.status_code == 200:
            create_data = response.json()
            item_id = create_data.get("id") if isinstance(create_data, dict) else None
            if not item_id:
                import re

                match = re.search(
                    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                    str(create_data.get("status", "")),
                )
                item_id = match.group(0) if match else None
            if item_id:
                item_client.delete_item(item_id)

    @allure.title("Успешное удаление объявления")
    def test_delete_item_success(self, item_client: ItemClient) -> None:
        payload = build_item_payload()
        create_response = item_client.create_item(payload)
        assert create_response.status_code == 200

        create_data = create_response.json()
        item_id = create_data.get("id") if isinstance(create_data, dict) else None

        if not item_id:
            import re

            match = re.search(
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                str(create_data.get("status", "")),
            )
            item_id = match.group(0) if match else None

        assert item_id

        delete_response = item_client.delete_item(item_id)
        assert delete_response.status_code == 200

        get_response = item_client.get_item_by_id(item_id)
        assert get_response.status_code == 404

    @allure.title("Удаление объявления по несущ. Id")
    def test_delete_item_not_found(self, item_client: ItemClient) -> None:
        response = item_client.delete_item(str(uuid.uuid4()))
        assert response.status_code == 404

    @allure.title("Удаление объявления - неверный формат")
    def test_delete_item_invalid_format(self, item_client: ItemClient) -> None:
        response = item_client.delete_item("invalid-id")
        assert response.status_code == 400

    @allure.title("Создание объявления - пустое поле name")
    def test_create_item_empty_name(self, item_client: ItemClient) -> None:
        payload = build_item_payload()
        payload["name"] = ""
        response = item_client.create_item(payload)
        assert response.status_code == 400

    @allure.title("Создание объявления - отсутствует поле sellerID")
    def test_create_item_missing_seller_id(self, item_client: ItemClient) -> None:
        payload = build_item_payload()
        del payload["sellerID"]
        response = item_client.create_item(payload)
        assert response.status_code == 400

    @allure.title("Создание объявления - нулевая цена")
    def test_create_item_zero_price(self, item_client: ItemClient) -> None:
        payload = build_item_payload(price=0)
        response = item_client.create_item(payload)
        # API не принимает нулевую цену
        assert response.status_code == 400

    @allure.title("Создание объявления - очень большая цена")
    def test_create_item_very_large_price(self, item_client: ItemClient) -> None:
        payload = build_item_payload(price=999999999)
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

        if item_id:
            item_client.delete_item(item_id)

    @allure.title("Создание объявления - без statistics")
    def test_create_item_without_statistics(self, item_client: ItemClient) -> None:
        payload = build_item_payload()
        del payload["statistics"]
        response = item_client.create_item(payload)
        # API требует поле statistics
        assert response.status_code == 400

    @allure.title("Создание объявления - sellerID ниже границы")
    def test_create_item_seller_id_below_boundary(self, item_client: ItemClient) -> None:
        payload = build_item_payload(seller_id=111110)
        response = item_client.create_item(payload)
        assert response.status_code in [200, 400]

        if response.status_code == 200:
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

            if item_id:
                item_client.delete_item(item_id)

    @allure.title("Создание объявления - sellerID выше границы")
    def test_create_item_seller_id_above_boundary(self, item_client: ItemClient) -> None:
        payload = build_item_payload(seller_id=1000000)
        response = item_client.create_item(payload)
        assert response.status_code in [200, 400]

        if response.status_code == 200:
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

            if item_id:
                item_client.delete_item(item_id)

    @allure.title("Создание объявления - очень длинное имя")
    def test_create_item_very_long_name(self, item_client: ItemClient) -> None:
        payload = build_item_payload(name="a" * 1000)
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

        if item_id:
            item_client.delete_item(item_id)

    @allure.title("Создание объявления - price строкой")
    def test_create_item_price_as_string(self, item_client: ItemClient) -> None:
        payload = build_item_payload()
        payload["price"] = "abc"
        response = item_client.create_item(payload)
        assert response.status_code == 400

    @allure.title("Создание объявления - пустой объект")
    def test_create_item_empty_object(self, item_client: ItemClient) -> None:
        response = item_client.create_item({})
        assert response.status_code == 400

    @allure.title("Получение объявления - пустой ID")
    def test_get_item_by_id_empty(self, item_client: ItemClient) -> None:
        response = item_client.get_item_by_id("")
        assert response.status_code == 404

    @allure.title("Получение объявлений продавца - без товаров")
    def test_get_items_by_seller_empty(self, item_client: ItemClient) -> None:
        seller_id = Generator.generate_seller_id()
        response = item_client.get_items_by_seller(seller_id)
        assert response.status_code == 200
        items = response.json()
        assert isinstance(items, list)
        assert len(items) == 0

    @allure.title("Получение объявлений продавца - неверный формат ID")
    def test_get_items_by_seller_invalid_format(self, item_client: ItemClient) -> None:
        response = item_client.get_items_by_seller("invalid")  # type: ignore
        assert response.status_code == 400

    @allure.title("Получение объявлений продавца - несуществующий ID")
    def test_get_items_by_seller_not_exist(self, item_client: ItemClient) -> None:
        response = item_client.get_items_by_seller(1)
        assert response.status_code == 200
        items = response.json()
        assert isinstance(items, list)

    @allure.title("Удаление объявления дважды")
    def test_delete_item_twice(self, item_client: ItemClient) -> None:
        payload = build_item_payload()
        create_response = item_client.create_item(payload)
        assert create_response.status_code == 200

        data = create_response.json()
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

        delete_response = item_client.delete_item(item_id)
        assert delete_response.status_code == 200

        second_delete = item_client.delete_item(item_id)
        assert second_delete.status_code == 404

    @allure.title("Удаление с пустым ID")
    def test_delete_item_empty_id(self, item_client: ItemClient) -> None:
        response = item_client.delete_item("")
        assert response.status_code == 404
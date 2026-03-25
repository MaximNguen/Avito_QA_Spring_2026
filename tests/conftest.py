"""Pytest фикстуры для тестов"""

import pytest

from src.clients.item_client import ItemClient
from src.clients.statistic_client import StatisticClient
from src.endpoints.endpoint_factory import EndpointFactory
from src.utils.generators import Generator
from src.utils.payloads import build_item_payload


@pytest.fixture
def item_client() -> ItemClient:
    return ItemClient()

@pytest.fixture
def statistic_client() -> StatisticClient:
    return StatisticClient()

@pytest.fixture
def endpoint_factory() -> EndpointFactory:
    factory = EndpointFactory()
    yield factory
    factory.clear_cache()

@pytest.fixture
def created_item(item_client: ItemClient):
    payload = build_item_payload()
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
    yield {"id": item_id, "payload": payload, "response": data}

    item_client.delete_item(item_id)

@pytest.fixture
def created_item_with_factory(endpoint_factory: EndpointFactory):
    create_endpoint = endpoint_factory.create_endpoint()
    delete_endpoint = endpoint_factory.delete_endpoint()

    payload = build_item_payload()
    item_id = create_endpoint.action(payload)

    yield {"id": item_id, "payload": payload}

    delete_endpoint.action(item_id)
    delete_endpoint.verify_deleted(item_id)

@pytest.fixture
def test_seller_id() -> int:
    return Generator.generate_seller_id()
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import allure
import requests

from src.config import BASE_URL


class BaseEndpoint(ABC):
    """Базовый класс для всех ручек"""

    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.response: Optional[requests.Response] = None
        self.response_json: Optional[Dict[str, Any]] = None

    @abstractmethod
    def action(self, *args, **kwargs) -> Any:
        pass

    @allure.step("Проверюяем, что код статуса - {expected_code}")
    def check_status_code(self, expected_code: int) -> None:
        assert self.response is not None, "Код статуса не пришел"
        actual_code = self.response.status_code
        assert (
            actual_code == expected_code
        ), f"Ожидали {expected_code}, получили {actual_code}. Ответ: {self.response.text}"

    @allure.step("Проверка наличия нужных полей в ответе")
    def check_response_fields(self, expected_fields: list) -> None:
        assert self.response_json is not None, "Не получен JSON ответ"
        for field in expected_fields:
            assert (
                field in self.response_json
            ), f"Поле '{field}' не найден в ответе"

    @allure.step("Достаем Id у объявления")
    def extract_item_id(self) -> Optional[str]:
        if not self.response_json:
            return None

        if "id" in self.response_json:
            return self.response_json["id"]

        status = self.response_json.get("status", "")
        import re

        match = re.search(
            r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fx`A-F]{4}-[0-9a-fA-F]{12}",
            str(status),
        )
        if match:
            return match.group(0)

        return None
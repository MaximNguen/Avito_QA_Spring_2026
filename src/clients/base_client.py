from __future__ import annotations
from typing import Any, Dict, Optional
import requests
from src.config import BASE_URL, TIMEOUT_SECONDS

class BaseClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
    ) -> None:
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.timeout_seconds = timeout_seconds or TIMEOUT_SECONDS
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Отправка запроса и принятие ответа"""
        url = f"{self.base_url}{path}"
        return self.session.request(
            method=method,
            url=url,
            json=json,
            timeout=self.timeout_seconds,
        )
import json
from pathlib import Path
from typing import Any, Dict, Optional

from src.utils.generators import Generator

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = REPO_ROOT / "tests" / "data" / "item_payloads.json"

def load_payload_template() -> Dict[str, Any]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return dict(data["base_valid"])

def build_item_payload(
    seller_id: Optional[int] = None,
    name: Optional[str] = None,
    price: Optional[int] = None,
    statistics: Optional[Dict[str, int]] = None,
    overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = load_payload_template()

    payload["sellerID"] = seller_id if seller_id is not None else Generator.generate_seller_id()
    payload["name"] = name if name is not None else Generator.generate_unique_name()

    if price is not None:
        payload["price"] = price

    if statistics is not None:
        payload["statistics"] = statistics

    if overrides:
        payload.update(overrides)

    return payload

def build_invalid_payload(
    invalid_field: str,
    invalid_value: Any,
    base_payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = base_payload or build_item_payload()
    payload[invalid_field] = invalid_value
    return payload
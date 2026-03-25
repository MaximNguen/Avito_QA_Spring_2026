import random
import uuid

from src.config import SELLER_ID_MAX, SELLER_ID_MIN


class Generator:
    """Класс-генератор данных"""

    @staticmethod
    def generate_seller_id() -> int:
        """Генерация Id в допущеном радиусе"""
        return random.randint(SELLER_ID_MIN, SELLER_ID_MAX)

    @staticmethod
    def generate_unique_name() -> str:
        """Уникальное имя объявления"""
        return f"item-{uuid.uuid4().hex[:12]}"

    @staticmethod
    def generate_price() -> int:
        """Генерация цен"""
        return random.randint(1, 1000000)

    @staticmethod
    def generate_statistics() -> dict:
        """Генерация рандомных статистик"""
        return {
            "likes": random.randint(0, 1000),
            "viewCount": random.randint(0, 10000),
            "contacts": random.randint(0, 500),
        }

    @staticmethod
    def generate_invalid_item_id() -> str:
        """Выдача id не существующего объявления"""
        return "invalid-id-123"

    @staticmethod
    def generate_non_existent_uuid() -> str:
        """Генерация несуществующего UUID"""
        return str(uuid.uuid4())
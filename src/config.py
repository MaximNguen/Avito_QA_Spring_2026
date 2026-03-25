import os

BASE_URL = os.getenv("BASE_URL", "https://qa-internship.avito.com").rstrip("/")
TIMEOUT_SECONDS = float(os.getenv("TIMEOUT_SECONDS", "10"))

SELLER_ID_MIN = 111111
SELLER_ID_MAX = 999999
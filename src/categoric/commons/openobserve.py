import os
import sys

import httpx
from loguru import logger


class OpenObserveHandler:
    def __init__(
        self,
        endpoint: str | None = None,
        username: str | None = None,
        password: str | None = None,
        organization: str = "default",
        stream: str = "logs",
    ):
        self.endpoint = endpoint or os.getenv("OPENOBSERVE_ENDPOINT")
        self.username = username or os.getenv("OPENOBSERVE_USERNAME")
        self.password = password or os.getenv("OPENOBSERVE_PASSWORD")
        self.organization = organization
        self.stream = stream
        self.client = httpx.Client(auth=(self.username, self.password)) if self.username and self.password else None

    def __call__(self, message):
        if not self.client or not self.endpoint:
            return

        record = message.record
        log_data = {
            "timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "message": record["message"],
            "module": record["module"],
            "function": record["function"],
            "line": record["line"],
            "extra": record["extra"],
        }

        url = f"{self.endpoint}/api/{self.organization}/{self.stream}/_json"
        try:
            self.client.post(url, json=[log_data])
        except Exception:
            # Fallback to stdout or just ignore to prevent infinite loop
            pass


def setup_telemetry() -> None:
    logger.remove()
    # Stdout logger
    logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")

    # OpenObserve logger if configured
    if os.getenv("OPENOBSERVE_ENDPOINT"):
        handler = OpenObserveHandler()
        logger.add(handler, level="INFO")

    logger.info(
        "Telemetry setup complete (OpenObserve enabled: {})",
        bool(os.getenv("OPENOBSERVE_ENDPOINT")),
    )

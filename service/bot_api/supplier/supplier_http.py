import asyncio
from dataclasses import dataclass

import httpx
from shared.settings import AppSettings


@dataclass
class HTTPSupplier:
    app_settings: AppSettings

    def __post_init__(self):
        self.client = httpx.AsyncClient()
        self.loop = asyncio.get_event_loop()

    def __del__(self):
        self.loop.run_until_complete(self.client.aclose())

    def predict(self, image: bytes):
        ...

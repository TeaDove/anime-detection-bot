from dataclasses import dataclass
from typing import Any, Dict

import ujson
from telegram import Update
from telegram.ext import Application

from shared.base import logger


@dataclass
class LambdaHandler:
    app: Application
    loop: Any

    def __post_init__(self):
        self.loop.run_until_complete(self.app.initialize())

    async def handle(self, event: Dict[str, Any], _) -> None:
        try:
            self.loop.run_until_complete(
                self.app.process_update(
                    Update.de_json(ujson.loads(event["body"]), self.app.bot)
                )
            )
        except Exception:
            logger.critical(
                {"status": "internal.server.error", "event": event}, exc_info=True
            )

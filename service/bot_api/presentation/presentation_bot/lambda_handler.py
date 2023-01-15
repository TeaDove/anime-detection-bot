import asyncio
from dataclasses import dataclass
from typing import Any, Dict

import ujson
from telegram import Update
from telegram.ext import Application

from shared.base import logger


@dataclass
class LambdaHandler:
    app: Application

    def __post_init__(self):
        logger.debug({"status": "creating.bot"})
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.app.initialize())
        self.loop.run_until_complete(self.app.start())

    def __del__(self):
        logger.debug({"status": "destroyng.bot"})
        self.loop.run_until_complete(self.app.stop())
        self.loop.run_until_complete(self.app.shutdown())
        self.loop.close()

    def handle(self, event: Dict[str, Any], _) -> Dict[str, Any]:
        logger.debug({"status": "got.event", "event": event})
        try:
            update = ujson.loads(event["body"])
            logger.debug({"status": "got.update", "update": update})
            self.loop.run_until_complete(
                self.app.process_update(Update.de_json(update, self.app.bot))
            )
        except Exception:
            logger.critical(
                {"status": "internal.server.error", "event": event}, exc_info=True
            )
            return {"statusCode": 500}
        logger.debug({"status": "event.processed", "event": event})
        return {"statusCode": 200}

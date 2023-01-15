import os
from logging import _nameToLevel

import uvicorn

from presentation.main import app
from shared.settings import app_settings

uvicorn_app = app

if __name__ == "__main__":
    uvicorn.run(
        "entrypoints:uvicorn_app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        workers=app_settings.uvicorn_workers,
        log_level=_nameToLevel["WARNING"],
    )

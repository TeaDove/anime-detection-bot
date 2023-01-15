from fastapi import FastAPI, Request, status
from fastapi.responses import UJSONResponse
from starlette.exceptions import ExceptionMiddleware

from presentation.router import router
from shared.base import logger


def create_app() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(ExceptionMiddleware, handlers=fastapi_app.exception_handlers)
    fastapi_app.include_router(router)
    return fastapi_app


app = create_app()


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, __: Exception):
    logger.critical({"status": "internal.server.error"}, exc_info=True)
    return UJSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "internal.server.error"})

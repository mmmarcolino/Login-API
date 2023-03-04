from login_api import routers
from login_api.exception import ApiException
from login_api import utils
from login_api.logger import logger
from login_api.globals import Globals
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse


STATUS_PATH = "/status"


def setup_routers(app):
    app.include_router(
        routers.login_router,
        prefix="/v1/login_api",
        tags=["login_api"],
    )


def setup_basic_routes(app):
    @app.get(STATUS_PATH, response_class=PlainTextResponse)
    async def status():
        return "OK"


def setup_exception_handlers(app):

    @app.exception_handler(HTTPException)
    async def validation_exception_handler(request: Request, exc: HTTPException):

        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
            headers={"x-request_id": Globals().get_value("request_id")},
        )

    @app.exception_handler(ApiException)
    async def handle_any_api_exceptions(request: Request, exc: ApiException):
        logger.exception(exc)

        return JSONResponse(
            status_code=exc.code,
            content={"message": exc.message},
            headers={"x-request_id": Globals().get_value("request_id")},
        )

    @app.exception_handler(500)
    async def handle_any_exceptions(request: Request, exc: Exception):
        logger.exception(exc)

        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"},
            headers={"x-request_id": Globals().get_value("request_id")},
        )


def setup_middlewares(app):
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        Globals().set_value("request_id", utils.generate_request_id())
        response = await call_next(request)
        response.headers["X-Request-Id"] = Globals().get_value("request_id")
        return response


def get_app():
    app = FastAPI()
    setup_exception_handlers(app)
    setup_routers(app)
    setup_basic_routes(app)
    setup_middlewares(app)
    return app

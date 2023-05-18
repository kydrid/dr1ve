import logging
import sys
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, List, Sequence, Type

from box import Box
from fastapi import APIRouter as OriginalAPIRouter
from fastapi import FastAPI as OriginalFastAPI
from fastapi.applications import AppType
from fastapi.datastructures import Default
from fastapi.middleware import Middleware
from fastapi.params import Depends
from fastapi.routing import APIRoute
from fastapi.utils import generate_unique_id
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.types import ASGIApp, Lifespan

from .docstrings import copy_doc


class FastAPI(OriginalFastAPI):
    logger: logging.Logger = None  # type: ignore

    @copy_doc(OriginalFastAPI.__init__)
    def __init__(
        self: AppType,
        logger_name: str,
        config: Box,
        *,
        debug: bool = False,
        routes: List[BaseRoute] | None = None,
        title: str = "FastAPI",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: str | None = "/openapi.json",
        openapi_tags: List[Dict[str, Any]] | None = None,
        servers: List[Dict[str, str | Any]] | None = None,
        dependencies: Sequence[Depends] | None = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        docs_url: str | None = "/docs",
        redoc_url: str | None = "/redoc",
        swagger_ui_oauth2_redirect_url: str | None = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Dict[str, Any] | None = None,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Dict[
            int | Type[Exception],
            Callable[[Request, Any], Coroutine[Any, Any, Response]],
        ]
        | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan[AppType] | None = None,
        terms_of_service: str | None = None,
        contact: Dict[str, str | Any] | None = None,
        license_info: Dict[str, str | Any] | None = None,
        openapi_prefix: str = "",
        root_path: str = "",
        root_path_in_servers: bool = True,
        responses: Dict[int | str, Dict[str, Any]] | None = None,
        callbacks: List[BaseRoute] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        swagger_ui_parameters: Dict[str, Any] | None = None,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
        **extra: Any,
    ) -> None:
        super().__init__(
            debug=debug,
            routes=routes,
            title=title,
            description=description,
            version=version,
            openapi_url=openapi_url,
            openapi_tags=openapi_tags,
            servers=servers,
            dependencies=dependencies,
            default_response_class=default_response_class,
            docs_url=docs_url,
            redoc_url=redoc_url,
            swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
            swagger_ui_init_oauth=swagger_ui_init_oauth,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            terms_of_service=terms_of_service,
            contact=contact,
            license_info=license_info,
            openapi_prefix=openapi_prefix,
            root_path=root_path,
            root_path_in_servers=root_path_in_servers,
            responses=responses,
            callbacks=callbacks,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            swagger_ui_parameters=swagger_ui_parameters,
            generate_unique_id_function=generate_unique_id_function,
            **extra,
        )

        self.config = config  # type: ignore
        self._logger_name = logger_name  # type: ignore

        self._setup_logger()  # type: ignore

    def _setup_logger(self) -> None:
        logger = logging.getLogger(self._logger_name)
        logger.setLevel(getattr(logging, self.config.logging.level))

        handler = logging.StreamHandler(sys.stdout)
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asciitime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.logger = logger


class APIRouter(OriginalAPIRouter):
    logger: logging.Logger = None  # type: ignore

    @copy_doc(OriginalAPIRouter.__init__)
    def __init__(
        self,
        logger_name,
        logger_level,
        *,
        prefix: str = "",
        tags: List[str | Enum] | None = None,
        dependencies: Sequence[Depends] | None = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Dict[int | str, Dict[str, Any]] | None = None,
        callbacks: List[BaseRoute] | None = None,
        routes: List[BaseRoute] | None = None,
        redirect_slashes: bool = True,
        default: ASGIApp | None = None,
        dependency_overrides_provider: Any | None = None,
        route_class: Type[APIRoute] = APIRoute,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan[Any] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> None:
        super().__init__(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            default_response_class=default_response_class,
            responses=responses,
            callbacks=callbacks,
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=route_class,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            generate_unique_id_function=generate_unique_id_function,
        )

        self._logger_name = logger_name  # type: ignore
        self._logger_level = logger_level  # type: ignore

        self._setup_logger()  # type: ignore

    def _setup_logger(self) -> None:
        logger = logging.getLogger(self._logger_name)
        logger.setLevel(self._logger_level)

        handler = logging.StreamHandler(sys.stdout)
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asciitime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.logger = logger

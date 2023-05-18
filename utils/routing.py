import importlib
import os
from pathlib import Path
from typing import List

from .classes import APIRouter, FastAPI


def load_routes(
    app: FastAPI, route_path: Path, excluded: List[str] | str | None = None
) -> None:
    """Recursively include all routers in the specified route path, except the excluded ones

    Args:
        app (FastAPI): The FastAPI app instance
        route_path (Path): The path for the routes to include
        excluded (List[str]): The list of routes to include, relative to the routes path
    """

    # If None is passed, convert it to an empty list
    if excluded is None:
        excluded = []

    # Convert the excluded parameter to a list, if a string is passed. Felt cute might delete later
    elif isinstance(excluded, str):
        new = excluded.split(",")
        excluded = [exclusion.strip() for exclusion in new]

    for route in route_path.rglob("*.py"):
        relative = route.relative_to(route_path)
        name = str(relative.with_suffix(""))

        if name not in excluded:
            fmt = str(route.with_suffix(""))

            module = importlib.import_module(fmt.replace(os.sep, "."))

            if hasattr(module, "router"):
                router: APIRouter = getattr(module, "router")
                router._logger_level = app.config.logging.routes.level
                app.include_router(router, prefix="/" + name)

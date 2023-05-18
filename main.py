from pathlib import Path

import tomli
from box import Box

from utils.classes import FastAPI
from utils.routing import load_routes

raw_config = tomli.load(open("config.toml", "rb"))
config = Box(raw_config)

app = FastAPI(
    logger_name=__name__,
    config=config,
    debug=config.app.debug,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
load_routes(
    app,
    Path(config.routes.path),
)


@app.get("/")
async def index():
    return "Hello, World!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=config.app.host, port=config.app.port, reload=config.app.debug
    )

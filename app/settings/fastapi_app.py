"""Fastapi app configuration."""

import importlib
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import env_data


def create_app() -> FastAPI:
    """Create and configure a FastAPI instance.

    This function creates a FastAPI application, configures it with middleware for
    handling Cross-Origin Resource Sharing (CORS), and sets up the OpenAPI
    documentation URLs. It also dynamically loads route modules from the specified
    directory and includes them in the app.

    Arguments:
        Has no arguments.

    Returns:
        FastAPI: The configured FastAPI application instance.

    """
    app = FastAPI(
        docs_url=env_data.DOCS_URL,
        redoc_url=env_data.RE_DOC_URL,
        openapi_url=env_data.OPENAPI_URL
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api = "/api"
    routes_directory = "app.routes"
    file_exceptions = ["__init__.py"]
    for filename in os.listdir(routes_directory.replace(".", "/")):
        if filename.endswith(".py") and filename not in file_exceptions:
            module_name = f"{routes_directory}.{filename[:-3]}"
            module = importlib.import_module(module_name)

            if hasattr(module, "routes"):
                app.include_router(module.routes, prefix=api)

    return app

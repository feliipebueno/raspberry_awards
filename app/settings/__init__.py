from pathlib import Path

from prettyconf import config


class Config:
    """Configuration class for the application.

    This class defines various configuration values that are loaded from environment
    variables using the `config()` function. These values include URLs for
    documentation, environment settings, log name, and the root directory for the
    project.

    Attributes:
        DOCS_URL (str): The URL for the documentation.
        RE_DOC_URL (str): The URL for the ReDoc documentation.
        OPENAPI_URL (str): The URL for the OpenAPI specification.
        AMBIENT_ENV (str): The environment setting (e.g., production, development).
        LOG_NAME (str): The name used for logging (default is "SDC").
        ROOT_DIR (Path): The root directory of the project, determined dynamically.

    """

    DOCS_URL = config("DOCS", default=None)
    RE_DOC_URL = config("REDOC", default=None)
    OPENAPI_URL = config("OPEN_API_URL", default=None)

    AMBIENT_ENV = config("AMBIENT_ENV", default=None)

    LOG_NAME = config("LOG_NAME", default="SDC")
    ROOT_DIR = Path(__file__).parent.parent.parent

def get_config() -> Config:
    """Retrieve the configuration object.

    This function instantiates and returns the `Config` class, which holds
    the application's configuration values. These values are loaded from
    environment variables using the `config()` function.

    Arguments:
        Has no arguments.

    Returns:
        Config: An instance of the `Config` class containing the application's
                configuration settings.

    """
    return Config()

env_data = get_config()

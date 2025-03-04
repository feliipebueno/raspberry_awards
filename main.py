"""Initial file setup."""

import uvicorn

from app.settings.fastapi_app import create_app
from app.utils.logger import Logger

app = create_app()


if __name__ == "__main__":
    msg = 'Serviço iniciado'
    Logger(__name__).debug(msg)
    uvicorn.run("main:app", host="127.0.0.1", port=7000, reload=True)

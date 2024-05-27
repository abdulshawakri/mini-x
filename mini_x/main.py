import uvicorn
from fastapi import FastAPI

from mini_x.api import router
from mini_x.logging_config import setup_logging
from mini_x.settings.app_settings import get_app_settings

setup_logging()

app_settings = get_app_settings()

app = FastAPI()

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to the Mini-X Blog APIs"}


def main() -> None:
    uvicorn.run(
        "mini_x.main:app",
        host=app_settings.server_host,
        port=app_settings.server_port,
        log_level=app_settings.log_level.lower(),
        access_log=app_settings.enable_access_log,
        reload=app_settings.enable_reload,
    )


if __name__ == "__main__":
    main()

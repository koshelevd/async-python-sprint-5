import uvicorn

from api.app import initialize_app  # noqa
from settings.api import api_settings

app = initialize_app()


if __name__ == "__main__":
    uvicorn.run(
        app="server:app",
        host=api_settings.SERVER_HOST,
        port=api_settings.SERVER_PORT,
        debug=api_settings.DEBUG,
        reload=api_settings.DEBUG,
    )

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn

def get_application() -> FastAPI:
    application = FastAPI()
    application.mount("/static", StaticFiles(directory="./static"), name="static")

    return application

app = get_application()
templates = Jinja2Templates(
            directory="./template/"
        )

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=11002)
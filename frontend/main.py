from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
from fastapi.responses import RedirectResponse, StreamingResponse
import httpx
from os import urandom
from time import time

def get_application() -> FastAPI:
    application = FastAPI()
    application.mount("/static", StaticFiles(directory="./static"), name="static")

    return application

app = get_application()
templates = Jinja2Templates(
            directory="./template/"
        )

@app.get("/chat/", response_class=HTMLResponse)
def index(request: Request):
    chat_id = f'{urandom(4).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{hex(int(time() * 1000))[2:]}'
    return templates.TemplateResponse("index.html", {"request": request, "chat_id": chat_id})

@app.get("/chat/{conversation_id}", response_class=HTMLResponse)
def chat(request: Request, conversation_id: str):
    if '-' not in conversation_id:
        return RedirectResponse(url="/chat/")
    return templates.TemplateResponse("index.html", {"request": request, "chat_id": conversation_id})

@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/chat/")

async def _stream_response(self, data):
        url = 'http://103.141.140.71:11001/api/v1/chat'
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=data) as r:
                async for chunk in r.aiter_bytes():
                    yield chunk

@app.post("/conversation")
async def conversation(request: Request):
    data = await request.json()
    print(data)
    return StreamingResponse(_stream_response(data), media_type="text/event-stream")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=11001)
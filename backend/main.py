import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config.manager import settings
from database.chromadb import init_chroma_client
from database.mongodb import init_mongo_db
from api.endpoints import router as api_router

def initialize_backend_application(lifespan) -> fastapi.FastAPI:
    app = fastapi.FastAPI(lifespan=lifespan, **settings.set_backend_app_attributes)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )
    
    app.include_router(router=api_router, prefix=settings.API_PREFIX)

    return app

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    init_chroma_client()
    await init_mongo_db()
    yield
    
    
backend_app: fastapi.FastAPI = initialize_backend_application(lifespan)

if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )
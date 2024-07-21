from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.conversation import Conversation
from config.manager import settings

class MongoDB:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 27017,
        username: str = None,
        password: str = None
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        
        if self.username and self.password:
            self.uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"
        else:
            self.uri = f"mongodb://{self.host}:{self.port}"

    async def init(self):
        self.client = AsyncIOMotorClient(
            self.uri,
            maxPoolSize=100,
            minPoolSize=10,
        )
        
        await init_beanie(database=self.client.chatbot, document_models=[Conversation])
        
mongo_db: MongoDB = MongoDB(settings.MONGO_DB_HOST, settings.MONGO_DB_PORT, settings.MONGO_DB_USERNAME, settings.MONGO_DB_PASSWORD)

async def init_mongo_db():
    await mongo_db.init()
    print("MongoDB client initialized")
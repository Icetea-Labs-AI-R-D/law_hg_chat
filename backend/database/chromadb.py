import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from chromadb.config import Settings
from config.manager import settings

class ChromaDB:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 11003,
        openai_api_key: str = None,
    ):
        self.host = host
        self.port = port
        if not openai_api_key:
            raise ValueError("OpenAI API key is required")
        self.embedding_function = OpenAIEmbeddingFunction(api_key=openai_api_key)
        self.settings = Settings(allow_reset=True)
        self.client = None
        self.collection = None
        
    async def init_client(self):
        self.client = await chromadb.AsyncHttpClient(settings=self.settings, host= self.host, port=self.port)
        
    async def init_collection(self):
        self.collection = await self.client.get_or_create_collection(
            name=settings.CHROMA_DB_COLLECTION,
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"},
        )
        return self.collection
        
    async def get_client(self):
        return self.client
    
    def get_embedding_function(self):
        return self.embedding_function
    
    async def get_collection(self):
        return self.collection
    
chroma_db = ChromaDB(host=settings.CHROMA_DB_HOST, port=settings.CHROMA_DB_PORT, openai_api_key=settings.OPENAI_API_KEY)

async def init_chroma_client():
    await chroma_db.init_client()
    await chroma_db.init_collection()
    print("ChromaDB client initialized")
    
async def get_chroma_client():
    return await chroma_db.get_client()

async def get_collection():
    return await chroma_db.get_collection()
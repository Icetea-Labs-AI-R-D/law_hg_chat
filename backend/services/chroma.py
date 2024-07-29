from database.chromadb import get_collection
from utilities.constants import SEP
import asyncio

async def get_document_by_keyword(keywords: list):
    """
    Get a document from the collection by keywords.
    """
    collection = await get_collection()
    keywords.extend([SEP.join(keywords[:i+1]) for i in range(len(keywords))])
    response = await asyncio.gather(*[collection.asimilarity_search(query=keyword, k=3) for keyword in keywords])
    docs = []
    for res in response:
        docs.extend(res)
    result = {
        "documents": [],
        "metadatas": []    
    }
    
    for doc in docs:
        result['documents'].append(doc.page_content)
        result['metadatas'].append(doc.metadata)
        
    return result
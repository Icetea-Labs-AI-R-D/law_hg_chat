from database.chromadb import get_collection

async def get_document_by_keyword(keywords: list):
    """
    Get a document from the collection by keywords.
    """
    collection = await get_collection()
    concatenated_keywords = [' '.join(keywords[:i+1]) for i in range(len(keywords))]
    result = await collection.query(
        query_texts=[
            *keywords,
            *concatenated_keywords,
        ],
        n_results=5
    )
    
    return result
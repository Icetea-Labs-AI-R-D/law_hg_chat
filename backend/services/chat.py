from services import openai, chroma
from utilities import tools
from models.dto import ToolChoice
import json
from utilities.constants import TRANSLATE, TAB_AND_NEWLINE, ENDL, DENDL
async def extract(conversation: list, documents: list) -> list:
    result_extract_keywords = await openai.extract_keywords(conversation)
    keywords = tools.extraction_parser(result_extract_keywords)['keywords']
    
    results = await chroma.get_document_by_keyword(keywords)
    
    doc_full = results['documents']
    meta_full = results['metadatas']
    
    doc_full.extend([doc['name'] for doc in documents])
    meta_full.extend([doc['metadata'] for doc in documents])
    
    doc = []
    merged_documents = []
    
    for i in range(len(doc_full)):
        if doc_full[i] not in doc:
            doc.append(doc_full[i])
            merged_documents.append({
                "name": doc_full[i],
                "metadata": meta_full[i],
                "index" : len(doc)-1
            })
            
    document_titles = doc
    documents = merged_documents
    
    result_filter_documents = await openai.filter_documents(conversation=conversation, keywords=keywords, document_titles=document_titles)
    filtered_document_indexes = tools.filter_parser(result_filter_documents)['documents']
    
    documents = list(map(lambda x: x[1],filter(lambda x: x[0] in filtered_document_indexes, enumerate(documents))))
    
    return documents

async def router(conversation: list, documents: list) -> list:
    result_check_router = await openai.check_router(conversation=conversation, documents=documents)
    router = tools.router_parser(result_check_router)['tool']
    
    if ('1' in router):
        return ToolChoice.ASK
    else:
        return ToolChoice.ANSWER

async def ask(conversation: list, documents: list) -> tuple[str, list]:
    result_ask_follow_up_question = await openai.ask_follow_up_question(conversation=conversation, documents=documents)

    follow_up_question = tools.question_parser(result_ask_follow_up_question)['question']
    
    return follow_up_question
    

async def answer(conversation: list, documents: list) -> tuple[str, list]:
    documents_titles = [doc['name'] for doc in documents]
    
    result_filter_final_document = await openai.filter_final_document(conversation=conversation, documents=documents_titles)
    
    final_document_index = tools.final_document_parser(result_filter_final_document)['document-index']
    
    final_document = {
        "name": documents[final_document_index]['name'],
        "metadata": documents[final_document_index]['metadata'],
        "index" : final_document_index
    }
    
    formated_document = f"""
    # Tài liệu {final_document['index']}:
    ## {TAB_AND_NEWLINE.join(
    [
        f"{TRANSLATE[key]}: {final_document['metadata'].get(key).replace(DENDL, ENDL)}" for key in TRANSLATE.keys()
    ]
    )}
    """
    
    result_answer = await openai.answer(conversation=conversation, documents=[formated_document])
    
    documents = [documents[final_document_index]]
    
    return result_answer, documents
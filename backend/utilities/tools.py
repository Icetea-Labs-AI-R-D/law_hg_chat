import re
from utilities.constants import TRANSLATE, TAB_AND_NEWLINE, ENDL, DENDL

def router_parser(text: str) -> dict:
    tool_start = "<tool>"
    tool_end = "</tool>"

    # Extract tool
    tool_start_index = text.find(tool_start)
    tool_end_index = text.find(tool_end)
    if tool_start_index != -1 and tool_end_index != -1:
        tool = text[tool_start_index + len(tool_start):tool_end_index].strip()
    else:
        tool = ""
    return {
        "tool": tool
    }

def extraction_parser(text: str) -> dict:
    keywords_start = "<keywords>"
    keywords_end = "</keywords>"
    
    # Extract keywords
    keywords_start_index = text.find(keywords_start)
    keywords_end_index = text.find(keywords_end)
    if keywords_start_index != -1 and keywords_end_index != -1:
        keywords_text = text[keywords_start_index + len(keywords_start):keywords_end_index].strip()
        keywords = re.findall(r'"([^"]*)"', keywords_text)
    else:
        keywords = []
    
    return {
        "keywords": keywords
    }
    
def filter_parser(text: str) -> dict:
    documents_start = "<documents>"
    documents_end = "</documents>"

    # Extract documents
    documents_start_index = text.find(documents_start)
    documents_end_index = text.find(documents_end)
    if documents_start_index != -1 and documents_end_index != -1:
        documents_text = text[documents_start_index + len(documents_start):documents_end_index].strip()
        documents = re.findall(r'\d+', documents_text)
        documents = [int(doc) for doc in documents]
    else:
        documents = []
    
    return {
        "documents": documents
    }
    
def question_parser(text: str) -> dict:
    question_start = "<question>"
    question_end = "</question>"

    # Extract question
    question_start_index = text.find(question_start)
    question_end_index = text.find(question_end)
    if question_start_index != -1 and question_end_index != -1:
        question = text[question_start_index + len(question_start):question_end_index].strip()
    else:
        question = ""

    return {
        "question": question
    }
    
def final_document_parser(text: str) -> dict:
    document_start = "<index>"
    document_end = "</index>"

    # Extract document
    document_start_index = text.find(document_start)
    document_end_index = text.find(document_end)
    if document_start_index != -1 and document_end_index != -1:
        document_text = text[document_start_index + len(document_start):document_end_index].strip()
        document = int(document_text.split()[-1].strip())
    else:
        document = -1

    return {
        "document-index": document
    }     

def flatten_list(nested_list: list) -> list:
    """Flatten a nested list

    Args:
        nested_list (list): Nested list to flatten

    Returns:
        list: Flattened list
    """
    
    return [item for sublist in nested_list for item in sublist]

def get_documents_by_id(docs: list, metadata: list, indexes: list) -> list:
    documents = list(map(lambda index: {
        "name": docs[index],
        "metadata": metadata[index],
        "index": indexes
    }, indexes))
    
    return documents

def format_documents(documents: list, translate: bool = False) -> list:
    formatted_documents = [
        f"""
        # Tài liệu {index}: {doc["name"]}
        {translate and f"{TAB_AND_NEWLINE.join([
            f"- {TRANSLATE[key]}: {doc['metadata'][key].replace(DENDL, ENDL)}" for key in TRANSLATE.keys()
            ])}" }
        """
        for index, doc in enumerate(documents)
    ]
    
    return formatted_documents
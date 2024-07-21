import re
from utilities.constants import TRANSLATE, TAB_AND_NEWLINE

def extraction_parser(text: str) -> dict:
    """Parse the extraction response from the GPT model

    Args:
        text (str): Text to parse

    Returns:
        dict: Parsed extraction response
    """
    
    analysis_start = "<analysis>"
    analysis_end = "</analysis>"
    keywords_start = "<keywords>"
    keywords_end = "</keywords>"
    
    # Extract analysis
    analysis_start_index = text.find(analysis_start)
    analysis_end_index = text.find(analysis_end)
    if analysis_start_index != -1 and analysis_end_index != -1:
        analysis = text[analysis_start_index + len(analysis_start):analysis_end_index].strip()
    else:
        # raise ValueError("Analysis not found in text")
        analysis = ""
    
    # Extract keywords
    keywords_start_index = text.find(keywords_start)
    keywords_end_index = text.find(keywords_end)
    if keywords_start_index != -1 and keywords_end_index != -1:
        keywords_text = text[keywords_start_index + len(keywords_start):keywords_end_index].strip()
        keywords = re.findall(r'"([^"]*)"', keywords_text)
    else:
        # raise ValueError("Keywords not found in text")
        keywords = []
    
    return {
        "analysis": analysis,
        "keywords": keywords
    }
    
def filter_parser(text: str) -> dict:
    """Parse the filter response from the GPT model

    Args:
        text (str): Text to parse

    Returns:
        dict: Parsed filter response
    """
    
    analysis_start = "<analysis>"
    analysis_end = "</analysis>"
    documents_start = "<documents>"
    documents_end = "</documents>"
    
    # Extract analysis
    analysis_start_index = text.find(analysis_start)
    analysis_end_index = text.find(analysis_end)
    if analysis_start_index != -1 and analysis_end_index != -1:
        analysis = text[analysis_start_index + len(analysis_start):analysis_end_index].strip()
    else:
        # raise ValueError("Analysis not found in text")
        analysis = ""

    # Extract documents
    documents_start_index = text.find(documents_start)
    documents_end_index = text.find(documents_end)
    if documents_start_index != -1 and documents_end_index != -1:
        documents_text = text[documents_start_index + len(documents_start):documents_end_index].strip()
        documents = re.findall(r'\d+', documents_text)
        documents = [int(doc) for doc in documents]
    else:
        # raise ValueError("Documents not found in text")
        documents = []
    
    return {
        "analysis": analysis,
        "documents": documents
    }
    
def question_parser(text: str) -> dict:
    analysis_start = "<analysis>"
    analysis_end = "</analysis>"
    question_start = "<question>"
    question_end = "</question>"

    # Extract analysis
    analysis_start_index = text.find(analysis_start)
    analysis_end_index = text.find(analysis_end)
    if analysis_start_index != -1 and analysis_end_index != -1:
        analysis = text[analysis_start_index + len(analysis_start):analysis_end_index].strip()
    else:
        analysis = ""

    # Extract question
    question_start_index = text.find(question_start)
    question_end_index = text.find(question_end)
    if question_start_index != -1 and question_end_index != -1:
        question = text[question_start_index + len(question_start):question_end_index].strip()
    else:
        question = ""

    return {
        "analysis": analysis,
        "question": question
    }
    
def final_document_parser(text: str) -> dict:
    analysis_start = "<analysis>"
    analysis_end = "</analysis>"
    document_start = "<document>"
    document_end = "</document>"

    # Extract analysis
    analysis_start_index = text.find(analysis_start)
    analysis_end_index = text.find(analysis_end)
    if analysis_start_index != -1 and analysis_end_index != -1:
        analysis = text[analysis_start_index + len(analysis_start):analysis_end_index].strip()
    else:
        analysis = ""

    # Extract document
    document_start_index = text.find(document_start)
    document_end_index = text.find(document_end)
    if document_start_index != -1 and document_end_index != -1:
        document_text = text[document_start_index + len(document_start):document_end_index].strip()
        document = int(document_text)
    else:
        document = -1

    return {
        "analysis": analysis,
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
        "metadata": metadata[index]
    }, indexes))
    
    return documents

def format_documents(documents: list) -> list:
    formatted_documents = [
        f"""
        # Tài liệu {index}: {doc["name"]}
        ## {TAB_AND_NEWLINE.join(
            [
                f"{TRANSLATE[key]}: {doc['metadata'].get(key)}" for key in TRANSLATE.keys()
            ]
        )}
        """
        for index, doc in enumerate(documents)
    ]
    
    return formatted_documents
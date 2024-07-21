from fastapi import APIRouter, status, Depends
from models.chat import ChatRequest, ChatResponse
from services.openai import extract_keywords, filter_documents, ask_follow_up_question, filter_final_document, final_chat
from utilities import tools
from services.chroma import get_document_by_keyword
from services.mongo import get_conversation, add_message
from models.conversation import Message, Conversation, ConversationModel

router = APIRouter()

@router.post('/chat', response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    chat_request: ChatRequest
) -> ChatResponse:

    print(chat_request)

    conversation = await get_conversation(chat_request.conversation_id)
    conversation_model = ConversationModel(chat_id=conversation['chat_id'], messages=conversation['messages'], documents=conversation['documents'])
    messages = []
    chat_response = ""
    
    if (len(conversation_model.messages) == 0):
        extract_reponse = await extract_keywords(chat_request.message)
    
        keywords = tools.extraction_parser(extract_reponse)
    
        retrieval_response = await get_document_by_keyword(keywords['keywords'])
        
        docs = tools.flatten_list(retrieval_response['documents'])
        metadata = tools.flatten_list(retrieval_response['metadatas'])
        
        filter_documents_response = await filter_documents(chat_request.message, docs)
        filter_document = tools.filter_parser(filter_documents_response)
        document_indexes = filter_document['documents']
        documents = tools.get_documents_by_id(docs, metadata, document_indexes)
        
        formatted_documents = tools.format_documents(documents)
        
        ask_follow_up_question_response = await ask_follow_up_question(chat_request.message, formatted_documents)
        
        followup_question = tools.question_parser(ask_follow_up_question_response)
        chat_response = followup_question['question']
        
        messages.append(Message(role='user', content=chat_request.message))
        messages.append(Message(role='assistant', content=chat_response))
        conversation_model.documents = documents
    
    else:
        documents = conversation_model.documents
        formatted_documents = tools.format_documents(documents)
        
        filter_final_document_response = await filter_final_document(conversation_model.messages, formatted_documents)
        filter_final_documents = tools.final_document_parser(filter_final_document_response)
        
        final_document_index = filter_final_documents['document-index']
        
        final_document = documents[final_document_index]
        
        conversation_model.messages.append(Message(role='user', content=chat_request.message))
        
        final_chat_response = await final_chat(conversation_model.messages[0].content, [final_document], conversation_model.messages)
        chat_response = final_chat_response
        
        messages.append(Message(role='user', content=chat_request.message))
        messages.append(Message(role='assistant', content=chat_response))
        conversation_model.documents = [final_document]
        
    conversation['documents'] = conversation_model.documents
    conversation['messages'].extend(messages)
    
    await add_message(conversation)
    
    return ChatResponse(
        message=chat_response
    )
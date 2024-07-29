from fastapi import APIRouter, status, Depends
from models.chat import ChatRequest, ChatResponse
from services.openai import extract_keywords, ask_follow_up_question, filter_final_document, answer, check_router
from utilities import tools
from services.chroma import get_document_by_keyword
from services.mongo import get_conversation, add_message
from models.conversation import Message, Conversation, ConversationModel
from models.dto import ToolChoice
from services import chat as chat_service
import time
import asyncio

router = APIRouter()

@router.post('/chat', response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    chat_request: ChatRequest
) -> ChatResponse:
    conversation = await get_conversation(chat_request.conversation_id)
    conversation_model = ConversationModel(chat_id=conversation['chat_id'], messages=conversation['messages'], documents=conversation['documents'])
    
    messages = conversation_model.messages
    messages.append(Message(role='user', content=chat_request.message))
    chat_response = ""
    
    new_documents, choice = await asyncio.gather(
        *[chat_service.extract(conversation=messages, documents=conversation_model.documents), 
         chat_service.router(conversation=messages, documents=conversation_model.documents)]
    )
        
    if choice == ToolChoice.ASK:
        
        new_documents_title = [doc['name'] for doc in new_documents]
        
        follow_up_question, new_choice = await asyncio.gather(
            *[chat_service.ask(conversation=messages, documents=new_documents_title), 
            chat_service.router(conversation=messages, documents=new_documents_title)]
        )
        
        if new_choice == ToolChoice.ANSWER:
            result_answer, documents = await chat_service.answer(conversation=messages, documents=new_documents)
            chat_response = result_answer
            messages.append(Message(role='assistant', content=chat_response))
            conversation_model.documents = documents
        
        else:
            chat_response = follow_up_question
            messages.append(Message(role='assistant', content=chat_response))
            conversation_model.documents = new_documents
        
    else:
        result_answer, documents = await chat_service.answer(conversation=messages, documents=conversation_model.documents)
        chat_response = result_answer
        conversation_model.documents = documents
        messages.append(Message(role='assistant', content=chat_response))
        
    conversation['documents'] = conversation_model.documents
    conversation['messages'] = messages
   
    await add_message(conversation)
   
    return ChatResponse(
        message=chat_response
    )
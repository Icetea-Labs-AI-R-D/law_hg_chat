from fastapi import APIRouter, status, Depends
from fastapi.responses import StreamingResponse
from models.chat import ChatRequest, ChatResponse
from services.openai import extract_keywords, ask_follow_up_question, filter_final_document, answer, check_router
from utilities import tools
from services.chroma import get_document_by_keyword
from services.mongo import get_conversation, add_message
from models.conversation import Message, Conversation, ConversationModel
from models.dto import ToolChoice
from services import chat as chat_service
from services import openai
import asyncio

router = APIRouter()

@router.post('/chat', response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    chat_request: ChatRequest
):
    conversation = await get_conversation(chat_request.conversation_id)
    conversation_model = ConversationModel(chat_id=conversation['chat_id'], messages=conversation['messages'], documents=conversation['documents'])
    messages = conversation_model.messages
    messages.append(Message(role='user', content=chat_request.message))
    conversation['messages'] = messages
    await add_message(conversation)
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
            formated_document, documents = await chat_service.answer(conversation=messages, documents=new_documents)
            conversation_model.documents = documents
            conversation['documents'] = conversation_model.documents
            await add_message(conversation)
            return StreamingResponse(
                openai.answer(conversation=conversation, documents=[formated_document]),
                status_code=status.HTTP_200_OK,
                media_type="text/event-stream",
            )
        
        else:
            chat_response = follow_up_question
            messages.append(Message(role='assistant', content=chat_response))
            conversation_model.documents = new_documents
            await add_message(conversation)
            return StreamingResponse(
                chat_service.display_answer(chat_response),
                status_code=status.HTTP_200_OK,
                media_type="text/event-stream",
            )
        
    else:
        formated_document, documents = await chat_service.answer(conversation=messages, documents=conversation_model.documents)
        conversation_model.documents = documents
        conversation['documents'] = conversation_model.documents
        await add_message(conversation)
        return StreamingResponse(
            openai.answer(conversation=conversation, documents=[formated_document]),
            status_code=status.HTTP_200_OK,
            media_type="text/event-stream",
        )
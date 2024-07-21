from modules.gpt import async_client_4o_mini, async_client_gpt4o, get_choice_text
from utilities import prompt_templates, constants

async def extract_keywords(user_message: str) -> dict:
    system_prompt = prompt_templates.EXTRACT_KEYWORDS_SYSTEM_PROMPT
    user_prompt = prompt_templates.EXTRACT_KEYWORDS_USER_PROMPT.format(user_message=user_message)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0
    )
    
    return get_choice_text(response.choices[0])

async def filter_documents(user_message: str, document_titles: dict) -> dict:
    document_titles = constants.ENDL.join([f"- Tài liệu {i}: {title}" for i, title in enumerate(document_titles)])
    
    system_prompt = prompt_templates.FILTER_DOCUMENTS_SYSTEM_PROMPT.format(document_titles=document_titles)
    user_prompt = prompt_templates.FILTER_DOCUMENTS_USER_PROMPT.format(user_message=user_message)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0
    )
    
    return get_choice_text(response.choices[0])

async def ask_follow_up_question(user_message: str, documents: dict) -> dict:
    
    documents = constants.DENDL.join(documents)
    
    system_prompt = prompt_templates.ASK_FOLLOW_UP_QUESTION_SYSTEM_PROMPT
    user_prompt = prompt_templates.ASK_FOLLOW_UP_QUESTION_USER_PROMPT.format(user_message=user_message, documents=documents)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0
    )
    
    return get_choice_text(response.choices[0])

async def filter_final_document(conversation: list, documents: dict) -> dict:
    conversation = constants.ENDL.join(
        [f'- {"Khách hàng" if member.role == "user" else "Tư vấn viên"}: "{member.content}"' for member in conversation]
    )
    documents = constants.ENDL.join(documents)
    
    system_prompt = prompt_templates.FILTER_FINAL_DOCUMENT_SYSTEM_PROMPT
    user_prompt = prompt_templates.FILTER_FINAL_DOCUMENT_USER_PROMPT.format(conversation=conversation, documents=documents)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0
    )
    
    return get_choice_text(response.choices[0])

async def final_chat(user_message: str, documents: dict, messages: list) -> dict:
    documents = constants.ENDL.join([f"- {doc['name']}" for doc in documents])
    history = constants.ENDL.join([f'- {"Khách hàng" if message.role == "user" else "Tư vấn viên"}: "{message.content}"' for message in messages])
    
    system_prompt = prompt_templates.FINAL_CHAT_SYSTEM_PROMPT.format(context=documents)
    user_prompt = prompt_templates.FINAL_CHAT_USER_PROMPT.format(user_message=user_message, history=history)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
    
    return get_choice_text(response.choices[0])
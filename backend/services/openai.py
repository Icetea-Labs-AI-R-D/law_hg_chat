from modules.gpt import async_client_4o_mini, async_client_gpt4o, get_choice_text
from utilities import prompt_templates, constants
from models.conversation import Message
from services.mongo import add_message

async def check_router(
    conversation: list,
    documents: list
):
    conversation = constants.ENDL.join(
        [f'- {"Khách hàng" if member.role == "user" else "Tư vấn viên"}: "{member.content}"' for member in conversation]
    )
    
    documents = constants.ENDL.join(
        [f'- Tài liệu {index}: {title}' for index, title in enumerate(documents)]
    )
    
    system_prompt = prompt_templates.CHECK_ROUTER_SYSTEM_PROMPT
    user_prompt = prompt_templates.CHECK_ROUTER_USER_PROMPT.format(
        conversation=conversation, 
        documents=documents
    )
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0
    )
    
    return get_choice_text(response.choices[0])

async def extract_keywords(conversation: list) -> dict:
    conversation = constants.ENDL.join(f'- {"Khách hàng" if member.role == "user" else "Tư vấn viên"}: "{member.content}"' for member in conversation)
    
    system_prompt = prompt_templates.EXTRACT_KEYWORDS_SYSTEM_PROMPT
    user_prompt = prompt_templates.EXTRACT_KEYWORDS_USER_PROMPT.format(conversation=conversation)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0
    )
    
    return get_choice_text(response.choices[0])

async def filter_documents(conversation: list, keywords: list, document_titles: list) -> dict:
    document_titles = constants.ENDL.join([f"- Tài liệu {index}: {title}" for index, title in enumerate(document_titles)])
    conversation = constants.ENDL.join([f'- {"Khách hàng" if member.role == "user" else "Tư vấn viên"}: "{member.content}"' for member in conversation])
    keywords = constants.SEPARATOR.join([f'"{keyword}"' for keyword in keywords])
    
    system_prompt = prompt_templates.FILTER_DOCUMENTS_SYSTEM_PROMPT
    user_prompt = prompt_templates.FILTER_DOCUMENTS_USER_PROMPT.format(conversation=conversation, documents=document_titles, keywords=keywords)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0
    )
    
    return get_choice_text(response.choices[0])

async def ask_follow_up_question(conversation: list, documents: list) -> dict:

    conversation = constants.ENDL.join(
        [f'- {"Khách hàng" if member.role == "user" else "Tư vấn viên"}: "{member.content}"' for member in conversation]
    )
    documents = constants.ENDL.join(
        [f'- Tài liệu {index}: {title}' for index, title in enumerate(documents)]
    )
    
    system_prompt = prompt_templates.ASK_FOLLOW_UP_QUESTION_SYSTEM_PROMPT
    user_prompt = prompt_templates.ASK_FOLLOW_UP_QUESTION_USER_PROMPT.format(conversation=conversation, documents=documents)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0
    )
    
    return get_choice_text(response.choices[0])

async def filter_final_document(conversation: list, documents: list) -> dict:
    conversation = constants.ENDL.join(
        [f'- {"Khách hàng" if member.role == "user" else "Tư vấn viên"}: "{member.content}"' for member in conversation]
    )
    documents = constants.ENDL.join(
        [f'- Tài liệu {index}: {title}' for index, title in enumerate(documents)]
    )
    
    system_prompt = prompt_templates.FILTER_FINAL_DOCUMENT_SYSTEM_PROMPT
    user_prompt = prompt_templates.FILTER_FINAL_DOCUMENT_USER_PROMPT.format(conversation=conversation, documents=documents)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0
    )
    
    return get_choice_text(response.choices[0])

async def answer(conversation: dict, documents: list) -> dict:
    message = conversation['messages']
    question = message[-1].content
    documents = constants.ENDL.join(documents)
    
    system_prompt = prompt_templates.ANSWER_SYSTEM_PROMPT.format(documents=documents)
    user_prompt = prompt_templates.ANSWER_USER_PROMPT.format(question=question)
    
    response = await async_client_4o_mini.chat(
        system_prompt=system_prompt,
        conversation=message[:-1],
        user_prompt=user_prompt,
        stream=True
    )
    
    ans = ""
    
    async for chunk in response:
        token = chunk.choices[0].delta.content
        if token is not None:
            ans += token
            yield token
    
    message.append(Message(role='assistant', content=ans))
    conversation['messages'] = message
    await add_message(conversation)
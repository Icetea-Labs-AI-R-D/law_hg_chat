from typing import List, Union
from datetime import datetime, timedelta
from models.conversation import Conversation, Message
from beanie import PydanticObjectId

def conversatin2dict(conversation: Conversation) -> dict:
    return {
        "_id": conversation.id,
        "chat_id": conversation.chat_id,
        "messages": conversation.messages,
        "documents": conversation.documents,
        "create_at": conversation.create_at,
        "update_at": conversation.update_at
    }

async def get_conversation(chat_id: str) -> Union[Conversation, None]:
    current_time = datetime.now()
    x_minutes_ago = current_time - timedelta(minutes=30)

    pipeline = [
        {
            "$match": {
                "chat_id": chat_id,
                "$or": [
                    {"update_at": {"$lte": x_minutes_ago}},
                    {"$expr": {"$lte": [{"$size": "$messages"}, 2]}}
                ]
            }
        },
        {
            "$sort": {"update_at": -1}
        },
        {
            "$limit": 1
        }
    ]

    results = await Conversation.get_motor_collection().aggregate(pipeline).to_list(length=None)

    if not results:
        new_conversation = Conversation(
            chat_id=chat_id,
            messages=[],
            documents=[],
            create_at=datetime.now(),
            update_at=datetime.now()
           )
        await new_conversation.insert()
        dict_conversation = conversatin2dict(new_conversation)
        return dict_conversation
    return results[0]

async def add_message(update_conversation: Conversation) -> None:
    _id = PydanticObjectId(update_conversation['_id'])
    conversation = await Conversation.get(_id)
    update_conversation['update_at'] = datetime.now()
    update_query = {field: value for field, value in update_conversation.items()}
    await conversation.update({
        "$set": update_query
    })
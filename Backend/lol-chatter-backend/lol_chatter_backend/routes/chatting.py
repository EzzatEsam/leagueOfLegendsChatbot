import asyncio
import json
from fastapi import APIRouter, Depends, Body, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from lol_chatter_backend.DTOs import sessionDTO
from lol_chatter_backend.DTOs.error_DTO import ErrorDTO
from lol_chatter_backend.DTOs.message_DTO import messageDTO
from lol_chatter_backend.Dependencies.db_deps import get_db
from lol_chatter_backend.Dependencies.token_deps import get_current_user
from lol_chatter_backend.LolGeminiClient.summarizer import Summarizer
from lol_chatter_backend.Models.User import User
from lol_chatter_backend.DbOperations.ChatManagement import ChatManager
from lol_chatter_backend.LolGeminiClient.chat_manager import (
    ChatManager as GeminiChatManager,
)
from lol_chatter_backend.LolGeminiClient.model_generation import (
    get_available_models,
    get_model,
    get_summarizer_model,
)

router = APIRouter()


@router.get(
    "/sessions", responses={400: {"model": ErrorDTO}}, response_model=list[sessionDTO]
)
async def get_all_chats(user: User = Depends(get_current_user), db=Depends(get_db)):

    manager = ChatManager(db)
    chats, err = manager.get_user_chats(user_id=user.id)
    if err:
        return JSONResponse(status_code=400, content=err.model_dump())
    return [
        sessionDTO(id=chat.id, title=chat.title, date=chat.updated_at) for chat in chats
    ]


@router.get(
    "/messages",
    responses={400: {"model": ErrorDTO}, 401: {}},
    response_model=list[messageDTO],
)
async def get_chat_messages(
    sessionId: int,
    user: User = Depends(get_current_user),
    db=Depends(get_db),
):

    manager = ChatManager(db)
    session, err = manager.get_chat_by_id(sessionId)
    if err:
        return JSONResponse(status_code=400, content=err.model_dump())
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.user_id != user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    messages, err = manager.get_session_messages(session_id=sessionId)
    if err:
        return JSONResponse(status_code=400, content=err.model_dump())
    return [
        messageDTO(role=msg.role, content=msg.content, date=msg.created_at, id=msg.id)
        for msg in messages
    ]


@router.post(
    "/sessions", responses={400: {"model": ErrorDTO}}, response_model=sessionDTO
)
async def create_chat(
    user: User = Depends(get_current_user),
    db=Depends(get_db),
    firstMsg: str = Body(embed=True),
):
    manager = ChatManager(db)
    chat, err = manager.create_chat_session(user_id=user.id, title=firstMsg[:20])
    if err:
        return JSONResponse(status_code=400, content=err.model_dump())
    assert chat
    msg, err = manager.add_chat_msg(session_id=chat.id, role="user", content=firstMsg)
    if err:
        manager.delete_chat_by_id(chat.id)
        return JSONResponse(status_code=400, content=err.model_dump())
    assert chat
    return sessionDTO(id=chat.id, title=chat.title, date=chat.created_at)


@router.post(
    "/messages", responses={400: {"model": ErrorDTO}}, response_model=messageDTO
)
async def add_chat(
    user: User = Depends(get_current_user),
    sessionId: int = Body(),
    content: str = Body(),
    db=Depends(get_db),
):
    manager = ChatManager(db)
    msg, err = manager.add_chat_msg(session_id=sessionId, role="user", content=content)
    if err:
        return JSONResponse(status_code=400, content=err.model_dump())
    if not msg:
        raise HTTPException(status_code=404, detail="Session not found")

    if msg.session.user_id != user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return messageDTO(
        role=msg.role, content=msg.content, date=msg.created_at, id=msg.id
    )


@router.get("/models", response_model=list[str])
async def get_current_models(user: User = Depends(get_current_user)):
    return get_available_models()


@router.get(
    "/messages/response",
    responses={400: {"model": ErrorDTO}},
    response_model=messageDTO,
)
async def get_chat_response(
    sessionId: int,
    modelIndex: int = 0,
    user: User = Depends(get_current_user),
    db=Depends(get_db),
):

    models = get_available_models()

    if 0 > modelIndex >= len(models):
        raise HTTPException(status_code=400, detail="Invalid model index")

    model = models[modelIndex]

    # Temporary
    if model == "Gemini-1.5-Pro" :
        return JSONResponse(status_code=400, content= ErrorDTO(message = "What do you think I am rich or something? Use the regular model for fucks sake!").model_dump())

    print(f"User {user.id} requested model {model}")
    manager = ChatManager(db)
    msgs, err = manager.get_session_messages(session_id=sessionId)

    if err:
        return JSONResponse(status_code=400, content=err.model_dump())
    if not msgs:
        raise HTTPException(status_code=404, detail="Message not found")

    if msgs[0].session.user_id != user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if msgs[-1].role == "model":
        return JSONResponse(
            status_code=200, content=ErrorDTO(message="Already responded").model_dump()
        )

    # generate response
    prev_msgs = msgs[:-1]
    last_msg = msgs[-1]
    gemManager = GeminiChatManager(await get_model(model), prev_msgs)

    result = gemManager.send_msg(last_msg.content)

    resp, err = manager.add_chat_msg(
        session_id=sessionId, role="model", content=result.text
    )

    
    if err:
        return JSONResponse(status_code=400, content=err.model_dump())

    refreshed_msgs , err = manager.get_session_messages(session_id=sessionId)
    
    
    summarizer = Summarizer(get_summarizer_model())
    summary = summarizer.get_summarized_text(refreshed_msgs)
    
    manager.update_chat_session(chat_id=sessionId, title=summary)
    
    assert resp
    return messageDTO(
        role=resp.role, content=resp.content, date=resp.created_at, id=resp.id
    )

    # response_stream = result.stream()
    # async def simulate_response():
    #     # Simulate a large response by sending chunks of text
    #     total_msg = ""

    #     for part in response_stream:
    #         # if await request.is_disconnected():
    #         #     print("Client disconnected")
    #         #     return
    #         print("part")
    #         total_msg += part.text
    #         yield "data: " + part.text + "\n\n"
    #         # yield "data: "+ json.dumps({"answer" : large_text[i : i + chunk_size] , "test" : 2 }) + "\n\n"

    #     manager.add_chat_msg(session_id=sessionId, role="model", content=total_msg)

    # return StreamingResponse(simulate_response(), media_type="text/event-stream")

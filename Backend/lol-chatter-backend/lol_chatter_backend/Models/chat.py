from datetime import datetime
from sqlalchemy import  ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, mapped_column , Mapped
from lol_chatter_backend.DbInitialization import Base


class ChatSession(Base):
    __tablename__ = "chatsession"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    title  : Mapped[str] = mapped_column(String(400) , nullable=False)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    user  = relationship("User", back_populates="chat_sessions")
    messages :Mapped[list['ChatMessage']] = relationship('ChatMessage', back_populates="session")


class ChatMessage(Base):
    __tablename__ = "chatmessage"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_session_id : Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chatsession.id"),
        nullable=False,
    )
    role : Mapped[str] = mapped_column(String(255) , nullable=False)
    content : Mapped[str] = mapped_column(String(5000) , nullable=False)
    created_at  = mapped_column(DateTime , nullable=False , server_default=func.now())
    session : Mapped[ChatSession] = relationship( ChatSession ,back_populates="messages")

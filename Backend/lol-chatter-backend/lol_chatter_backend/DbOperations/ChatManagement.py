from typing import Tuple
from lol_chatter_backend.DTOs.error_DTO import ErrorDTO
from lol_chatter_backend.Models.chat import ChatSession, ChatMessage
from sqlalchemy.orm import Session


class ChatManager:
    def __init__(self, db: Session):
        self.db = db

    def get_chat_by_id(self, chat_id) -> Tuple[ChatSession | None, ErrorDTO | None]:
        """
        Retrieves a chat session from the database by its ID.

        Args:
            chat_id: The ID of the chat session to retrieve.

        Returns:
            Tuple[ChatSession | None, ErrorDTO | None]: A tuple containing the retrieved chat session, or None if not found.
        """
        try:
            chat = self.db.query(ChatSession).filter(ChatSession.id == chat_id).first()
        except Exception as e:
            print(e)
            return None, ErrorDTO(message="Failed to get chat")
        return chat, None

    def delete_chat_by_id(self, chat_id) -> ErrorDTO | None:
        """
        Deletes a chat session from the database by its ID.

        Args:
            chat_id (int): The ID of the chat session to be deleted.

        Returns:
            ErrorDTO | None: If the chat session is successfully deleted, returns None.
                             If there is an error during the deletion process, returns an ErrorDTO object with the message "Failed to delete chat".
        """
        try:
            chat = self.db.query(ChatSession).filter(ChatSession.id == chat_id).first()
            self.db.delete(chat)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
            return ErrorDTO(message="Failed to delete chat")
        return None

    def get_user_chats(self, user_id: int) -> Tuple[list[ChatSession], ErrorDTO | None]:
        """
        Retrieves all chat sessions associated with a given user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Tuple[list[ChatSession], ErrorDTO | None]: A tuple containing a list of chat sessions and an optional error.
                If the chat sessions are successfully retrieved, the list of chat sessions is returned.
                If there is an error during the retrieval process, an ErrorDTO object with the error message is returned.
        """
        try:
            chats = (
                self.db.query(ChatSession).filter(ChatSession.user_id == user_id).all()
            )
        except Exception as e:
            print(e)
            self.db.rollback()
            return [], ErrorDTO(message="Failed to get chats")

        return chats, None

    def create_chat_session(
        self, user_id: int, title: str
    ) -> Tuple[ChatSession | None, ErrorDTO | None]:
        """
        Creates a chat session in the database.

        Args:
            user_id (int): The ID of the user for whom the chat session is being created.
            title (str): The title of the chat session.

        Returns:
            Tuple[ChatSession | None, ErrorDTO | None]: A tuple containing the created chat session if successful, and None if there was an error.
        """
        try:
            chat = ChatSession(user_id=user_id, title=title)
            self.db.add(chat)
            self.db.commit()
            self.db.refresh(chat)
        except Exception as e:
            print(e)
            self.db.rollback()
            return None, ErrorDTO(message="Failed to create chat")
        return chat, None

    def add_chat_msg(
        self, session_id: int, role: str, content: str
    ) -> Tuple[ChatMessage | None, ErrorDTO | None]:
        """
        Adds a chat message to the database.

        Args:
            session_id (int): The ID of the chat session.
            role (str): The role of the chat message.
            content (str): The content of the chat message.

        Returns:
            Tuple[ChatMessage | None, ErrorDTO | None]: A tuple containing the created chat message if successful, and None if there was an error.
        """
        msg = ChatMessage(chat_session_id=session_id, role=role, content=content)
        try:
            self.db.add(msg)
            self.db.commit()
            self.db.refresh(msg)
        except Exception as e:
            print(e)
            self.db.rollback()
            return None, ErrorDTO(message="Failed to create chat message")
        return msg, None

    def get_session_messages(
        self, session_id: int
    ) -> Tuple[list[ChatMessage], ErrorDTO | None]:
        """
        Retrieves messages associated with a specific chat session.

        Args:
            session_id (int): The ID of the chat session.

        Returns:
            Tuple[list[ChatMessage], ErrorDTO | None]: A tuple containing a list of chat messages if successful, and an error message or None if there was an error.
        """
        try:
            messages = (
                self.db.query(ChatMessage)
                .filter(ChatMessage.chat_session_id == session_id)
                .all()
            )
        except Exception as e:
            print(e)
            return [], ErrorDTO(message="Failed to get messages")

        return messages, None

    def get_msg_by_id(self, msg_id) -> Tuple[ChatMessage | None, ErrorDTO | None]:
        """
        Retrieves a chat message from the database based on its ID.

        Args:
            msg_id (int): The ID of the chat message.

        Returns:
            Tuple[ChatMessage | None, ErrorDTO | None]: A tuple containing the chat message if found, or None if not found.
            If an error occurs, the second element of the tuple will be an instance of ErrorDTO with a message indicating the failure.
        """
        try:
            msg = self.db.query(ChatMessage).filter(ChatMessage.id == msg_id).first()
        except Exception as e:
            print(e)
            return None, ErrorDTO(message="Failed to get message")
        return msg, None

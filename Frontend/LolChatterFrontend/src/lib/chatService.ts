import { fetchEventSource } from "@microsoft/fetch-event-source";
import { chat, chatMessage } from "../models/chat";
import { Result } from "../models/result";
import { getServerAddr } from "./ServerCalls";

export class ChatService {
  private serverAddr: string = getServerAddr();
  private token: string;

  constructor(token: string) {
    this.token = token;
  }

  private postProcessChatMessage(message: chatMessage): chatMessage {
    return {
      ...message,
      date: new Date(message.date),
    };
  }

  private postProcessChatSession(chat: chat): chat {
    return {
      ...chat,
      date: new Date(chat.date),
    };
  }

  private async request<T>(
    url: string,
    options: RequestInit
  ): Promise<Result<T>> {
    try {
      const response = await fetch(url, options);
      if (response.ok) {
        const data = (await response.json()) as T;
        return { success: true, data, message: null };
      } else {
        const errorData = await response.json();
        console.error(errorData);
        return {
          success: false,
          data: null,
          message:
            errorData.message ||
            `Error ${response.status}: ${response.statusText}`,
        };
      }
    } catch (error) {
      console.error(error);
      return { success: false, data: null, message: `Error: ${error}` };
    }
  }

  private getHeaders(): HeadersInit {
    return {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.token}`,
    };
  }

  public async getSessions(): Promise<Result<chat[]>> {
    const url = `${this.serverAddr}/chatting/sessions`;
    const options = {
      method: "GET",
      headers: this.getHeaders(),
    };
    let result = await this.request<chat[]>(url, options);
    if (result.data) {
      result.data = result.data.map((chat) =>
        this.postProcessChatSession(chat)
      );
    }
    return result;
  }

  public async createSession(initialMessage: string): Promise<Result<chat>> {
    const url = `${this.serverAddr}/chatting/sessions`;
    const options = {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ firstMsg: initialMessage }),
    };
    let result = await this.request<chat>(url, options);
    if (result.data) {
      result.data = this.postProcessChatSession(result.data);
    }
    return result;
  }

  public async addMsg(
    chatId: number,
    message: string
  ): Promise<Result<chatMessage>> {
    const url = `${this.serverAddr}/chatting/messages`;
    const options = {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ sessionId: chatId, content: message }),
    };
    let result = await this.request<chatMessage>(url, options);
    if (result.data) {
      result.data = this.postProcessChatMessage(result.data);
    }
    return result;
  }

  public async getSessionMessages(
    chatId: number | string
  ): Promise<Result<chatMessage[]>> {
    // Construct the query parameters
    const params = new URLSearchParams({ sessionId: chatId.toString() });

    // Append the query parameters to the URL
    const url = `${this.serverAddr}/chatting/messages?${params.toString()}`;

    const options = {
      method: "GET",
      headers: this.getHeaders(),
    };

    let result = await this.request<chatMessage[]>(url, options);
    if (result.data) {
      result.data = result.data.map((msg) => this.postProcessChatMessage(msg));
    }
    return result;
  }

  public  getMsgResponse(sessionId: number , onRcv :(data: string) => void , onClose: () => void) : AbortController  {
    const url = `${this.serverAddr}/chatting/messages/${sessionId}/response`;
    const controller = new AbortController();
    const signal = controller.signal;
    fetchEventSource(url, {
      method: "GET",
      headers: {
        Accept: "text/event-stream",
        Authorization: `Bearer ${this.token}`,
      },
      onmessage: (event) => {
        onRcv(event.data);
      },
      onclose: () => {
        onClose();
      },
      signal
    });
    return controller;
  }
}

import { chat } from "./chat";
import User from "./user";

export interface HomePageLoadingData {
  user: User;
  chats: chat[];
  chatId: string;
}


import LoginPage from "./pages/login";
import SignupPage from "./pages/signup";
import { TokenManager } from "./lib/tokenManager";
import {
  createBrowserRouter,
  RouterProvider,
  redirect,
} from "react-router-dom";
import { ChatPage } from "./pages/ChatsPage";
import { HomePageLoadingData } from "./models/pageLoadData";
import { ChatService } from "./lib/chatService";

const router = createBrowserRouter([
  {
    path: "/",
    element: null,
    loader: async () => {
      return redirect("/chats");
    },
  },
  {
    path: "/chats/:chatId?",
    element: <ChatPage />,
    loader: async ({ params }) => {
      console.log("loader :", params.chatId);
      if (
        params.chatId === undefined ||
        (params.chatId !== "new" && isNaN(parseInt(params.chatId!)))
      ) {
        return redirect("/chats/new");
      }
      const user = await TokenManager.testToken();
      if (user) {
        const chatsService = new ChatService(TokenManager.token!);
        const chats = await chatsService.getSessions();
        if (chats.success) {
          console.log("all success>");
          const data: HomePageLoadingData = {
            user: user,
            chats: chats.data!,
            chatId: params.chatId!,
          };
          console.log(data);
          return data;
        } else {
          const data: HomePageLoadingData = {
            user: user,
            chats: [],
            chatId: params.chatId!,
          };
          return data;
        }
      } else {
        return redirect("/login");
      }
    },
  },

  {
    path: "/login",
    element: <LoginPage />,
    loader: async () => {
      const user = await TokenManager.testToken();

      if (user) {
        return redirect("/chats");
      }

      return null;
    },
  },
  {
    path: "/signup",
    element: <SignupPage />,
    loader: async () => {
      const user = await TokenManager.testToken();

      if (user) {
        return redirect("/chats");
      }
      return null;
    },
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;

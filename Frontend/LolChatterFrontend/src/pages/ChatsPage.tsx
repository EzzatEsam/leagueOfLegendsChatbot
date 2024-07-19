import React from "react";
import { Layout, theme } from "antd";
import Navbar from "../components/navbar";
import Sider from "antd/es/layout/Sider";
import SideBar from "../components/sideBar";
import { TokenManager } from "../lib/tokenManager";
import { useLoaderData } from "react-router-dom";
import { HomePageLoadingData } from "../models/pageLoadData";
import { useNavigate } from "react-router-dom";
import MsgsWindow from "../components/msgsWindow";

const { Content } = Layout;
/* const msgs: chatMessage[] = [
  {
    chatId: 1,
    id: 1,
    content:
      "Hello, how are you doing today? I wanted to ask if you have any recommendations for good books to read.",
    role: "user",
    date: new Date("2024-07-01T10:00:00Z"),
  },
  {
    chatId: 1,
    id: 2,
    content:
      "Hi there! I'm doing well, thank you. Yes, I have several recommendations depending on your interests. What genres do you like?",
    role: "assistant",
    date: new Date("2024-07-01T10:01:00Z"),
  },
  {
    chatId: 1,
    id: 3,
    content:
      "I enjoy reading science fiction and fantasy. I'm also interested in historical fiction. Do you have any suggestions in those genres?",
    role: "user",
    date: new Date("2024-07-01T10:02:00Z"),
  },
  {
    chatId: 1,
    id: 4,
    content:
      "Absolutely! For science fiction, you might enjoy 'Dune' by Frank Herbert or 'Neuromancer' by William Gibson. For fantasy, 'The Name of the Wind' by Patrick Rothfuss is excellent. In historical fiction, 'The Book Thief' by Markus Zusak is a compelling read.",
    role: "assistant",
    date: new Date("2024-07-01T10:03:00Z"),
  },
  {
    chatId: 1,
    id: 5,
    content:
      "Thank you so much for the recommendations! I've heard a lot about 'Dune' and 'The Name of the Wind', but I haven't read them yet. I'll definitely check them out. Do you have any more suggestions?",
    role: "user",
    date: new Date("2024-07-01T10:04:00Z"),
  },
  {
    chatId: 1,
    id: 6,
    content:
      "Sure! For more science fiction, consider 'Snow Crash' by Neal Stephenson. For fantasy, 'Mistborn' by Brandon Sanderson is a fantastic series. If you're looking for another historical fiction, 'All the Light We Cannot See' by Anthony Doerr is beautifully written.",
    role: "assistant",
    date: new Date("2024-07-01T10:05:00Z"),
  },
  {
    chatId: 1,
    id: 7,
    content:
      "These sound great! I'll add 'Snow Crash' and 'Mistborn' to my reading list. And 'All the Light We Cannot See' sounds fascinating as well. Thank you for your help!",
    role: "user",
    date: new Date("2024-07-01T10:06:00Z"),
  },
  {
    chatId: 1,
    id: 8,
    content:
      "You're welcome! Enjoy your reading, and feel free to reach out if you need more recommendations or have any other questions. Have a great day!",
    role: "assistant",
    date: new Date("2024-07-01T10:07:00Z"),
  },
  {
    chatId: 1,
    id: 2,
    content:
      "Hi there! I'm doing well, thank you. Yes, I have several recommendations depending on your interests. What genres do you like?",
    role: "assistant",
    date: new Date("2024-07-01T10:01:00Z"),
  },
  {
    chatId: 1,
    id: 3,
    content:
      "I enjoy reading science fiction and fantasy. I'm also interested in historical fiction. Do you have any suggestions in those genres?",
    role: "user",
    date: new Date("2024-07-01T10:02:00Z"),
  },
  {
    chatId: 1,
    id: 4,
    content:
      "Absolutely! For science fiction, you might enjoy 'Dune' by Frank Herbert or 'Neuromancer' by William Gibson. For fantasy, 'The Name of the Wind' by Patrick Rothfuss is excellent. In historical fiction, 'The Book Thief' by Markus Zusak is a compelling read.",
    role: "assistant",
    date: new Date("2024-07-01T10:03:00Z"),
  },
  {
    chatId: 1,
    id: 5,
    content:
      "Thank you so much for the recommendations! I've heard a lot about 'Dune' and 'The Name of the Wind', but I haven't read them yet. I'll definitely check them out. Do you have any more suggestions?",
    role: "user",
    date: new Date("2024-07-01T10:04:00Z"),
  },
  {
    chatId: 1,
    id: 6,
    content:
      "Sure! For more science fiction, consider 'Snow Crash' by Neal Stephenson. For fantasy, 'Mistborn' by Brandon Sanderson is a fantastic series. If you're looking for another historical fiction, 'All the Light We Cannot See' by Anthony Doerr is beautifully written.",
    role: "assistant",
    date: new Date("2024-07-01T10:05:00Z"),
  },
];

const chats: chat[] = [
  {
    id: 1,
    title: "Book Recommendations",
    date: new Date("2024-07-01T10:00:00Z"),
  },
  { id: 2, title: "Travel Plans", date: new Date("2024-07-01T11:30:00Z") },
  { id: 3, title: "Project Update", date: new Date("2024-07-02T14:15:00Z") },
  { id: 4, title: "Dinner Ideas", date: new Date("2024-07-02T18:45:00Z") },
  {
    id: 5,
    title: "Weekend Activities",
    date: new Date("2024-07-03T09:20:00Z"),
  },
  { id: 6, title: "Fitness Routine", date: new Date("2024-07-03T07:00:00Z") },
  {
    id: 7,
    title: "Work Meeting Notes",
    date: new Date("2024-07-04T16:50:00Z"),
  },
  { id: 8, title: "Shopping List", date: new Date("2024-07-04T12:10:00Z") },
  { id: 9, title: "Event Planning", date: new Date("2024-07-05T15:30:00Z") },
  { id: 10, title: "Health Tips", date: new Date("2024-07-05T08:00:00Z") },
  {
    id: 11,
    title: "Movie Suggestions",
    date: new Date("2024-07-06T10:45:00Z"),
  },
  { id: 12, title: "Coding Help", date: new Date("2024-07-06T13:20:00Z") },
  { id: 13, title: "New Recipes", date: new Date("2024-07-07T11:00:00Z") },
  {
    id: 14,
    title: "Job Interview Tips",
    date: new Date("2024-07-07T17:30:00Z"),
  },
  {
    id: 15,
    title: "Music Recommendations",
    date: new Date("2024-07-08T14:00:00Z"),
  },
  {
    id: 16,
    title: "Home Improvement Ideas",
    date: new Date("2024-07-08T18:25:00Z"),
  },
  { id: 17, title: "Photography Tips", date: new Date("2024-07-09T09:50:00Z") },
  { id: 18, title: "Gardening Advice", date: new Date("2024-07-09T13:15:00Z") },
  { id: 19, title: "Tech News", date: new Date("2024-07-10T10:00:00Z") },
  { id: 20, title: "Fashion Trends", date: new Date("2024-07-10T15:45:00Z") },
]; */

const handleSignOut = () => {
  TokenManager.logout();
  window.location.href = "/login";
};

export const ChatPage: React.FC = () => {
  let navigate = useNavigate();
  const [selectedModelIdx, setSelectedModelIdx] = React.useState<number>(0);
  const {
    token: { colorBgLayout },
  } = theme.useToken();
  // const [textAreaText, setTextAreaText] = useState<string>("");

  const loadingData: HomePageLoadingData =
    useLoaderData() as HomePageLoadingData;
  let { user, chats, chatId, availableModelNames } = loadingData;

  let chatIdVerified: number | null = null;
  if (chatId !== null && !isNaN(parseInt(chatId))) {
    chatIdVerified = parseInt(chatId);
  }
  console.log("ChatPage rendered");
  console.log(chats);
  console.log(user);
  const navigateToChat = (id: number | null) => {
    console.log("Navigating to chat", id);
    let newurl = "/chats/";
    if (id !== null) {
      newurl = `/chats/${id}`;
    }
    // newurl =`/login`;
    // history.push(newUrl , {shallow});
    navigate(newurl, { replace: false });
  };

  // setTextAreaText("");

  return (
    <Layout style={{ height: "100vh", background: colorBgLayout }}>
      <Sider
        width="20%"
        collapsible
        breakpoint="lg"
        style={{ background: colorBgLayout }}
        className="shadow-md rounded-xl"
      >
        <SideBar
          chats={chats}
          selectedIdx={chatIdVerified}
          setSelectedId={navigateToChat}
        ></SideBar>
      </Sider>

      <Layout style={{ height: "100vh" }}>
        <Navbar
          user={user}
          onSignOut={handleSignOut}
          appName="LolChatter"
          selectedModelIdx={selectedModelIdx}
          availableModels={availableModelNames}
          onModelSelect={(modelName) => {
            let idx = availableModelNames.indexOf(modelName);
            setSelectedModelIdx(idx);
          }}
        />
        <Content
          style={{
            overflow: "auto",
            // height: "75vh",
            margin: 0,
            background: colorBgLayout,
          }}
        >
          <MsgsWindow
            chatId={chatIdVerified}
            selectedModel={selectedModelIdx}
          ></MsgsWindow>
        </Content>
        {/* <Footer style={{ textAlign: "center", justifyContent: "center" }}>
         
        </Footer> */}
      </Layout>
    </Layout>
  );
};

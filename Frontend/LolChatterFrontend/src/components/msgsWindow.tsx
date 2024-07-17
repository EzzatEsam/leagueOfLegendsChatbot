import { Col, Flex, Form, Space } from "antd";
import { chatMessage } from "../models/chat";
import MsgBox from "./chatBox";
import TextArea from "antd/es/input/TextArea";
import React, { useEffect, useState } from "react";
import { ChatService } from "../lib/chatService";
import { TokenManager } from "../lib/tokenManager";
import { useNavigate } from "react-router-dom";
import { message } from "antd";
import { Footer } from "antd/es/layout/layout";

const MsgsWindow: React.FC<{ chatId: number | null }> = ({ chatId }) => {
  const [messages, setMessages] = useState<chatMessage[]>([]);
  const [inputDisabled, setInputDisabled] = useState<boolean>(false);
  const [form] = Form.useForm();
  const [messageApi, contextHolder] = message.useMessage();
  const [controller, setController] = useState<AbortController | null>(null);
  let navigate = useNavigate();
  const chatService = new ChatService(TokenManager.token!);

  console.log("MsgsWindow rendered");
  const updateData = async () => {
    if (chatId !== null) {
      const msgsResult = await chatService.getSessionMessages(chatId);
      if (!msgsResult.success) {
        console.error(msgsResult.message);
      } else {
        setMessages(msgsResult.data!);
      }
    } else {
      setMessages([]);
      setInputDisabled(false);
      setController(null);
    }
  };

  useEffect(() => {
    controller?.abort();
    setController(null);
    console.log("MsgsWindow rendered");
    console.log("chatId", chatId);
    updateData();
  }, [chatId]);

  useEffect(() => {
    fetchLastMsgResponse();
  }, [messages]);

  const handleSubmit = async () => {
    let textAreaText = form.getFieldValue("prompt") as string;
    form.resetFields();
    if (textAreaText.trim() === "") {
      return;
    }
    let error = false;
    if (chatId === null) {
      // create new chat
      const result = await chatService.createSession(textAreaText);
      if (result.success) {
        let newUrl = `/chats/${result.data!.id}`;
        // history.push(newUrl , {shallow});
        navigate(newUrl, { replace: false });
      } else {
        messageApi.error(result.message);
        error = true;
      }
    } else {
      const result = await chatService.addMsg(chatId, textAreaText);
      if (!result.success) {
        error = true;
        messageApi.error(result.message);
      } else {
        setMessages((prev) => [...prev, result.data!]);
      }
    }
    if (error) {
      return;
    }
  };

  const fetchLastMsgResponse = async () => {
    console.log("fetchLastMsgResponse");
    console.log(messages[messages.length - 1]);
    if (
      messages.length === 0 ||
      messages[messages.length - 1].role !== "user"
    ) {
      return;
    }

    const tempResponse: chatMessage = {
      chatId: -1,
      content: "",
      date: new Date(),
      id: -1,
      role: "assistant",
    };
    let lastMsg = messages[messages.length - 1];
    setMessages((prev) => [...prev, tempResponse]);
    // setMessages((prev) => [...prev, tempResponse]);
    setInputDisabled(true);
    // let controller = chatService.getMsgResponse(
    //   chatId!,
    //   (msg) => {
    //     setMessages((prev) => {
    //       const last = prev[prev.length - 1];
    //       const modified: chatMessage = {
    //         chatId: last.chatId,
    //         content: last.content + msg,
    //         date: new Date(),
    //         id: last.id,
    //         role: last.role,
    //       };
    //       let copy = [...prev];
    //       copy[copy.length - 1] = modified;
    //       return copy;
    //     });
    //   },
    //   () => {
    //     setController(null);
    //     // updateData();
    //   }
    // );

    // setController(controller);

    let result = await chatService.getMsgResponseNoSSE(chatId!);
    if (result.success) {
      setMessages((prev) => {
        let copy = [...prev];
        copy[copy.length - 1] = result.data!;
        return copy;
      });
    } else {
      messageApi.error(result.message);
    }
    setInputDisabled(false);
  };

  return (
    <>
      {contextHolder}

      <Flex vertical style={{ height: "100%" }} >
        <Col className="w-full p-6" style={{ flex: 1, overflowY: "auto" }} >
          {messages.map((msg) => (
            <div
              key={msg.id}
              style={{
                display: "flex",
                justifyContent: msg.role !== "user" ? "flex-start" : "flex-end",
              }}
            >
              <MsgBox msg={msg} />
            </div>
          ))}
        </Col>
        <Footer style={{ textAlign: "center", justifyContent: "center" , margin : 0}} className="shadow-md">
          
            <Form
              className="  p-2 justify-center align-middle w-full"
              style={{
                display: "block",
                justifyContent: "center",
                alignItems: "center",

                width: "100%",
              }}
              form={form}
              disabled={inputDisabled}
            >
              <Form.Item
                name="prompt"
                rules={[{ required: true }]}
                style={{
                  display: "block",
                  justifyContent: "center",
                  alignItems: "center",

                  width: "100%",
                }}
              >
                <TextArea
                  showCount
                  placeholder="Enter a prompt here..."
                  autoSize={{ minRows: 1, maxRows: 6 }}
                  allowClear
                  size="large"
                  className="w-5/6 rounded-2xl border text-md p-4"
                  onPressEnter={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      handleSubmit();
                    }
                  }}
                />
              </Form.Item>
            </Form>
        </Footer>
      </Flex>
    </>
  );
};

export default MsgsWindow;

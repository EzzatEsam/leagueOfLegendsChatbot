import { Space } from "antd";
import { chatMessage } from "../models/chat";
import Markdown from "react-markdown";

const MsgBox: React.FC<{ msg: chatMessage }> = ({ msg: chatMessage }) => {
  return (
    <Space className="w-4/6 rounded-lg border m-4 text-lg p-4">
      <Markdown>{chatMessage.content}</Markdown>
    </Space>
  );
};

export default MsgBox;

import { Skeleton, Space } from "antd";
import { chatMessage } from "../models/chat";
import Markdown from "react-markdown";

const MsgBox: React.FC<{ msg: chatMessage }> = ({ msg }) => {
  return (
    <Space
      className="w-4/6 rounded-lg border m-4 text-base p-4 shadow-md bg-gray-50"
      style={{ display: "block" }}
    >
      <Skeleton active loading={msg.content === ""} style={{ width: "100%" }}>
        <Markdown>{msg.content}</Markdown>
      </Skeleton>
    </Space>
  );
};

export default MsgBox;

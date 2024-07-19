import React from "react";
import { Layout, Dropdown, Button, Space, MenuProps } from "antd";
import { UserOutlined } from "@ant-design/icons";
import User from "../models/user";
import { DownOutlined } from "@ant-design/icons";

const { Header } = Layout;

interface NavbarProps {
  appName: string;
  user: User;
  selectedModelIdx: number;
  onModelSelect: (model: string) => void;
  availableModels: string[];
  onSignOut: () => void;
}

const Navbar: React.FC<NavbarProps> = ({
  appName,
  user,
  onSignOut,
  onModelSelect,
  availableModels,
  selectedModelIdx
}) => {
  const accountItems: MenuProps["items"] = [
    {
      key: "sign-out",
      label: "Sign Out",
      onClick: onSignOut,
    },
  ];

  const modelItems: MenuProps["items"] = availableModels.map((model) => {
    return {
      key: model,
      label: model,
      onClick: () => onModelSelect(model),
    };
  });

  return (
    <Header
      style={{
        backgroundColor: "#fff",
        padding: "0 20px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        height: "50px",
      }}
    >
      <Space>
        <div style={{ fontSize: "20px" }}>{appName}</div>
        <Dropdown menu={{ items: modelItems, selectable: true }}>
          <Button type="link" size="large">
            {availableModels[selectedModelIdx]} <DownOutlined />
          </Button>
        </Dropdown>
      </Space>
      <Dropdown menu={{ items: accountItems }}>
        <Button type="link" icon={<UserOutlined />} size="large">
          <Space>
            {user.firstName}
            {user.lastName}
          </Space>
        </Button>
      </Dropdown>
    </Header>
  );
};

export default Navbar;

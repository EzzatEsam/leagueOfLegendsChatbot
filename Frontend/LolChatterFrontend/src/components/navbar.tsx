import React from "react";
import { Layout, Dropdown, Button, Space, MenuProps } from "antd";
import { UserOutlined } from "@ant-design/icons";
import User from "../models/user";

const { Header } = Layout;

interface NavbarProps {
  appName: string;
  user: User;

  onSignOut: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ appName, user,onSignOut  }) => {
  const items: MenuProps["items"] = [
    {
      key: "sign-out",
      label: "Sign Out",
      onClick: onSignOut,
    },
  ];

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
      <div style={{ fontSize: "20px" }}>{appName}</div>

      <Dropdown menu={{ items }}>
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

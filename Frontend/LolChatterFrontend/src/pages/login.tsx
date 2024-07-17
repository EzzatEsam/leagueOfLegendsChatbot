import React from "react";
import { Form, Input, Button, Row, Space } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import { TokenManager } from "../lib/tokenManager";
import { message } from "antd";
import { AuthService } from "../lib/authService";
interface LoginFormValues {
  email: string;
  password: string;
  remember: boolean;
}

const LoginPage: React.FC = () => {
  const [messageApi, contextHolder] = message.useMessage();
  const onFinish = async (values: LoginFormValues) => {
    console.log("Received values of form: ", values);
    const service = new AuthService();
    let result = await service.tryLogin(values.email, values.password);

    if (result.success) {
      TokenManager.token = result.data!.accessToken;
      window.location.href = "/";
    } else {
      messageApi.error(result.message);
    }
  };

  return (
    <>
      {contextHolder}
      <Row justify="center" style={{ width: "100vw", marginTop: "50px" }}>
        <Space direction="vertical" align="center" size={"small"}>
          <h2>Login to Your Account</h2>
          <p>Please enter your credentials to log in</p>
          <Form
            name="login_form"
            initialValues={{ remember: true }}
            onFinish={onFinish}
            style={{
              border: "1px solid #ccc",
              padding: "20px",
              borderRadius: "5px",
              minWidth: "400px",
            }}
          >
            <Form.Item
              name="email"
              rules={[
                { required: true, message: "Please input your Email!" },
                { type: "email", message: "Please enter a valid email!" },
              ]}
            >
              <Input prefix={<UserOutlined />} placeholder="Email" />
            </Form.Item>
            <Form.Item
              name="password"
              rules={[
                { required: true, message: "Please input your Password!" },
              ]}
            >
              <Input
                prefix={<LockOutlined />}
                type="password"
                placeholder="Password"
              />
            </Form.Item>
            <Form.Item>
              {/* <Form.Item name="remember" valuePropName="checked" noStyle>
              <Checkbox>Remember me</Checkbox>
            </Form.Item> */}
              <a href="">Forgot password ?</a>
            </Form.Item>
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                style={{ width: "100%" }}
              >
                Log in
              </Button>
            </Form.Item>
            Or <a href="/signup">register now!</a>
          </Form>
        </Space>
      </Row>
    </>
  );
};

export default LoginPage;

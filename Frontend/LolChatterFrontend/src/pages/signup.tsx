import React from "react";
import { Form, Input, Button, Row, Space } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import { message } from "antd";
import { AuthService } from "../lib/authService";

interface SignupFormValues {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const SignupPage: React.FC = () => {
  const [messageApi, contextHolder] = message.useMessage();

  const onFinish = async (values: SignupFormValues) => {
    console.log("Received values of form: ", values);
    const service = new AuthService();
    let result = await service.trySignUp(
      values.firstName,
      values.lastName,
      values.email,
      values.password
    );

    if (result.success) {
      window.location.href = "/login";
    } else {
      messageApi.error(result.message);
    }
  };

  return (
    <>
      {contextHolder}
      <Row justify="center" style={{ width: "100vw", marginTop: "50px" }}>
        <Space direction="vertical" align="center" size={"small"}>
          <h1 className="text-3xl">LolChatter</h1>
          <img src="/logo.png" alt="logo" className="w-20 h-20 m-4" />
          <h2>Create Your Account</h2>
          <p>Please fill in the form to sign up</p>
          <Form
            name="signup_form"
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
              name="firstName"
              rules={[
                { required: true, message: "Please input your First Name!" },
              ]}
            >
              <Input prefix={<UserOutlined />} placeholder="First Name" />
            </Form.Item>
            <Form.Item
              name="lastName"
              rules={[
                { required: true, message: "Please input your Last Name!" },
              ]}
            >
              <Input prefix={<UserOutlined />} placeholder="Last Name" />
            </Form.Item>
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
            <Form.Item
              name="confirmPassword"
              rules={[
                { required: true, message: "Please confirm your Password!" },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue("password") === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(
                      new Error(
                        "The two passwords that you entered do not match!"
                      )
                    );
                  },
                }),
              ]}
            >
              <Input
                prefix={<LockOutlined />}
                type="password"
                placeholder="Confirm Password"
              />
            </Form.Item>
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                style={{ width: "100%" }}
              >
                Sign Up
              </Button>
            </Form.Item>
            Or <a href="/login">log in now!</a>
          </Form>
        </Space>
      </Row>
    </>
  );
};

export default SignupPage;

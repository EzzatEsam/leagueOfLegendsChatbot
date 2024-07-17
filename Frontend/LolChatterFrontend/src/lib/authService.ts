import { Result } from "../models/result";
import User from "../models/user";
import { getServerAddr } from "./ServerCalls";

interface TokenData {
  accessToken: string;
  tokenType: string;
}
export class AuthService {
  private serverAddr: string;

  constructor() {
    this.serverAddr = getServerAddr();
  }

  private async request<T>(
    url: string,
    options: RequestInit
  ): Promise<Result<T>> {
    try {
      const response = await fetch(url, options);
      if (response.ok) {
        const data = (await response.json()) as T;
        return { success: true, data, message: null };
      } else {
        const errorData = await response.json();
        console.error(errorData);
        return {
          success: false,
          data: null,
          message:
            errorData.message ||
            `Error ${response.status}: ${response.statusText}`,
        };
      }
    } catch (error) {
      console.error(error);
      return { success: false, data: null, message: `Error: ${error}` };
    }
  }

  private getHeaders(token?: string): HeadersInit {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
    return headers;
  }

  public async trySignUp(
    firstName: string,
    lastName: string,
    email: string,
    password: string
  ): Promise<Result<null>> {
    const url = `${this.serverAddr}/auth/signup`;
    const options = {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ firstName, lastName, email, password }),
    };
    return this.request<null>(url, options);
  }

  public async tryLogin(
    email: string,
    password: string
  ): Promise<Result<TokenData>> {
    const url = `${this.serverAddr}/auth/login`;
    const options = {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ email, password }),
    };
    return this.request<TokenData>(url, options);
  }

  public async getUser(token: string): Promise<Result<User>> {
    const url = `${this.serverAddr}/auth/me`;
    const options = {
      method: "GET",
      headers: this.getHeaders(token),
    };
    return this.request<User>(url, options);
  }
}

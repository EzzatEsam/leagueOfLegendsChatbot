import User from "../models/user";
import { AuthService } from "./authService";
export class TokenManager {
  static get token() {
    return localStorage.getItem("token");
  }
  static set token(token: string | null) {
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }

  /**
   * Asynchronously tests the token for authentication.
   *
   * @return {Promise<User | null>} The user data if authentication is successful, otherwise null.
   */
  static async testToken(): Promise<User | null> {
    if (!TokenManager.token) {
      return null;
    }
    const service = new AuthService();
    const result = await service.getUser(TokenManager.token!);

    if (result.success) {
      return result.data;
    } else {
      
      TokenManager.token = null;
      return null;
    }
  }

  /**
   * Logs out the user by clearing the token.
   *
   * @return {Promise<void>} A promise that resolves when the logout is complete.
   */
  static async logout() {
    TokenManager.token = null;
  }
}

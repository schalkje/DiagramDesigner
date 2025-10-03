/**
 * Authentication API service
 */
import { apiClient, setToken, removeToken } from "./api-client";
import type { LoginRequest, LoginResponse, RegisterRequest, RegisterResponse } from "../types/api";

export class AuthAPI {
  /**
   * User login
   */
  static async login(email: string, password: string): Promise<LoginResponse> {
    const request: LoginRequest = { email, password };
    const response = await apiClient.post<LoginResponse>("/auth/login", request);

    // Store JWT token
    setToken(response.data.token);

    return response.data;
  }

  /**
   * User registration
   */
  static async register(
    email: string,
    username: string,
    password: string,
    full_name?: string
  ): Promise<RegisterResponse> {
    const request: RegisterRequest = { email, username, password, full_name };
    const response = await apiClient.post<RegisterResponse>("/auth/register", request);

    // Store JWT token
    setToken(response.data.token);

    return response.data;
  }

  /**
   * User logout (client-side only - removes token)
   */
  static logout(): void {
    removeToken();
  }
}

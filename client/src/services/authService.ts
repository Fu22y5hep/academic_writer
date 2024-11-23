import axios from 'axios';
import { API_BASE_URL } from '../config';
import { setToken, removeToken } from '../utils/token';

const API_URL = `${API_BASE_URL}/api/v1`;

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<void> {
    try {
      const response = await axios.post<AuthResponse>(
        `${API_URL}/login/access-token`,
        new URLSearchParams({
          username: credentials.email,
          password: credentials.password,
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );
      setToken(response.data.access_token);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  },

  async register(data: RegisterData): Promise<void> {
    try {
      await axios.post(`${API_URL}/register`, {
        email: data.email,
        password: data.password,
        full_name: data.full_name
      });

      // After successful registration, log in
      await this.login({
        email: data.email,
        password: data.password,
      });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      console.error('Registration error:', error.response?.data);
      throw new Error(errorMessage);
    }
  },

  logout(): void {
    removeToken();
  },
};

export default authService;

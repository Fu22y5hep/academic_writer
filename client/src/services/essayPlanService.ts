import axios from 'axios';
import { API_BASE_URL } from '../config';
import { getToken } from '../utils/token';

export interface OutlineSection {
  title: string;
  content: string;
  subsections: OutlineSection[];
}

export interface OutlineResponse {
  success: boolean;
  outline?: {
    sections: OutlineSection[];
  };
  essay_type?: string;
  topic?: string;
  word_count?: number;
  thesis_statement?: string;
  error?: string;
}

export interface GenerateOutlineParams {
  topic: string;
  essay_type: string;
  word_count?: number;
  thesis_statement?: string;
}

export interface EssayPlan {
  id: number;
  title: string;
  essayType: string;
  topic: string;
  thesisStatement?: string;
  outline?: Record<string, any>;
  guidelines?: Record<string, any>;
  wordCountTarget?: number;
}

export interface CreateEssayPlanDto {
  title: string;
  essayType: string;
  topic: string;
  thesisStatement?: string;
  outline?: Record<string, any>;
  guidelines?: Record<string, any>;
  wordCountTarget?: number;
}

export interface UpdateEssayPlanDto {
  title?: string;
  essayType?: string;
  topic?: string;
  thesisStatement?: string;
  outline?: Record<string, any>;
  guidelines?: Record<string, any>;
  wordCountTarget?: number;
}

const API_URL = `${API_BASE_URL}/api/v1`;

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const essayPlanService = {
  async createPlan(plan: CreateEssayPlanDto): Promise<EssayPlan> {
    const response = await api.post('/essay-plans', plan);
    return response.data;
  },

  async getUserPlans(): Promise<EssayPlan[]> {
    const response = await api.get('/essay-plans');
    return response.data;
  },

  async getPlan(id: number): Promise<EssayPlan> {
    const response = await api.get(`/essay-plans/${id}`);
    return response.data;
  },

  async updatePlan(id: number, plan: UpdateEssayPlanDto): Promise<EssayPlan> {
    const response = await api.put(`/essay-plans/${id}`, plan);
    return response.data;
  },

  async deletePlan(id: number): Promise<void> {
    await api.delete(`/essay-plans/${id}`);
  },

  async generateOutline(params: GenerateOutlineParams): Promise<OutlineResponse> {
    try {
      const response = await api.post('/generate-outline', params);
      return {
        success: true,
        ...response.data
      };
    } catch (error: any) {
      if (error.response?.status === 401) {
        // Handle unauthorized error
        return {
          success: false,
          error: 'Please log in to generate outlines'
        };
      }
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to generate outline'
      };
    }
  }
};

export default essayPlanService;

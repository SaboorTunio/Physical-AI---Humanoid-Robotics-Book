/**
 * API service for communicating with Living Textbook RAG Backend
 * Handles HTTP requests, error handling, and response parsing
 */

import axios, { AxiosInstance, AxiosError } from "axios";
import {
  ChatRequest,
  ChatResponse,
  IngestRequest,
  IngestResponse,
  HealthResponse,
  MetadataResponse,
  ApiError,
  ApiClient,
} from "@/types/api";

class ApiService implements ApiClient {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor(baseUrl: string = process.env.REACT_APP_API_URL || "http://localhost:8000") {
    this.baseUrl = baseUrl;

    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => this.handleError(error)
    );
  }

  /**
   * Handle API errors and convert to standardized format
   */
  private handleError(error: AxiosError): never {
    if (error.response?.data) {
      const errorData = error.response.data as any;
      const apiError: ApiError = {
        code: errorData.error?.code || "UNKNOWN_ERROR",
        message: errorData.error?.message || error.message,
        status: error.response.status,
        details: errorData,
      };
      throw apiError;
    }

    throw {
      code: "NETWORK_ERROR",
      message: error.message,
      status: error.response?.status || 0,
    } as ApiError;
  }

  /**
   * POST /api/chat
   * Send a question to the RAG system and get an AI-generated answer
   */
  async chat(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await this.client.post<ChatResponse>("/api/chat", request);
      return response.data;
    } catch (error) {
      console.error("Chat request failed:", error);
      throw error;
    }
  }

  /**
   * POST /api/ingest
   * Trigger content ingestion/reingestion (admin only)
   */
  async ingest(request: IngestRequest): Promise<IngestResponse> {
    try {
      const response = await this.client.post<IngestResponse>("/api/ingest", request);
      return response.data;
    } catch (error) {
      console.error("Ingest request failed:", error);
      throw error;
    }
  }

  /**
   * GET /api/health
   * Check system health and service status
   */
  async health(): Promise<HealthResponse> {
    try {
      const response = await this.client.get<HealthResponse>("/api/health");
      return response.data;
    } catch (error) {
      console.error("Health check failed:", error);
      throw error;
    }
  }

  /**
   * GET /api/metadata
   * Get chapter list and textbook metadata
   */
  async metadata(moduleId?: number): Promise<MetadataResponse> {
    try {
      const params = moduleId ? { module_id: moduleId } : {};
      const response = await this.client.get<MetadataResponse>("/api/metadata", {
        params,
      });
      return response.data;
    } catch (error) {
      console.error("Metadata request failed:", error);
      throw error;
    }
  }

  /**
   * Set authentication token for admin operations
   */
  setAuthToken(token: string): void {
    this.client.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  }

  /**
   * Clear authentication token
   */
  clearAuthToken(): void {
    delete this.client.defaults.headers.common["Authorization"];
  }

  /**
   * Set base URL for API requests (useful for multi-environment setup)
   */
  setBaseUrl(baseUrl: string): void {
    this.baseUrl = baseUrl;
    this.client.defaults.baseURL = baseUrl;
  }

  /**
   * Get current base URL
   */
  getBaseUrl(): string {
    return this.baseUrl;
  }
}

// Export singleton instance
export const apiClient = new ApiService();

// Export for testing/dependency injection
export default apiClient;

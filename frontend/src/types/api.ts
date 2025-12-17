/**
 * TypeScript type definitions for Living Textbook RAG API
 * Auto-generated types matching backend OpenAPI specification
 */

// ============================================================================
// Chat Endpoint Types
// ============================================================================

export interface ChatRequest {
  query: string;
  session_id?: string;
  highlighted_context?: string;
  chapter_context?: number;
}

export interface ChatResponseSource {
  chapter_index: number;
  chapter_title: string;
  section: string;
  excerpt: string;
  confidence: number;
}

export interface ChatResponse {
  session_id: string;
  answer: string;
  sources: ChatResponseSource[];
  confidence: number;
  timestamp: string;
  message_id: string;
}

// ============================================================================
// Ingest Endpoint Types
// ============================================================================

export interface IngestRequest {
  force_refresh?: boolean;
}

export interface IngestChapterResult {
  chapter_index: number;
  title: string;
  chunks_created: number;
  status: "success" | "error";
  error_message?: string;
}

export interface IngestResponse {
  status: "success" | "partial";
  chapters_processed: number;
  chunks_created: number;
  results: IngestChapterResult[];
  timestamp: string;
}

// ============================================================================
// Health Endpoint Types
// ============================================================================

export interface ServiceStatus {
  name: string;
  status: "ok" | "degraded" | "error";
  latency_ms?: number;
  message?: string;
}

export interface HealthResponse {
  status: "healthy" | "unhealthy";
  services: ServiceStatus[];
  version: string;
  timestamp: string;
}

// ============================================================================
// Metadata Endpoint Types
// ============================================================================

export interface ChapterMetadata {
  chapter_index: number;
  title: string;
  module: number;
  part: number;
  learning_objectives: string[];
  keywords: string[];
  prerequisites: number[];
  chunks_count: number;
}

export interface MetadataResponse {
  chapters: ChapterMetadata[];
  total_chapters: number;
  total_chunks: number;
  modules: number;
  last_updated: string;
}

// ============================================================================
// Error Types
// ============================================================================

export interface ErrorDetail {
  code: string;
  message: string;
  detail?: string;
}

export interface ErrorResponse {
  error: ErrorDetail;
  timestamp: string;
  request_id: string;
}

// ============================================================================
// Internal State Types
// ============================================================================

export interface ChatSession {
  id: string;
  user_id?: string;
  chapter_context?: number;
  is_active: boolean;
  message_count: number;
  created_at: string;
  updated_at: string;
  last_activity_at: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: "user" | "assistant";
  content: string;
  highlighted_context?: string;
  source_chunks?: ChatResponseSource[];
  confidence?: number;
  created_at: string;
}

// ============================================================================
// Component Props Types
// ============================================================================

export interface AiAssistantProps {
  sessionId?: string;
  onMessage?: (message: ChatMessage) => void;
  highlightedText?: string;
  chapterIndex?: number;
}

export interface ChatWidgetProps {
  sessionId: string;
  messages: ChatMessage[];
  onSendMessage: (query: string) => Promise<void>;
  isLoading?: boolean;
  error?: string;
}

export interface HighlightMenuProps {
  position: { x: number; y: number };
  selectedText: string;
  onAsk: (text: string) => void;
  onClose: () => void;
}

export interface ContextHighlightProps {
  children: React.ReactNode;
  onHighlight?: (text: string, context: HTMLElement) => void;
  disabled?: boolean;
}

// ============================================================================
// Request/Response Interceptor Types
// ============================================================================

export interface ApiRequestConfig {
  method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
  headers?: Record<string, string>;
  timeout?: number;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}

export interface ApiError {
  code: string;
  message: string;
  status: number;
  details?: ErrorResponse;
}

// ============================================================================
// Utility Types
// ============================================================================

export type AsyncFunction<T> = () => Promise<T>;
export type OnError = (error: ApiError) => void;
export type OnSuccess<T> = (data: T) => void;

export interface ApiClient {
  chat: (request: ChatRequest) => Promise<ChatResponse>;
  ingest: (request: IngestRequest) => Promise<IngestResponse>;
  health: () => Promise<HealthResponse>;
  metadata: (moduleId?: number) => Promise<MetadataResponse>;
}

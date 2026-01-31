// TypeScript types for Task entities
import { UUID } from 'crypto';

export interface Task {
  id: UUID;
  user_id: UUID;
  title: string;
  description?: string;
  completed: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface TaskCreateData {
  title: string;
  description?: string;
}

export interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface User {
  id: UUID;
  email: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface AuthResponse {
  token: string;
  user: User;
}
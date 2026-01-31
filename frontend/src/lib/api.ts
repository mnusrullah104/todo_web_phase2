// Centralized API client with JWT injection
import axios from 'axios';

// Function to detect available backend port
const getBackendURL = async (): Promise<string> => {
  // Try 8001 first (Todo API), then 8000 as fallback
  const ports = [8001, 8000];

  for (const port of ports) {
    try {
      const url = `http://localhost:${port}`;
      const response = await fetch(`${url}/api/auth/login`, {
        method: 'HEAD',
        signal: AbortSignal.timeout(2000)
      });
      // Accept any response (even 405 Method Not Allowed means the endpoint exists)
      if (response.status !== 404) {
        return url;
      }
    } catch (error) {
      // Port not available, try next
      continue;
    }
  }

  // Default to 8001 (Todo API port)
  return 'http://localhost:8001';
};

// Get base URL with fallback
const getBaseURL = (): string => {
  if (typeof window !== 'undefined') {
    // Client-side: use stored URL or default
    const storedURL = sessionStorage.getItem('api_base_url');
    if (storedURL) return storedURL;
  }
  return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';
};

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token && token.trim() !== '') {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors and port fallback
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token might be expired or invalid, redirect to login
      localStorage.removeItem('token');
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }

    // Handle connection errors with port fallback
    if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
      if (typeof window !== 'undefined') {
        const newURL = await getBackendURL();
        sessionStorage.setItem('api_base_url', newURL);
        apiClient.defaults.baseURL = newURL;

        // Retry the request with new URL
        return apiClient.request(error.config);
      }
    }

    return Promise.reject(error);
  }
);

// Export the configured API client
export default apiClient;

// API endpoints for tasks
export const taskApi = {
  // Get all tasks for a user
  getTasks: (userId: string) => {
    return apiClient.get(`/api/${userId}/tasks`);
  },

  // Create a new task
  createTask: (userId: string, taskData: { title: string; description?: string }) => {
    return apiClient.post(`/api/${userId}/tasks`, taskData);
  },

  // Get a specific task
  getTask: (userId: string, taskId: string) => {
    return apiClient.get(`/api/${userId}/tasks/${taskId}`);
  },

  // Update a task
  updateTask: (userId: string, taskId: string, taskData: { title?: string; description?: string; completed?: boolean }) => {
    return apiClient.put(`/api/${userId}/tasks/${taskId}`, taskData);
  },

  // Delete a task
  deleteTask: (userId: string, taskId: string) => {
    return apiClient.delete(`/api/${userId}/tasks/${taskId}`);
  },

  // Toggle task completion
  toggleTaskCompletion: (userId: string, taskId: string, completed: boolean) => {
    return apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`, { completed });
  },
};

// Initialize backend URL detection on client
if (typeof window !== 'undefined') {
  getBackendURL().then(url => {
    sessionStorage.setItem('api_base_url', url);
    apiClient.defaults.baseURL = url;
  });
}

// API endpoints for authentication
export const authApi = {
  // Login
  login: async (email: string, password: string) => {
    try {
      const baseURL = await getBackendURL();
      // Send credentials in JSON body
      const response = await fetch(`${baseURL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Login failed with status: ${response.status}`);
      }

      const data = await response.json();
      if (data.access_token) {
        localStorage.setItem('token', data.access_token);
        return data;
      } else {
        throw new Error('No token returned from login');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Signup
  signup: async (email: string, password: string) => {
    try {
      const baseURL = await getBackendURL();
      // Send credentials in JSON body
      const response = await fetch(`${baseURL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Signup failed with status: ${response.status}`);
      }

      const data = await response.json();
      if (data.access_token) {
        localStorage.setItem('token', data.access_token);
        return data;
      } else {
        throw new Error('No token returned from signup');
      }
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    }
  },

  // Logout
  logout: () => {
    localStorage.removeItem('token');
  },
};
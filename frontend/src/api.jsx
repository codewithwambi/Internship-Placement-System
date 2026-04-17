import axios from 'axios';

// Professional tip: Create an 'instance' so you don't repeat the Base URL
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
});

// This is the "Passport Stamper"
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      // Professional standard: The "Bearer" prefix is required by JWT
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
export const loginUser = async (username, password) => {
  const response = await api.post('token/', { username, password });
  
  if (response.data.access) {
    localStorage.setItem('accessToken', response.data.access);
    localStorage.setItem('userRole', response.data.role);
    localStorage.setItem('username', response.data.username);

    // CRITICAL: Manually attach the token to the header for the 
    // immediate requests that happen right after login.
    api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
  }
  return response.data;
};
export const uploadDocument = (documentName, file) => {
  const formData = new FormData();
  formData.append('document_name', documentName);
  formData.append('file', file);
  
  // REMOVED: formData.append('student', 1); 
  // Django's perform_create now handles this via request.user!

  return api.post('documents/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.clear();
      window.location.href = '/'; // Kick back to login
    }
    return Promise.reject(error);
  }
);
export default api;
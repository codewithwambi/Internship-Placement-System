import axios from 'axios';

// Professional tip: Create an 'instance' so you don't repeat the Base URL
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
});
// Add this to your src/api.js
export const loginUser = async (username, password) => {
  const response = await api.post('token/', { username, password });
  
  // Professional move: Save the token in localStorage
  if (response.data.access) {
    localStorage.setItem('accessToken', response.data.access);
    localStorage.setItem('userRole', response.data.role); // We'll send the role from Django
  }
  return response.data;
};

export const uploadDocument = (documentName, file) => {
  // We use FormData because we are sending a physical file, not just text
  const formData = new FormData();
  formData.append('document_name', documentName);
  formData.append('file', file);
  // Temporary: manual student ID until we build login
  formData.append('student', 1); 

  return api.post('documents/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export default api;
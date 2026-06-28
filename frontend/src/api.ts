import axios from 'axios';

// Configura a URL base do seu backend em FastAPI
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

export default api;
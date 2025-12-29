import axios from 'axios';

const rawBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const baseNoSlash = String(rawBase).replace(/\/$/, '');

const api = axios.create({
  baseURL: `${baseNoSlash}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;

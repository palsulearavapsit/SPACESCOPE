import apiClient from '../api';

// Sky Events
export const skyEventsAPI = {
  getUpcoming: (daysAhead = 30) => 
    apiClient.get('/sky-events/upcoming', { params: { days_ahead: daysAhead } }),
  
  getByType: (eventType) =>
    apiClient.get('/sky-events/upcoming', { params: { event_type: eventType } }),
  
  getVisible: (lat, lon, days = 30) =>
    apiClient.get('/sky-events/visible', { 
      params: { latitude: lat, longitude: lon, days_ahead: days } 
    }),
};

// Space Weather
export const spaceWeatherAPI = {
  getActive: () => 
    apiClient.get('/weather/alerts/active'),
  
  getByType: (alertType) =>
    apiClient.get(`/weather/alerts/${alertType}`),
};

// Missions
export const missionsAPI = {
  getAll: () => 
    apiClient.get('/missions'),
  
  getByStatus: (status) =>
    apiClient.get(`/missions/status/${status}`),
};

// Chat
export const chatAPI = {
  send: (message, contextType = null) =>
    apiClient.post('/chat', { 
      user_message: message,
      context_type: contextType 
    }),
};

// Learning
export const learningAPI = {
  getContent: (category = null, difficulty = null) =>
    apiClient.get('/learning/content', { 
      params: { category, difficulty } 
    }),
  
  submitQuiz: (contentId, answers) =>
    apiClient.post('/learning/quiz/submit', {
      content_id: contentId,
      answers,
    }),
};

// Earth Impact
export const earthImpactAPI = {
  getByType: (impactType, limit = 50) =>
    apiClient.get(`/earth-impact/${impactType}`, { params: { limit } }),
  
  getRecent: (days = 7, limit = 100) =>
    apiClient.get('/earth-impact/recent', { params: { days, limit } }),
};

import { create } from 'zustand';

export const useStore = create((set) => ({
  // Sky Events
  skyEvents: [],
  setSkyEvents: (events) => set({ skyEvents: events }),
  
  // Space Weather
  weatherAlerts: [],
  setWeatherAlerts: (alerts) => set({ weatherAlerts: alerts }),
  
  // User preferences
  userLocation: { latitude: 37.7749, longitude: -122.4194 }, // SF default
  setUserLocation: (location) => set({ userLocation: location }),
  
  // Loading states
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
  
  // User
  isLoggedIn: false,
  setIsLoggedIn: (loggedIn) => set({ isLoggedIn: loggedIn }),
}));

import React, { useEffect, useState } from 'react';
import { skyEventsAPI, spaceWeatherAPI, missionsAPI } from '../services/api';
import { useStore } from '../store';

function Dashboard() {
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [activeMissions, setActiveMissions] = useState([]);
  const isLoading = useStore((state) => state.isLoading);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [eventsRes, alertsRes, missionsRes] = await Promise.all([
        skyEventsAPI.getUpcoming(30),
        spaceWeatherAPI.getActive(),
        missionsAPI.getByStatus('active'),
      ]);
      
      setUpcomingEvents(eventsRes.data.slice(0, 5));
      setAlerts(alertsRes.data);
      setActiveMissions(missionsRes.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header with Neon */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold neon mb-2">
          🌌 Welcome to SpaceScope 🌌
        </h1>
        <p className="text-gray-300 text-lg glow-text">Your gateway to space exploration and cosmic events</p>
        <div className="mt-4 h-1 w-24 mx-auto bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-500 rounded-full"></div>
      </div>

      {/* Stats Grid with Space Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title="Upcoming Events" value={upcomingEvents.length} icon="🌠" />
        <StatCard title="Active Alerts" value={alerts.length} icon="⚠️" />
        <StatCard title="Active Missions" value={activeMissions.length} icon="🚀" />
        <StatCard title="Learning Items" value="12" icon="📚" />
      </div>

      {/* Upcoming Events */}
      <div className="glass-card space-card glow-border">
        <h2 className="text-2xl font-bold neon mb-4 flex items-center gap-2">
          📅 Upcoming Sky Events
        </h2>
        <div className="space-y-3">
          {upcomingEvents.length > 0 ? (
            upcomingEvents.map((event) => (
              <div key={event.id} className="flex justify-between items-center p-4 bg-indigo-900/20 rounded-lg border border-indigo-500/30 hover:border-indigo-400/60 transition glow-border">
                <div>
                  <p className="font-semibold text-cyan-300">{event.name}</p>
                  <p className="text-gray-400 text-sm">{event.event_type}</p>
                </div>
                <p className="text-indigo-300 text-sm font-mono">{new Date(event.start_time).toLocaleDateString()}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-400 text-center py-4">No upcoming events</p>
          )}
        </div>
      </div>

      {/* Space Weather Alerts */}
      {alerts.length > 0 && (
        <div className="glass-card space-card glow-border border-red-500/30">
          <h2 className="text-2xl font-bold text-red-300 mb-4 flex items-center gap-2">
            ⚠️ Space Weather Alerts
          </h2>
          <div className="space-y-3">
            {alerts.slice(0, 3).map((alert) => (
              <div key={alert.id} className="p-4 bg-red-900/30 rounded-lg border border-red-500/40 hover:border-red-400/60 transition">
                <p className="font-semibold text-red-200">{alert.title}</p>
                <p className="text-gray-300 text-sm">{alert.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({ title, value, icon }) {
  return (
    <div className="glass-card space-card glow-border bg-gradient-to-br from-indigo-900/30 to-purple-900/20 hover:from-indigo-800/40 hover:to-purple-800/30">
      <p className="text-cyan-300 text-sm mb-2 font-semibold">{title}</p>
      <div className="flex items-end gap-3">
        <p className="text-4xl font-bold neon">{value}</p>
        <p className="text-3xl mb-1 float-animation">{icon}</p>
      </div>
    </div>
  );
}

export default Dashboard;

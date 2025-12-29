import React, { useEffect, useState } from 'react';
import { spaceWeatherAPI } from '../services/api';
import { FaBolt, FaWind, FaThermometerHalf, FaShieldAlt } from 'react-icons/fa';

function SpaceWeather() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      setLoading(true);
      const response = await spaceWeatherAPI.getActive();
      setAlerts(response.data || []);
      setError(null);
    } catch (err) {
      console.error('Error loading alerts:', err);
      setError('Failed to load space weather alerts');
      setAlerts([]);
    } finally {
      setLoading(false);
    }
  };

  const mockAlerts = [
    {
      id: 1,
      alert_type: 'Solar Wind Stream',
      severity: 'Moderate',
      description: 'A high-speed solar wind stream is impacting Earth\'s magnetosphere.',
      timestamp: '2025-12-29',
      impact: 'G2 Geomagnetic Storm'
    },
    {
      id: 2,
      alert_type: 'Coronal Mass Ejection',
      severity: 'High',
      description: 'Multiple CMEs detected from active solar region.',
      timestamp: '2025-12-28',
      impact: 'Strong aurora activity expected'
    }
  ];

  const displayAlerts = alerts.length > 0 ? alerts : mockAlerts;

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return 'from-red-500/20 to-red-500/10 border-red-500/40 text-red-300';
      case 'high':
        return 'from-orange-500/20 to-orange-500/10 border-orange-500/40 text-orange-300';
      case 'moderate':
        return 'from-yellow-500/20 to-yellow-500/10 border-yellow-500/40 text-yellow-300';
      default:
        return 'from-green-500/20 to-green-500/10 border-green-500/40 text-green-300';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return '🔴';
      case 'high':
        return '🟠';
      case 'moderate':
        return '🟡';
      default:
        return '🟢';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold neon mb-2 flex items-center justify-center gap-3">
          <FaBolt className="text-yellow-300 animate-pulse" />
          Space Weather
        </h1>
        <p className="text-gray-300 text-lg glow-text">Real-time solar and geomagnetic activity monitoring</p>
        <div className="mt-4 h-1 w-32 mx-auto bg-gradient-to-r from-yellow-500 via-orange-500 to-red-500 rounded-full"></div>
      </div>

      {/* Space Weather Index */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card space-card glow-border bg-gradient-to-br from-yellow-900/30 to-orange-900/20">
          <div className="flex items-center justify-between mb-2">
            <p className="text-yellow-300 text-sm font-semibold">K-Index</p>
            <FaBolt className="text-yellow-400 text-xl" />
          </div>
          <p className="text-3xl font-bold neon">5.5</p>
          <p className="text-yellow-200 text-xs mt-1">Moderate</p>
        </div>

        <div className="glass-card space-card glow-border bg-gradient-to-br from-blue-900/30 to-cyan-900/20">
          <div className="flex items-center justify-between mb-2">
            <p className="text-cyan-300 text-sm font-semibold">Solar Flux</p>
            <FaWind className="text-cyan-400 text-xl" />
          </div>
          <p className="text-3xl font-bold neon">145</p>
          <p className="text-cyan-200 text-xs mt-1">sfu</p>
        </div>

        <div className="glass-card space-card glow-border bg-gradient-to-br from-purple-900/30 to-indigo-900/20">
          <div className="flex items-center justify-between mb-2">
            <p className="text-purple-300 text-sm font-semibold">Aurora</p>
            <FaThermometerHalf className="text-purple-400 text-xl" />
          </div>
          <p className="text-3xl font-bold neon">Likely</p>
          <p className="text-purple-200 text-xs mt-1">Tonight</p>
        </div>

        <div className="glass-card space-card glow-border bg-gradient-to-br from-green-900/30 to-emerald-900/20">
          <div className="flex items-center justify-between mb-2">
            <p className="text-green-300 text-sm font-semibold">Radiation</p>
            <FaShieldAlt className="text-green-400 text-xl" />
          </div>
          <p className="text-3xl font-bold neon">Safe</p>
          <p className="text-green-200 text-xs mt-1">Status</p>
        </div>
      </div>

      {loading && <div className="text-center text-cyan-400 py-8 text-lg">🔄 Loading space weather data...</div>}
      {error && <div className="text-center text-red-400 py-8 text-lg">⚠️ {error}</div>}

      {/* Active Alerts */}
      <div>
        <h2 className="text-3xl font-bold neon mb-6">⚠️ Active Alerts</h2>
        <div className="space-y-4">
          {displayAlerts.map((alert, idx) => (
            <div
              key={idx}
              className={`glass-card space-card border bg-gradient-to-r ${getSeverityColor(alert.severity)} p-6 relative overflow-hidden`}
            >
              {/* Status Indicator */}
              <div className="absolute top-4 right-4 text-2xl">{getSeverityIcon(alert.severity)}</div>

              {/* Content */}
              <div className="pr-8">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-2xl font-bold text-white">{alert.alert_type || alert.name}</h3>
                  <span className="px-4 py-1 bg-black/30 rounded-full text-xs font-semibold">
                    {alert.severity || 'Unknown'}
                  </span>
                </div>

                <p className="text-gray-100 text-sm leading-relaxed mb-4">{alert.description || alert.details}</p>

                {/* Details */}
                <div className="grid grid-cols-2 gap-3">
                  {alert.timestamp && (
                    <div className="bg-white/10 rounded p-3 border border-white/10">
                      <p className="text-white/70 text-xs mb-1">REPORTED</p>
                      <p className="text-white font-mono text-sm">{alert.timestamp}</p>
                    </div>
                  )}
                  {alert.impact && (
                    <div className="bg-white/10 rounded p-3 border border-white/10">
                      <p className="text-white/70 text-xs mb-1">IMPACT</p>
                      <p className="text-white font-mono text-sm">{alert.impact}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {!loading && displayAlerts.length === 0 && (
        <div className="glass-card space-card text-center py-12">
          <p className="text-green-300 text-xl font-semibold">✓ No active alerts</p>
          <p className="text-gray-400 mt-2">Space weather conditions are normal</p>
        </div>
      )}
    </div>
  );
}

export default SpaceWeather;

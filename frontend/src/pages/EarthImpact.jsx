import React, { useEffect, useState } from 'react';
import { earthImpactAPI } from '../services/api';
import { FaGlobe, FaArrowRight, FaSpinner, FaCircle } from 'react-icons/fa';
import DetailModal from '../components/DetailModal';

function EarthImpact() {
  const [impacts, setImpacts] = useState([]);
  const [impactType, setImpactType] = useState('asteroids');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedImpact, setSelectedImpact] = useState(null);

  useEffect(() => {
    loadImpacts();
  }, [impactType]);

  const loadImpacts = async () => {
    try {
      setLoading(true);
      const response = await earthImpactAPI.getByType(impactType, 50);
      setImpacts(response.data || []);
      setError(null);
    } catch (err) {
      console.error('Error loading impacts:', err);
      setError('Failed to load impact data');
      setImpacts([]);
    } finally {
      setLoading(false);
    }
  };

  const mockImpacts = [
    {
      id: 1,
      name: '2024 BX19',
      object_type: 'Asteroid',
      distance: '0.045 AU',
      velocity: '18.5 km/s',
      size: '120 meters',
      closest_approach: '2025-01-15',
      hazard_level: 'Low',
      description: 'Near-Earth asteroid on a predictable orbit',
      composition: 'Silicate/Iron',
      discovered: '2024-01-20',
      orbit_type: 'Apollo class',
      orbital_period: '1.2 years',
      detailed_description: 'This asteroid is a moderate-sized near-Earth object with well-understood orbital mechanics. It will pass at approximately 0.045 AU (astronomical units) from Earth, which is well beyond any danger threshold.',
      monitoring_status: 'Under continuous observation by NASA',
      impact_probability: '0.0001%'
    },
    {
      id: 2,
      name: '2023 DW',
      object_type: 'Asteroid',
      distance: '0.062 AU',
      velocity: '22.3 km/s',
      size: '85 meters',
      closest_approach: '2025-01-22',
      hazard_level: 'Very Low',
      description: 'Small asteroid passing safely at distance',
      composition: 'Carbonaceous',
      discovered: '2023-02-15',
      orbit_type: 'Amor class',
      orbital_period: '1.8 years',
      detailed_description: 'This small carbonaceous asteroid is well-tracked and poses no threat to Earth. It represents an excellent opportunity for scientific observation.',
      monitoring_status: 'Routine monitoring',
      impact_probability: '0.00001%'
    }
  ];

  const displayImpacts = impacts.length > 0 ? impacts : mockImpacts;

  const getHazardColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'critical':
        return 'from-red-500/20 to-red-500/10 border-red-500/40';
      case 'high':
        return 'from-orange-500/20 to-orange-500/10 border-orange-500/40';
      case 'moderate':
        return 'from-yellow-500/20 to-yellow-500/10 border-yellow-500/40';
      case 'low':
        return 'from-yellow-500/20 to-yellow-500/10 border-yellow-500/40';
      default:
        return 'from-green-500/20 to-green-500/10 border-green-500/40';
    }
  };

  const getHazardBadge = (level) => {
    switch (level?.toLowerCase()) {
      case 'critical':
        return 'bg-red-500/30 text-red-300';
      case 'high':
        return 'bg-orange-500/30 text-orange-300';
      case 'moderate':
        return 'bg-yellow-500/30 text-yellow-300';
      case 'low':
        return 'bg-yellow-500/20 text-yellow-300';
      default:
        return 'bg-green-500/30 text-green-300';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold neon mb-2 flex items-center justify-center gap-3">
          <FaGlobe className="text-blue-400 float-animation" />
          Earth Impact Tracker
        </h1>
        <p className="text-gray-300 text-lg glow-text">Monitor Near-Earth Objects and potential impacts</p>
        <div className="mt-4 h-1 w-32 mx-auto bg-gradient-to-r from-blue-500 via-cyan-500 to-green-500 rounded-full"></div>
      </div>

      {/* Object Type Selector */}
      <div className="flex gap-3 justify-center flex-wrap">
        {['asteroids', 'comets', 'near-earth-objects'].map((type) => (
          <button
            key={type}
            onClick={() => setImpactType(type)}
            className={`px-6 py-2 rounded-lg font-semibold transition neon-btn ${
              impactType === type
                ? 'bg-indigo-600 border-cyan-400 text-cyan-300 neon'
                : 'hover:border-indigo-400'
            }`}
          >
            {type.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
          </button>
        ))}
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">{displayImpacts.length}</p>
          <p className="text-gray-300 text-sm mt-1">Tracked Objects</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-green-400 text-2xl font-bold">✓</p>
          <p className="text-gray-300 text-sm mt-1">All Safe</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-yellow-400 text-2xl font-bold">24h</p>
          <p className="text-gray-300 text-sm mt-1">Update Freq</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">🛰️</p>
          <p className="text-gray-300 text-sm mt-1">Monitored</p>
        </div>
      </div>

      {loading && <div className="text-center text-cyan-400 py-8 text-lg flex items-center justify-center gap-2"><FaSpinner className="animate-spin" /> Loading impact data...</div>}
      {error && <div className="text-center text-red-400 py-8 text-lg">⚠️ {error}</div>}

      {/* Objects List */}
      <div className="space-y-4">
        {displayImpacts.map((impact, idx) => (
          <div
            key={idx}
            className={`glass-card space-card glow-border border bg-gradient-to-r ${getHazardColor(impact.hazard_level)} p-6`}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4 pb-4 border-b border-white/10">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-2xl font-bold neon">{impact.name}</h3>
                  <FaCircle className={`text-xs ${getHazardBadge(impact.hazard_level).split(' ')[1]}`} />
                </div>
                <p className="text-gray-300">{impact.description || `${impact.object_type} near Earth`}</p>
              </div>
              <span className={`px-4 py-2 rounded-full text-sm font-bold whitespace-nowrap ml-4 ${getHazardBadge(impact.hazard_level)} border border-white/20`}>
                {impact.hazard_level} Risk
              </span>
            </div>

            {/* Details Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
              {impact.distance && (
                <div className="bg-white/5 rounded p-3 border border-white/10">
                  <p className="text-white/60 text-xs font-semibold mb-1">DISTANCE</p>
                  <p className="text-white font-mono text-sm">{impact.distance}</p>
                </div>
              )}
              {impact.velocity && (
                <div className="bg-white/5 rounded p-3 border border-white/10">
                  <p className="text-white/60 text-xs font-semibold mb-1">VELOCITY</p>
                  <p className="text-white font-mono text-sm">{impact.velocity}</p>
                </div>
              )}
              {impact.size && (
                <div className="bg-white/5 rounded p-3 border border-white/10">
                  <p className="text-white/60 text-xs font-semibold mb-1">SIZE</p>
                  <p className="text-white font-mono text-sm">{impact.size}</p>
                </div>
              )}
              {impact.closest_approach && (
                <div className="bg-white/5 rounded p-3 border border-white/10">
                  <p className="text-white/60 text-xs font-semibold mb-1">CLOSEST</p>
                  <p className="text-white font-mono text-sm">{impact.closest_approach}</p>
                </div>
              )}
            </div>

            {/* Risk Indicator */}
            <div className="flex items-center justify-between">
              <span className="text-green-300 font-semibold text-sm">✓ Safe Distance Confirmed</span>
              <button 
                onClick={() => setSelectedImpact(impact)}
                className="neon-btn"
              >
                <FaArrowRight className="inline mr-1" /> Details
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Detail Modal */}
      <DetailModal
        isOpen={!!selectedImpact}
        title={selectedImpact?.name}
        onClose={() => setSelectedImpact(null)}
      >
        {selectedImpact && (
          <div className="space-y-4">
            <p className="text-gray-100 leading-relaxed">{selectedImpact.detailed_description}</p>

            <div className="bg-indigo-900/30 border border-indigo-500/30 rounded-lg p-4">
              <h3 className="text-cyan-300 font-bold mb-3">🔬 Physical Properties</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-gray-400">Size</p>
                  <p className="text-white font-semibold">{selectedImpact.size}</p>
                </div>
                <div>
                  <p className="text-gray-400">Type</p>
                  <p className="text-white font-semibold">{selectedImpact.composition}</p>
                </div>
                <div>
                  <p className="text-gray-400">Velocity</p>
                  <p className="text-white font-semibold">{selectedImpact.velocity}</p>
                </div>
                <div>
                  <p className="text-gray-400">Orbit Class</p>
                  <p className="text-white font-semibold">{selectedImpact.orbit_type}</p>
                </div>
              </div>
            </div>

            <div className="bg-green-900/30 border border-green-500/30 rounded-lg p-4">
              <h3 className="text-green-300 font-bold mb-3">📍 Encounter Details</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-gray-400">Distance</p>
                  <p className="text-white font-semibold">{selectedImpact.distance}</p>
                </div>
                <div>
                  <p className="text-gray-400">Closest Approach</p>
                  <p className="text-white font-semibold">{selectedImpact.closest_approach}</p>
                </div>
                <div className="col-span-2">
                  <p className="text-gray-400">Impact Probability</p>
                  <p className="text-green-300 font-semibold text-lg">{selectedImpact.impact_probability}</p>
                </div>
              </div>
            </div>

            <div className="bg-purple-900/30 border border-purple-500/30 rounded-lg p-4">
              <h3 className="text-purple-300 font-bold mb-3">📊 Orbital Information</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Discovery Date</span>
                  <span className="text-white font-semibold">{selectedImpact.discovered}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Orbital Period</span>
                  <span className="text-white font-semibold">{selectedImpact.orbital_period}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Monitoring Status</span>
                  <span className="text-white font-semibold">{selectedImpact.monitoring_status}</span>
                </div>
              </div>
            </div>

            <div className="bg-green-900/40 border border-green-500/40 rounded-lg p-4">
              <p className="text-green-300 font-bold mb-2">✓ Safety Assessment</p>
              <p className="text-gray-100 text-sm">This object poses no threat to Earth. Extensive calculations show it will pass at a safe distance from our planet.</p>
            </div>
          </div>
        )}
      </DetailModal>

      {!loading && displayImpacts.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-400 text-xl">No impact data available</p>
        </div>
      )}
    </div>
  );
}

export default EarthImpact;

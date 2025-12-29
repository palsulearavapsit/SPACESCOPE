import React, { useEffect, useState } from 'react';
import { missionsAPI } from '../services/api';
import { FaRocket, FaCalendarAlt, FaBuilding, FaCheckCircle } from 'react-icons/fa';
import DetailModal from '../components/DetailModal';

function Missions() {
  const [missions, setMissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMission, setSelectedMission] = useState(null);

  useEffect(() => {
    loadMissions();
  }, []);

  const loadMissions = async () => {
    try {
      setLoading(true);
      const response = await missionsAPI.getAll();
      setMissions(response.data || []);
      setError(null);
    } catch (err) {
      console.error('Error loading missions:', err);
      setError('Failed to load missions');
      setMissions([]);
    } finally {
      setLoading(false);
    }
  };

  const mockMissions = [
    {
      id: 1,
      name: 'Artemis II',
      status: 'Active',
      description: 'Next crewed lunar mission - returning humans to the Moon',
      launch_date: '2025-09-23',
      organization: 'NASA',
      progress: 75,
      crew: 4,
      destination: 'Moon Orbit',
      fullDescription: 'Artemis II is a crewed lunar mission that will carry astronauts to lunar orbit. This mission is crucial for testing systems and procedures needed for future crewed lunar landing missions. The mission will carry a crew of four astronauts and will orbit the Moon for several days before returning to Earth.',
      objectives: [
        'Test crewed Orion spacecraft systems',
        'Demonstrate lunar orbit insertion',
        'Validate Earth reentry procedures',
        'Train crew for future Artemis missions'
      ],
      crew_members: ['Reid Wiseman', 'Victor Glover', 'Christina Koch', 'Jeremy Hansen'],
      budget: '$4.7 billion',
      duration: '10 days'
    },
    {
      id: 2,
      name: 'James Webb Space Telescope',
      status: 'Active',
      description: 'Observing the universe in infrared, studying the first galaxies',
      launch_date: '2021-12-25',
      organization: 'NASA/ESA/CSA',
      progress: 100,
      crew: 0,
      destination: 'L2 Orbit',
      fullDescription: 'The James Webb Space Telescope is the most powerful space telescope ever built. It observes the universe primarily in infrared wavelengths and can see objects 13.6 billion light-years away. The telescope helps us understand the origin of the universe and search for signs of habitability on exoplanets.',
      objectives: [
        'Observe the first galaxies',
        'Study star and galaxy formation',
        'Observe the birth of stars',
        'Study planetary systems and the origins of life'
      ],
      cost: '$10 billion',
      mirror_diameter: '6.5 meters',
      operating_since: '2021'
    }
  ];

  const displayMissions = missions.length > 0 ? missions : mockMissions;

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'active':
        return 'from-green-500/20 to-emerald-500/10 border-green-500/40';
      case 'upcoming':
        return 'from-blue-500/20 to-cyan-500/10 border-blue-500/40';
      case 'completed':
        return 'from-gray-500/20 to-slate-500/10 border-gray-500/40';
      default:
        return 'from-indigo-500/20 to-purple-500/10 border-indigo-500/40';
    }
  };

  const getStatusBadge = (status) => {
    switch (status?.toLowerCase()) {
      case 'active':
        return 'bg-green-500/30 text-green-300 border border-green-500/50';
      case 'upcoming':
        return 'bg-blue-500/30 text-blue-300 border border-blue-500/50';
      case 'completed':
        return 'bg-gray-500/30 text-gray-300 border border-gray-500/50';
      default:
        return 'bg-indigo-500/30 text-indigo-300 border border-indigo-500/50';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold neon mb-2 flex items-center justify-center gap-3">
          <FaRocket className="text-orange-400" />
          Space Missions
        </h1>
        <p className="text-gray-300 text-lg glow-text">Current and upcoming space exploration missions worldwide</p>
        <div className="mt-4 h-1 w-32 mx-auto bg-gradient-to-r from-orange-500 via-yellow-500 to-orange-500 rounded-full"></div>
      </div>

      {/* Mission Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">{displayMissions.filter(m => m.status?.toLowerCase() === 'active').length}</p>
          <p className="text-gray-300 text-sm mt-1">Active</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">{displayMissions.filter(m => m.status?.toLowerCase() === 'upcoming').length}</p>
          <p className="text-gray-300 text-sm mt-1">Upcoming</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">{displayMissions.length}</p>
          <p className="text-gray-300 text-sm mt-1">Total</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">🌍</p>
          <p className="text-gray-300 text-sm mt-1">Worldwide</p>
        </div>
      </div>

      {loading && <div className="text-center text-cyan-400 py-8 text-lg">🔄 Loading missions...</div>}
      {error && <div className="text-center text-red-400 py-8 text-lg">⚠️ {error}</div>}

      {/* Missions Grid */}
      <div className="space-y-6">
        {displayMissions.map((mission, idx) => (
          <div
            key={idx}
            className={`glass-card space-card glow-border border bg-gradient-to-r ${getStatusColor(mission.status)} p-6`}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4 pb-4 border-b border-white/10">
              <div className="flex-1">
                <h3 className="text-3xl font-bold neon mb-2">{mission.name}</h3>
                <p className="text-gray-300 leading-relaxed">{mission.description}</p>
              </div>
              <span className={`px-4 py-2 rounded-full text-sm font-bold whitespace-nowrap ml-4 ${getStatusBadge(mission.status)}`}>
                {mission.status}
              </span>
            </div>

            {/* Details Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              {mission.launch_date && (
                <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                  <p className="text-white/60 text-xs font-semibold mb-2 flex items-center gap-1">
                    <FaCalendarAlt className="text-cyan-400" /> LAUNCH DATE
                  </p>
                  <p className="text-white font-mono text-sm">{mission.launch_date}</p>
                </div>
              )}
              {mission.organization && (
                <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                  <p className="text-white/60 text-xs font-semibold mb-2 flex items-center gap-1">
                    <FaBuilding className="text-cyan-400" /> ORGANIZATION
                  </p>
                  <p className="text-white font-mono text-sm">{mission.organization}</p>
                </div>
              )}
              {mission.destination && (
                <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                  <p className="text-white/60 text-xs font-semibold mb-2 flex items-center gap-1">
                    🎯 DESTINATION
                  </p>
                  <p className="text-white font-mono text-sm">{mission.destination}</p>
                </div>
              )}
            </div>

            {/* Progress Bar */}
            {mission.progress && (
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-cyan-300 text-sm font-semibold">Mission Progress</p>
                  <span className="text-cyan-300 font-bold text-sm">{mission.progress}%</span>
                </div>
                <div className="w-full bg-black/30 rounded-full h-2 border border-cyan-500/30 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full transition-all duration-500"
                    style={{ width: `${mission.progress}%` }}
                  ></div>
                </div>
              </div>
            )}

            {/* Action Button */}
            <button 
              onClick={() => setSelectedMission(mission)}
              className="w-full neon-btn"
            >
              <FaCheckCircle className="inline mr-2" /> Learn More
            </button>
          </div>
        ))}
      </div>

      {/* Detail Modal */}
      <DetailModal
        isOpen={!!selectedMission}
        title={selectedMission?.name}
        onClose={() => setSelectedMission(null)}
      >
        {selectedMission && (
          <div className="space-y-4">
            <p className="text-gray-100 leading-relaxed">{selectedMission.fullDescription}</p>

            <div className="bg-indigo-900/30 border border-indigo-500/30 rounded-lg p-4">
              <h3 className="text-cyan-300 font-bold mb-3">📋 Key Information</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-gray-400">Status</p>
                  <p className="text-white font-semibold">{selectedMission.status}</p>
                </div>
                <div>
                  <p className="text-gray-400">Organization</p>
                  <p className="text-white font-semibold">{selectedMission.organization}</p>
                </div>
                <div>
                  <p className="text-gray-400">Destination</p>
                  <p className="text-white font-semibold">{selectedMission.destination}</p>
                </div>
                <div>
                  <p className="text-gray-400">Launch Date</p>
                  <p className="text-white font-semibold">{selectedMission.launch_date}</p>
                </div>
                {selectedMission.budget && (
                  <div>
                    <p className="text-gray-400">Budget</p>
                    <p className="text-white font-semibold">{selectedMission.budget}</p>
                  </div>
                )}
                {selectedMission.duration && (
                  <div>
                    <p className="text-gray-400">Duration</p>
                    <p className="text-white font-semibold">{selectedMission.duration}</p>
                  </div>
                )}
              </div>
            </div>

            {selectedMission.objectives && (
              <div className="bg-purple-900/30 border border-purple-500/30 rounded-lg p-4">
                <h3 className="text-purple-300 font-bold mb-3">🎯 Mission Objectives</h3>
                <ul className="space-y-2">
                  {selectedMission.objectives.map((obj, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm">
                      <span className="text-purple-400 mt-1">✓</span>
                      <span className="text-gray-100">{obj}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {selectedMission.crew_members && (
              <div className="bg-cyan-900/30 border border-cyan-500/30 rounded-lg p-4">
                <h3 className="text-cyan-300 font-bold mb-3">👨‍🚀 Crew Members</h3>
                <div className="grid grid-cols-2 gap-2">
                  {selectedMission.crew_members.map((member, idx) => (
                    <div key={idx} className="text-sm text-gray-100 bg-black/20 p-2 rounded">
                      {member}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </DetailModal>

      {!loading && displayMissions.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-400 text-xl">No missions found</p>
        </div>
      )}
    </div>
  );
}

export default Missions;

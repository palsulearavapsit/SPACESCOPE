import React, { useEffect, useState } from 'react';
import { skyEventsAPI } from '../services/api';
import { FaCalendarAlt, FaClock, FaLocationArrow, FaEye } from 'react-icons/fa';
import DetailModal from '../components/DetailModal';

function EventCalendar() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    try {
      setLoading(true);
      const response = await skyEventsAPI.getUpcoming(30);
      setEvents(response.data || []);
      setError(null);
    } catch (err) {
      console.error('Error loading events:', err);
      setError('Failed to load events');
      setEvents([]);
    } finally {
      setLoading(false);
    }
  };

  const mockEvents = [
    {
      id: 1,
      name: 'Quadrantids Meteor Shower',
      event_type: 'Meteor Shower',
      description: 'Peak activity with up to 40 meteors per hour',
      start_time: '2025-01-03',
      end_time: '2025-01-04',
      best_time: '2:00 AM - 5:00 AM',
      visibility: 'Best from Northern Hemisphere',
      moon_phase: 'Waning Crescent',
      full_description: 'The Quadrantids is an annual meteor shower caused by the Earth passing through the debris field left by an extinct comet. This is one of the most reliable meteor showers each year, with consistent activity and bright, fast meteors.',
      tips: [
        'Find a dark location away from city lights',
        'Look towards the northeast sky',
        'Allow 20-30 minutes for eyes to adjust to darkness',
        'No telescope needed - use naked eyes only',
        'Peak activity lasts only 6-12 hours'
      ],
      parent_body: 'EH1 (extinct comet)',
      zenithal_hourly_rate: '40 meteors/hour'
    },
    {
      id: 2,
      name: 'Venus at Greatest Elongation',
      event_type: 'Planetary Event',
      description: 'Venus reaches maximum angular distance from the Sun',
      start_time: '2025-01-10',
      best_time: 'Evening',
      visibility: 'Visible from entire Earth',
      moon_phase: 'Waning Gibbous',
      full_description: 'Greatest elongation is when Venus reaches its maximum angular separation from the Sun as seen from Earth. During this time, Venus will be most prominent and easiest to observe in the evening sky.',
      tips: [
        'Look just after sunset in the western sky',
        'Venus will be the brightest object in the evening sky',
        'Best viewed 30-60 minutes after sunset',
        'Binoculars will show Venus phases',
        'Visible for about 3 hours after sunset'
      ],
      magnitude: '-4.9 (extremely bright)',
      angular_distance: '47.1° from Sun'
    }
  ];

  const displayEvents = events.length > 0 ? events : mockEvents;

  const getEventColor = (type) => {
    switch (type?.toLowerCase()) {
      case 'meteor shower':
        return 'from-orange-500/20 to-red-500/10';
      case 'planetary event':
        return 'from-cyan-500/20 to-blue-500/10';
      case 'eclipse':
        return 'from-purple-500/20 to-indigo-500/10';
      default:
        return 'from-indigo-500/20 to-blue-500/10';
    }
  };

  const getEventBorder = (type) => {
    switch (type?.toLowerCase()) {
      case 'meteor shower':
        return 'border-orange-500/40';
      case 'planetary event':
        return 'border-cyan-500/40';
      case 'eclipse':
        return 'border-purple-500/40';
      default:
        return 'border-indigo-500/40';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold neon mb-2 flex items-center justify-center gap-3">
          <FaCalendarAlt className="text-cyan-400" />
          Event Calendar
        </h1>
        <p className="text-gray-300 text-lg glow-text">Upcoming astronomical events in the next 30 days</p>
        <div className="mt-4 h-1 w-32 mx-auto bg-gradient-to-r from-orange-500 via-cyan-500 to-purple-500 rounded-full"></div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-3 justify-center flex-wrap">
        {['all', 'meteor shower', 'planetary event', 'eclipse'].map((type) => (
          <button
            key={type}
            onClick={() => setFilter(type)}
            className={`px-6 py-2 rounded-lg font-semibold transition neon-btn ${
              filter === type
                ? 'bg-indigo-600 border-cyan-400 text-cyan-300 neon'
                : 'hover:border-indigo-400'
            }`}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto">
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">{displayEvents.length}</p>
          <p className="text-gray-300 text-sm mt-1">Events</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">30</p>
          <p className="text-gray-300 text-sm mt-1">Days</p>
        </div>
        <div className="glass-card space-card glow-border text-center p-4">
          <p className="text-cyan-400 text-2xl font-bold">🌙</p>
          <p className="text-gray-300 text-sm mt-1">Night</p>
        </div>
      </div>

      {loading && <div className="text-center text-cyan-400 py-8 text-lg">🔄 Loading cosmic events...</div>}
      {error && <div className="text-center text-red-400 py-8 text-lg">⚠️ {error}</div>}

      {/* Events Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {displayEvents.map((event, idx) => (
          <div
            key={idx}
            className={`glass-card space-card glow-border border bg-gradient-to-br ${getEventColor(event.event_type)} ${getEventBorder(event.event_type)}`}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-2xl font-bold neon mb-1">{event.name}</h3>
                <div className="flex items-center gap-2">
                  <FaEye className="text-cyan-400 text-sm" />
                  <span className="text-cyan-300 text-sm font-semibold">{event.event_type}</span>
                </div>
              </div>
              <div className="text-3xl">🌠</div>
            </div>

            {/* Description */}
            <p className="text-gray-200 text-sm leading-relaxed mb-4">{event.description}</p>

            {/* Details Grid */}
            <div className="grid grid-cols-2 gap-3 mb-4">
              {event.start_time && (
                <div className="bg-indigo-900/40 rounded-lg p-3 border border-indigo-500/20">
                  <p className="text-indigo-300 text-xs font-semibold mb-1 flex items-center gap-1">
                    <FaCalendarAlt className="text-xs" /> DATE
                  </p>
                  <p className="text-white font-mono text-sm">{event.start_time}</p>
                </div>
              )}
              {event.best_time && (
                <div className="bg-cyan-900/40 rounded-lg p-3 border border-cyan-500/20">
                  <p className="text-cyan-300 text-xs font-semibold mb-1 flex items-center gap-1">
                    <FaClock className="text-xs" /> BEST TIME
                  </p>
                  <p className="text-white font-mono text-sm">{event.best_time}</p>
                </div>
              )}
              {event.visibility && (
                <div className="bg-purple-900/40 rounded-lg p-3 border border-purple-500/20 col-span-2">
                  <p className="text-purple-300 text-xs font-semibold mb-1 flex items-center gap-1">
                    <FaLocationArrow className="text-xs" /> VISIBILITY
                  </p>
                  <p className="text-white text-sm">{event.visibility}</p>
                </div>
              )}
              {event.moon_phase && (
                <div className="bg-yellow-900/40 rounded-lg p-3 border border-yellow-500/20 col-span-2">
                  <p className="text-yellow-300 text-xs font-semibold mb-1">🌙 MOON PHASE</p>
                  <p className="text-white text-sm">{event.moon_phase}</p>
                </div>
              )}
            </div>

            {/* Action Button */}
            <button 
              onClick={() => setSelectedEvent(event)}
              className="w-full neon-btn mt-2"
            >
              Set Reminder 🔔
            </button>
          </div>
        ))}
      </div>

      {/* Detail Modal */}
      <DetailModal
        isOpen={!!selectedEvent}
        title={selectedEvent?.name}
        onClose={() => setSelectedEvent(null)}
      >
        {selectedEvent && (
          <div className="space-y-4">
            <p className="text-gray-100 leading-relaxed">{selectedEvent.full_description}</p>

            <div className="bg-indigo-900/30 border border-indigo-500/30 rounded-lg p-4">
              <h3 className="text-cyan-300 font-bold mb-3">📅 Event Details</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-gray-400">Start Date</p>
                  <p className="text-white font-semibold">{selectedEvent.start_time}</p>
                </div>
                {selectedEvent.end_time && (
                  <div>
                    <p className="text-gray-400">End Date</p>
                    <p className="text-white font-semibold">{selectedEvent.end_time}</p>
                  </div>
                )}
                {selectedEvent.best_time && (
                  <div>
                    <p className="text-gray-400">Best Time</p>
                    <p className="text-white font-semibold">{selectedEvent.best_time}</p>
                  </div>
                )}
                <div>
                  <p className="text-gray-400">Moon Phase</p>
                  <p className="text-white font-semibold">{selectedEvent.moon_phase}</p>
                </div>
              </div>
            </div>

            {selectedEvent.visibility && (
              <div className="bg-purple-900/30 border border-purple-500/30 rounded-lg p-4">
                <h3 className="text-purple-300 font-bold mb-2">🌍 Visibility</h3>
                <p className="text-gray-100 text-sm">{selectedEvent.visibility}</p>
              </div>
            )}

            {selectedEvent.tips && (
              <div className="bg-orange-900/30 border border-orange-500/30 rounded-lg p-4">
                <h3 className="text-orange-300 font-bold mb-3">💡 Viewing Tips</h3>
                <ul className="space-y-2">
                  {selectedEvent.tips.map((tip, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm">
                      <span className="text-orange-400 mt-1">→</span>
                      <span className="text-gray-100">{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {selectedEvent.parent_body && (
              <div className="bg-green-900/30 border border-green-500/30 rounded-lg p-4">
                <h3 className="text-green-300 font-bold mb-2">🪨 Source</h3>
                <p className="text-gray-100 text-sm">{selectedEvent.parent_body}</p>
              </div>
            )}

            <button
              onClick={() => {
                alert(`✓ Reminder set for ${selectedEvent.name}!`);
                setSelectedEvent(null);
              }}
              className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-3 rounded-lg font-semibold transition mt-4"
            >
              ✓ Confirm Reminder
            </button>
          </div>
        )}
      </DetailModal>

      {!loading && displayEvents.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-400 text-xl">No events found</p>
        </div>
      )}
    </div>
  );
}

export default EventCalendar;

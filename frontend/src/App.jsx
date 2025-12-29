import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import CosmicBackground from './components/CosmicBackground';
import Dashboard from './pages/Dashboard';
import EventCalendar from './pages/EventCalendar';
import SpaceWeather from './pages/SpaceWeather';
import Missions from './pages/Missions';
import LearningZone from './pages/LearningZone';
import Chat from './pages/Chat';
import EarthImpact from './pages/EarthImpact';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-black relative overflow-hidden">
        <CosmicBackground />
        <div className="app-content min-h-screen bg-transparent">
          <Navigation />
          <main className="max-w-7xl mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/calendar" element={<EventCalendar />} />
              <Route path="/weather" element={<SpaceWeather />} />
              <Route path="/missions" element={<Missions />} />
              <Route path="/learning" element={<LearningZone />} />
              <Route path="/chat" element={<Chat />} />
              <Route path="/earth-impact" element={<EarthImpact />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;

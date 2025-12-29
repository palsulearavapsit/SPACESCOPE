import React from "react";
import { Link } from "react-router-dom";
import {
  FaRocket,
  FaCalendar,
  FaCloud,
  FaBook,
  FaComments,
  FaGlobe
} from "react-icons/fa";

function Navigation() {
  return (
    <nav className="sticky top-0 z-50 glass-card bg-transparent border-b border-indigo-500/10">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 text-2xl font-bold neon">
            <FaRocket className="text-amber-300 animate-bounce" />
            SpaceScope
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-6 text-slate-200">
            <Link to="/" className="hover:text-indigo-400 transition">
              Dashboard
            </Link>

            <Link to="/calendar" className="flex items-center gap-1 hover:text-indigo-400 transition">
              <FaCalendar /> Events
            </Link>

            <Link to="/weather" className="flex items-center gap-1 hover:text-indigo-400 transition">
              <FaCloud /> Weather
            </Link>

            <Link to="/missions" className="flex items-center gap-1 hover:text-indigo-400 transition">
              <FaRocket /> Missions
            </Link>

            <Link to="/earth-impact" className="flex items-center gap-1 hover:text-indigo-400 transition">
              <FaGlobe /> Earth
            </Link>

            <Link to="/learning" className="flex items-center gap-1 hover:text-indigo-400 transition">
              <FaBook /> Learn
            </Link>

            <Link
              to="/chat"
              className="flex items-center gap-1 bg-indigo-600 px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
            >
              <FaComments /> Chat
            </Link>
          </div>

        </div>
      </div>
    </nav>
  );
}

export default Navigation;

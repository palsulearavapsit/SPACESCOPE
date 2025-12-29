import React from 'react';
import { FaTimes } from 'react-icons/fa';

export default function DetailModal({ isOpen, title, children, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="relative bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl border border-cyan-500/30 p-8 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto shadow-2xl shadow-indigo-500/20">
        {/* Header */}
        <div className="flex items-center justify-between mb-6 pb-6 border-b border-white/10">
          <h2 className="text-3xl font-bold neon">{title}</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-cyan-400 transition text-2xl"
          >
            <FaTimes />
          </button>
        </div>

        {/* Content */}
        <div className="text-gray-200 space-y-4">
          {children}
        </div>

        {/* Close Button */}
        <div className="mt-8 pt-6 border-t border-white/10">
          <button
            onClick={onClose}
            className="w-full neon-btn"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

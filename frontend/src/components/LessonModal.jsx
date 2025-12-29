import React from 'react';
import { FaTimes, FaBook } from 'react-icons/fa';

function LessonModal({ isOpen, lesson, onClose }) {
  if (!isOpen || !lesson) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border border-purple-500/30 rounded-2xl shadow-2xl max-w-2xl w-full mx-4 mb-0 md:mb-auto max-h-[80vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-indigo-900/60 to-purple-900/60 border-b border-purple-500/30 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <FaBook className="text-purple-400 text-xl" />
            <h2 className="text-2xl font-bold neon">{lesson.name}</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition text-xl"
          >
            <FaTimes />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          {/* Duration */}
          <div className="flex items-center gap-2">
            <span className="text-cyan-400 font-semibold">⏱️ Duration:</span>
            <span className="text-gray-300">{lesson.duration}</span>
          </div>

          {/* Lesson Content */}
          <div className="bg-indigo-900/20 border border-indigo-500/30 rounded-lg p-4">
            <h3 className="text-cyan-300 font-bold mb-3">📖 Lesson Content</h3>
            <p className="text-gray-100 leading-relaxed text-base">
              {lesson.content}
            </p>
          </div>

          {/* Key Takeaways */}
          <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-4">
            <h3 className="text-purple-300 font-bold mb-3">💡 Key Takeaways</h3>
            <ul className="space-y-2">
              <li className="flex items-start gap-2">
                <span className="text-purple-400 mt-1">✓</span>
                <span className="text-gray-100">Comprehensive understanding of the topic</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-purple-400 mt-1">✓</span>
                <span className="text-gray-100">Practical applications and real-world examples</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-purple-400 mt-1">✓</span>
                <span className="text-gray-100">Foundation for advanced concepts</span>
              </li>
            </ul>
          </div>

          {/* Close Button */}
          <button
            onClick={onClose}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-4 py-3 rounded-lg font-semibold transition mt-4"
          >
            Close Lesson
          </button>
        </div>
      </div>
    </div>
  );
}

export default LessonModal;

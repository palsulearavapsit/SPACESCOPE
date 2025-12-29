import React, { useState, useRef, useEffect } from 'react';
import { chatAPI } from '../services/api';
import { FaComments, FaPaperPlane, FaSpinner } from 'react-icons/fa';

function Chat() {
  const [messages, setMessages] = useState([
    { 
      role: 'assistant', 
      content: '🌌 Welcome to SpaceScope AI! I\'m your cosmic expert assistant. Ask me about space events, missions, celestial objects, astronomy, or anything cosmic!'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const suggestedQuestions = [
    '🌠 What meteor showers are happening this month?',
    '🚀 Tell me about current space missions',
    '⭐ How far away is the nearest star?',
    '🌍 What are near-Earth asteroids?',
    '🔭 How do telescopes work?'
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setMessages([...messages, { role: 'user', content: userMessage }]);
    setIsLoading(true);
    setInput('');

    try {
      const response = await chatAPI.send(userMessage, 'general');
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.data.ai_response }
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '🚀 Sorry, I encountered an error. Please try again.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestedQuestion = (question) => {
    setInput(question);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center py-6">
        <h1 className="text-4xl font-bold neon mb-2 flex items-center justify-center gap-2">
          <FaComments className="text-cyan-400" />
          SpaceScope AI
        </h1>
        <p className="text-gray-300">Chat with your cosmic knowledge assistant</p>
      </div>

      {/* Chat Container */}
      <div className="flex flex-col h-[600px] glass-card space-card glow-border">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md xl:max-w-lg px-6 py-4 rounded-lg ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-br from-indigo-600 to-purple-600 text-white rounded-tr-none border border-indigo-400/50 shadow-lg shadow-indigo-500/30'
                    : 'bg-gradient-to-br from-slate-700 to-slate-800 text-gray-100 rounded-tl-none border border-cyan-500/20'
                }`}
              >
                <p className="text-sm leading-relaxed">{msg.content}</p>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="px-6 py-4 rounded-lg bg-slate-700 text-gray-100 flex items-center gap-2">
                <FaSpinner className="animate-spin text-cyan-400" />
                <span>Thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Questions (shown when few messages) */}
        {messages.length <= 1 && !isLoading && (
          <div className="px-6 py-4 border-t border-white/10">
            <p className="text-gray-400 text-sm mb-3 font-semibold">Try asking:</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {suggestedQuestions.slice(0, 4).map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSuggestedQuestion(q)}
                  className="text-left px-3 py-2 text-xs bg-indigo-900/30 hover:bg-indigo-900/50 text-cyan-300 rounded-lg border border-indigo-500/30 transition neon-btn"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="border-t border-white/10 p-4 flex gap-2">
          <div className="flex-1 relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSend()}
              placeholder="Ask me about space..."
              className="w-full bg-slate-700/50 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 border border-indigo-500/20 placeholder-gray-500 transition"
              disabled={isLoading}
            />
          </div>
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg transition font-semibold flex items-center gap-2 neon-btn"
          >
            {isLoading ? <FaSpinner className="animate-spin" /> : <FaPaperPlane />}
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>

      {/* Info Box */}
      <div className="glass-card space-card glow-border p-4 text-sm text-gray-300 border border-cyan-500/20">
        <p className="font-semibold text-cyan-300 mb-2">💡 Tips:</p>
        <ul className="list-disc list-inside space-y-1 text-xs">
          <li>Ask about upcoming celestial events and meteor showers</li>
          <li>Get information about space missions and NASA</li>
          <li>Learn about planets, stars, galaxies, and more</li>
          <li>Discover facts about the universe and astronomy</li>
        </ul>
      </div>
    </div>
  );
}

export default Chat;

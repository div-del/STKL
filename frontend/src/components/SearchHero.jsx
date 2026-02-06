import React, { useState } from 'react';
import { motion } from 'framer-motion';

const SearchHero = ({ onSearch }) => {
  const [name, setName] = useState('');
  const [extraInfo, setExtraInfo] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      onSearch(name, extraInfo);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-green-500 font-mono p-4">
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl md:text-6xl font-bold mb-4 tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500">
          DIGITAL FOOTPRINT
        </h1>
        <p className="text-sm md:text-lg opacity-80 typing-effect">
          Initialize search protocol...
        </p>
      </motion.div>

      <motion.form
        onSubmit={handleSubmit}
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="w-full max-w-lg space-y-4 relative z-10"
      >
        <div className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-green-500 to-blue-600 rounded-lg blur opacity-75 group-hover:opacity-100 transition duration-1000 group-hover:duration-200" />
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="ENTER TARGET IDENTIFIER (NAME)"
            className="relative w-full bg-gray-900 text-green-400 border border-gray-800 rounded-lg p-4 focus:outline-none focus:ring-2 focus:ring-green-500 placeholder-green-800 tracking-widest"
          />
        </div>

        <div className="relative group">
             <div className="absolute -inset-0.5 bg-gradient-to-r from-green-500 to-blue-600 rounded-lg blur opacity-75 group-hover:opacity-100 transition duration-1000 group-hover:duration-200" />
          <input
            type="text"
            value={extraInfo}
            onChange={(e) => setExtraInfo(e.target.value)}
            placeholder="ADDITIONAL PARAMETERS (School, Locality...)"
            className="relative w-full bg-gray-900 text-green-400 border border-gray-800 rounded-lg p-4 focus:outline-none focus:ring-2 focus:ring-green-500 placeholder-green-800 tracking-widest"
          />
        </div>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="w-full bg-green-600 hover:bg-green-500 text-black font-bold py-3 px-6 rounded-lg shadow-lg shadow-green-500/50 transition-all uppercase tracking-widest"
          type="submit"
        >
          Initiate Scan
        </motion.button>
      </motion.form>

      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
          <div className="absolute w-96 h-96 bg-green-500/10 rounded-full blur-3xl -top-20 -left-20 animate-pulse"></div>
          <div className="absolute w-96 h-96 bg-blue-500/10 rounded-full blur-3xl bottom-0 right-0 animate-pulse delay-1000"></div>
      </div>
    </div>
  );
};

export default SearchHero;

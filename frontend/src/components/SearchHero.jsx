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
    <div className="w-full max-w-4xl mx-auto flex flex-col items-center justify-center p-4">
      {/* Background Overlay */}
      <div className="absolute inset-0 -z-10" />

      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center mb-12 p-8 rounded-2xl backdrop-blur-sm bg-white/5 border border-white/10 shadow-2xl"
      >
        <h1 className="text-5xl md:text-8xl font-bold mb-6 tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 drop-shadow-[0_0_15px_rgba(59,130,246,0.8)] font-['Orbitron']">
          DIGITAL FOOTPRINT
        </h1>
        <p className="text-xl md:text-2xl text-blue-200 opacity-90 typing-effect font-medium tracking-widest drop-shadow-[0_0_5px_rgba(59,130,246,0.5)]">
          Initialize scan protocol...
        </p>
      </motion.div>

      <motion.form
        onSubmit={handleSubmit}
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="w-full max-w-xl flex flex-col gap-8 relative z-10"
      >
        <div className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-lg blur opacity-75 group-hover:opacity-100 transition duration-500 animate-pulse" />
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="ENTER TARGET IDENTIFIER (NAME)"
            className="relative w-full bg-black/80 backdrop-blur-xl text-cyan-50 border border-cyan-500/50 rounded-lg p-6 text-3xl focus:outline-none focus:ring-2 focus:ring-cyan-400 placeholder-cyan-700 tracking-widest shadow-[0_0_15px_rgba(6,182,212,0.3)] font-['Caveat'] font-bold uppercase transition-all"
          />
        </div>

        <div className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg blur opacity-75 group-hover:opacity-100 transition duration-500 animate-pulse" />
          <input
            type="text"
            value={extraInfo}
            onChange={(e) => setExtraInfo(e.target.value)}
            placeholder="ADDITIONAL PARAMETERS (School, Locality...)"
            className="relative w-full bg-black/80 backdrop-blur-xl text-purple-50 border border-purple-500/50 rounded-lg p-6 text-3xl focus:outline-none focus:ring-2 focus:ring-purple-400 placeholder-purple-700 tracking-widest shadow-[0_0_15px_rgba(168,85,247,0.3)] font-['Caveat'] font-bold uppercase transition-all"
          />
        </div>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="w-full bg-gradient-to-r from-cyan-600 via-blue-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 text-white font-black text-xl py-6 px-8 rounded-lg shadow-[0_0_30px_rgba(6,182,212,0.6)] transition-all uppercase tracking-[0.2em] border border-white/20 font-['Orbitron']"
          type="submit"
        >
          Initiate Scan
        </motion.button>
      </motion.form>
    </div>
  );
};

export default SearchHero;

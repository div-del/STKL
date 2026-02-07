import React from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, Share2, Globe, FileText, Image as ImageIcon } from 'lucide-react';

const ResultsDashboard = ({ results, onReset }) => {
    // Check if results is an array (legacy) or object (new categorized)
    const isCategorized = !Array.isArray(results);

    // Helper to render a grid of cards
    const ResultGrid = ({ items, delayOffset = 0 }) => (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-8 w-full place-items-center">
            {items.map((result, index) => (
                <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: delayOffset + index * 0.1 }}
                    className="bg-black/40 border border-blue-500/30 rounded-xl p-6 hover:bg-black/60 hover:border-blue-400 transition-all group backdrop-blur-md shadow-lg"
                >
                    <div className="flex items-start justify-between mb-4">
                        <div className="p-2 bg-blue-500/20 rounded-lg group-hover:bg-blue-400/30 transition-colors">
                            <Globe size={24} className="text-blue-300 group-hover:text-white" />
                        </div>
                        <a href={result.url} target="_blank" rel="noopener noreferrer">
                            <ExternalLink size={18} className="text-gray-400 hover:text-white transition-colors" />
                        </a>
                    </div>

                    <a href={result.url} target="_blank" rel="noopener noreferrer" className="block hover:opacity-80 transition-opacity">
                        <h3 className="text-3xl md:text-4xl font-bold text-white mb-3 leading-tight drop-shadow-md font-['Caveat'] decoration-cyan-400/50 underline-offset-4">
                            {result.title}
                        </h3>
                    </a>

                    {result.match_context && (
                        <div className="mb-4 inline-block px-3 py-1 bg-cyan-500/20 text-cyan-200 text-sm font-bold rounded border border-cyan-400/30 uppercase tracking-wider font-['Rajdhani']">
                            🔍 {result.match_context}
                        </div>
                    )}

                    <p className="text-lg text-gray-200 mb-4 line-clamp-3 font-['Caveat'] tracking-wide">
                        {result.description}
                    </p>

                    <div className="flex items-center text-xs text-gray-400 font-semibold bg-black/30 p-2 rounded hover:bg-black/50 transition-colors">
                        <a href={result.url} target="_blank" rel="noopener noreferrer" className="truncate w-full hover:text-blue-300 underline decoration-blue-500/30">
                            {result.url}
                        </a>
                    </div>
                </motion.div>
            ))}
        </div>
    );

    return (
        <div className="min-h-screen font-mono p-4 md:p-8 relative z-0 flex flex-col items-center w-full max-w-7xl mx-auto">
            {/* Background Overlay */}
            <div className="absolute inset-0 bg-black/40 -z-10" />

            <motion.button
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                onClick={onReset}
                className="mb-8 text-sm text-blue-300 hover:text-white underline tracking-widest uppercase"
            >
                &larr; New Search
            </motion.button>

            <motion.h2
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                className="text-3xl font-bold mb-8 border-b border-blue-500/50 pb-2 text-white drop-shadow-[0_0_10px_rgba(59,130,246,0.6)]"
            >
                SCAN RESULTS
            </motion.h2>

            {isCategorized ? (
                <>
                    {Object.entries(results).map(([category, items], idx) => (
                        items.length > 0 && (
                            <div key={category} className="mb-12">
                                <h3 className="text-xl font-bold text-blue-100 mb-6 uppercase tracking-widest pl-4 border-l-4 border-blue-500 flex items-center">
                                    {category}
                                    <span className="text-xs bg-blue-600/30 text-blue-200 px-2 py-1 rounded-full ml-3 border border-blue-500/30">
                                        {items.length}
                                    </span>
                                </h3>
                                <ResultGrid items={items} delayOffset={idx * 0.2} />
                            </div>
                        )
                    ))}
                </>
            ) : (
                <ResultGrid items={results} />
            )}

            {(!results || (isCategorized && Object.values(results).every(r => r.length === 0)) || (!isCategorized && results.length === 0)) && (
                <div className="flex-grow flex items-center justify-center w-full">
                    <div className="text-center text-gray-400 backdrop-blur-md p-12 rounded-2xl bg-black/40 border border-blue-500/30 shadow-[0_0_50px_rgba(59,130,246,0.2)] max-w-lg">
                        <p className="text-3xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-200 to-cyan-200 font-['Orbitron']">NO DATA FOUND</p>
                        <p className="text-lg opacity-80 font-['Rajdhani']">Target signature not located in public sector archives.</p>
                        <p className="text-sm opacity-50 mt-4">Try refining your search parameters.</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ResultsDashboard;

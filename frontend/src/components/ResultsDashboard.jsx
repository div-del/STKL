import React from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, Share2, Globe, FileText, Image as ImageIcon } from 'lucide-react';

const ResultsDashboard = ({ results, onReset }) => {
    // Check if results is an array (legacy) or object (new categorized)
    const isCategorized = !Array.isArray(results);

    // Helper to render a grid of cards
    const ResultGrid = ({ items, delayOffset = 0 }) => (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {items.map((result, index) => (
                <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: delayOffset + index * 0.1 }}
                    className="bg-gray-900/50 border border-green-900/50 rounded-lg p-6 hover:bg-gray-900 hover:border-green-500 transition-all group backdrop-blur-sm"
                >
                    <div className="flex items-start justify-between mb-4">
                        <div className="p-2 bg-green-900/20 rounded-lg group-hover:bg-green-500/20 transition-colors">
                            <Globe size={24} className="text-green-400 group-hover:text-green-300" />
                        </div>
                        <a href={result.url} target="_blank" rel="noopener noreferrer">
                            <ExternalLink size={18} className="text-gray-600 hover:text-green-400 transition-colors" />
                        </a>
                    </div>

                    <h3 className="text-xl font-bold text-gray-200 mb-2 line-clamp-2 leading-tight group-hover:text-green-400 transition-colors">
                        {result.title}
                    </h3>

                    {result.match_context && (
                        <div className="mb-3 inline-block px-2 py-1 bg-green-500/20 text-green-300 text-xs font-bold rounded border border-green-500/30">
                            🔍 {result.match_context}
                        </div>
                    )}

                    <p className="text-sm text-gray-400 mb-4 line-clamp-3">
                        {result.description}
                    </p>

                    <div className="flex items-center text-xs text-gray-500 font-semibold bg-black/30 p-2 rounded">
                        <span className="truncate w-full">{result.url}</span>
                    </div>
                </motion.div>
            ))}
        </div>
    );

    return (
        <div className="min-h-screen bg-black text-green-500 font-mono p-4 md:p-8">
            <motion.button
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                onClick={onReset}
                className="mb-8 text-sm text-green-400 hover:text-green-300 underline"
            >
                &larr; NEW SEARCH
            </motion.button>

            <motion.h2
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                className="text-3xl font-bold mb-8 border-b border-green-800 pb-2"
            >
                SCAN RESULTS
            </motion.h2>

            {isCategorized ? (
                <>
                    {Object.entries(results).map(([category, items], idx) => (
                        items.length > 0 && (
                            <div key={category}>
                                <h3 className="text-xl font-bold text-white mb-4 uppercase tracking-widest pl-2 border-l-4 border-green-500">
                                    {category} <span className="text-sm text-gray-500 ml-2">({items.length})</span>
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
                <div className="text-center mt-20 text-gray-600">
                    NO DATA FOUND IN PUBLIC SECTOR.
                </div>
            )}
        </div>
    );
};

export default ResultsDashboard;

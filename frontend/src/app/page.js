"use client"
import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, RadialLinearScale, PointElement, LineElement, Filler } from 'chart.js';
import { Doughnut, Radar } from 'react-chartjs-2';
import { FaMicrophone, FaStop, FaSpinner, FaSmile, FaFrown, FaMeh } from 'react-icons/fa';

// Register additional ChartJS components
ChartJS.register(
  ArcElement, Tooltip, Legend, 
  RadialLinearScale, PointElement, 
  LineElement, Filler, CategoryScale
); 

export default function SentimentAnalysis() {
  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [sentimentResult, setSentimentResult] = useState(null);
  const recognitionRef = useRef(null);

    // Initialize voice recognition
    useEffect(() => {
        if (typeof window !== 'undefined') {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setText(prev => prev + ' ' + transcript);
            };

            recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            setIsRecording(false);
            };

            recognitionRef.current = recognition;
        }
        }
    }, []);

    const toggleRecording = () => {
        if (!recognitionRef.current) return;
        
        if (isRecording) {
        recognitionRef.current.stop();
        setIsRecording(false);
        } else {
        recognitionRef.current.start();
        setIsRecording(true);
        }
    };

    // Analyze sentiment from backend
    const analyzeSentiment = async () => {
        if (!text.trim()) return;
        
        setIsAnalyzing(true);
        
        try {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });

        const data = await response.json();
        
        if (!data.success) {
            throw new Error('Analysis failed');
        }

        const sentimentValues = data.sentiment_scores 
        ? Object.values(data.sentiment_scores) 
        : [0];
        const maxScore = Math.max(...sentimentValues);
        
        setSentimentResult({
            emotions: data.emotions,
            overallSentiment: data.sentiment || 'neutral',
            sentimentScores: data.sentiment_scores || {
                positive: 0,
                negative: 0,
                neutral: 0
            },
            overallScore :  maxScore
        });
        } catch (error) {
        console.error('Error analyzing sentiment:', error);
        } finally {
        setIsAnalyzing(false);
        }
    };

    // Color mapping for emotions
    const emotionColors = {
        anger: '#FF6B6B',
        anticipation: '#FFD166',
        disgust: '#A05C7B',
        fear: '#4ECDC4',
        joy: '#06D6A0',
        sadness: '#118AB2',
        surprise: '#FF9F1C',
        trust: '#83C5BE',
        positive: '#2EC4B6',
        negative: '#EF476F',
        neutral: '#A78BFA'
    };

    // Filter and sort emotions by score (descending)
    const processedEmotions = sentimentResult?.emotions
        ? Object.entries(sentimentResult.emotions)
            .filter(([_, score]) => score > 0)
            .sort((a, b) => b[1] - a[1])
        : [];

    // Chart data configuration
    const chartData = {
        labels: processedEmotions.map(([emotion]) => emotion),
        datasets: [{
        data: processedEmotions.map(([_, score]) => score),
        backgroundColor: processedEmotions.map(([emotion]) => emotionColors[emotion]),
        borderColor: '#ffffff',
        borderWidth: 2,
        }]
    };

    // Doughnut chart options
    const doughnutOptions = {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
        legend: {
            position: 'right',
            labels: {
            color: '#4B5563',
            font: {
                size: 12,
                family: 'Inter'
            },
            padding: 16,
            usePointStyle: true,
            pointStyle: 'circle'
            }
        },
        tooltip: {
            callbacks: {
            label: (context) => {
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const value = context.raw || 0;
                const percentage = Math.round((value / total) * 100);
                return `${context.label}: ${value} (${percentage}%)`;
            }
            }
        }
        }
    };

    // Radar chart options
    const radarOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
        r: {
            angleLines: {
            display: true,
            color: 'rgba(203, 213, 225, 0.3)'
            },
            suggestedMin: 0,
            suggestedMax: Math.max(...(processedEmotions.map(([_, score]) => score)) || 10) + 2,
            ticks: {
            stepSize: 2,
            backdropColor: 'transparent'
            },
            pointLabels: {
            font: {
                size: 12,
                family: 'Inter'
            },
            color: '#4B5563'
            }
        }
        },
        elements: {
        line: {
            tension: 0.1,
            borderWidth: 3
        },
        point: {
            radius: 4,
            hoverRadius: 6
        }
        },
        plugins: {
        legend: {
            display: false
        },
        tooltip: {
            callbacks: {
            label: (context) => `${context.label}: ${context.raw}`
            }
        }
        }
    };

    // // Prepare chart data
    // const sentimentData = {
    //     labels: Object.keys(filteredEmotions),
    //     datasets: [{
    //     label: 'Emotion Distribution',
    //     data: Object.values(filteredEmotions),
    //     backgroundColor: Object.keys(filteredEmotions).map(emotion => 
    //         emotionColors[emotion.toLowerCase()] || '#94a3b8'
    //     ),
    //     borderWidth: 1,
    //     }]
    // };

    // const barData = {
    //     labels: Object.keys(filteredEmotions),
    //     datasets: [{
    //     label: 'Emotion Intensity',
    //     data: Object.values(filteredEmotions),
    //     backgroundColor: Object.keys(filteredEmotions).map(emotion => 
    //         emotionColors[emotion.toLowerCase()] || '#94a3b8'
    //     ),
    //     }]
    // };

    // Horizontal bar chart options
    // const horizontalBarOptions = {
    //     ...chartOptions,
    //     indexAxis: 'y',
    //     scales: {
    //     x: {
    //         beginAtZero: true
    //     },
    //     y: {
    //         ticks: {
    //         autoSkip: false
    //         }
    //     }
    //     }
    // };

    const getSentimentIcon = () => {
        if (!sentimentResult) return null;
        
        const size = 48;
        const commonProps = { size, className: 'mx-auto' };
        
        switch(sentimentResult.overallSentiment.toLowerCase()) {
        case 'positive':
            return <FaSmile {...commonProps} className="text-green-500" />;
        case 'negative':
            return <FaFrown {...commonProps} className="text-red-500" />;
        default:
            return <FaMeh {...commonProps} className="text-yellow-500" />;
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50 py-12 px-4 sm:px-6 lg:px-8">
        <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="max-w-4xl mx-auto"
        >
            <div className="text-center mb-12">
            <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
                Emotion <span className="text-indigo-600">Insight</span>
            </h1>
            <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
                Analyze the emotional tone of your text with Sentiment Analyzer
            </p>
            </div>

            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="p-6 sm:p-8">
                <div className="space-y-6">
                <div>
                    <label htmlFor="text-input" className="block text-sm font-medium text-gray-700 mb-2">
                    Enter text or use voice input
                    </label>
                    <div className="relative">
                    <textarea
                        id="text-input"
                        rows="4"
                        className="block w-full text-gray-800 px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 resize-none"
                        placeholder="Type or speak your text here..."
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                    />
                    <button
                        onClick={toggleRecording}
                        className={`absolute bottom-3 right-3 p-3 rounded-full ${isRecording ? 'bg-red-500 text-white' : 'bg-indigo-100 text-indigo-700'} transition-all duration-200 hover:scale-105`}
                        aria-label={isRecording ? 'Stop recording' : 'Start recording'}
                    >
                        {isRecording ? <FaStop /> : <FaMicrophone />}
                    </button>
                    </div>
                </div>

                <div className="flex justify-center">
                    <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={analyzeSentiment}
                    disabled={isAnalyzing || !text.trim()}
                    className={`px-6 py-3 rounded-lg font-medium text-white shadow-md ${isAnalyzing || !text.trim() ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'} transition-colors duration-200 flex items-center`}
                    >
                    {isAnalyzing ? (
                        <>
                        <FaSpinner className="animate-spin mr-2" />
                        Analyzing...
                        </>
                    ) : (
                        'Analyze Sentiment'
                    )}
                    </motion.button>
                </div>
                </div>
            </div>

            <AnimatePresence>
                {(sentimentResult || isAnalyzing) && (
                <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.5 }}
                    className="bg-gray-50 p-6 sm:p-8 border-t border-gray-200"
                >
                    {isAnalyzing ? (
                    <div className="flex justify-center items-center h-64">
                       <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                            className="w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full"
                        />
                    </div>
                    ) : (
                    <div className="space-y-8">
                        <div className="text-center">
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">Analysis Results</h3>
                        
                        <motion.div
                            initial={{ scale: 0.8 }}
                            animate={{ scale: 1 }}
                            className="inline-block"
                        >
                            <div className="flex items-center justify-center space-x-4">
                            {getSentimentIcon()}
                            <div>
                                <p className="text-lg font-medium text-gray-700">Overall Sentiment:</p>
                                <p className={`text-2xl font-bold ${
                                sentimentResult?.overallSentiment?.toLowerCase() === 'positive' ? 'text-green-600' :
                                sentimentResult?.overallSentiment?.toLowerCase() === 'negative' ? 'text-red-600' : 'text-yellow-600'
                                }`}>
                                {sentimentResult?.overallSentiment} {sentimentResult?.overallScore && `(${sentimentResult.overallScore}%)`}
                                </p>
                            </div>
                            </div>
                        </motion.div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            {/* Doughnut Chart */}
                            <motion.div
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.2 }}
                                className="bg-white p-4 rounded-xl shadow-md"
                            >
                                <h4 className="text-lg font-semibold text-center mb-4">Emotion Distribution</h4>
                                <div className="h-80 relative">
                                <Doughnut 
                                    data={chartData} 
                                    options={doughnutOptions}
                                />
                                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                                    <div className="text-center">
                                    <p className="text-sm text-gray-500">Total</p>
                                    <p className="text-2xl font-bold text-indigo-600">
                                        {processedEmotions.reduce((sum, [_, score]) => sum + score, 0)}
                                    </p>
                                    </div>
                                </div>
                                </div>
                            </motion.div>

                            {/* Radar Chart */}
                            <motion.div
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.4 }}
                                className="bg-white p-4 rounded-xl shadow-md"
                            >
                                <h4 className="text-lg font-semibold text-center mb-4">Emotion Profile</h4>
                                <div className="h-80">
                                <Radar 
                                    data={{
                                    ...chartData,
                                    datasets: [{
                                        ...chartData.datasets[0],
                                        backgroundColor: 'rgba(99, 102, 241, 0.2)',
                                        borderColor: '#6366F1',
                                        pointBackgroundColor: '#6366F1',
                                        pointBorderColor: '#fff',
                                    }]
                                    }} 
                                    options={radarOptions}
                                />
                                </div>
                            </motion.div>
                        </div>
                    </div>
                    )}
                </motion.div>
                )}
            </AnimatePresence>
            </div>
        </motion.div>
        </div>
    );
}
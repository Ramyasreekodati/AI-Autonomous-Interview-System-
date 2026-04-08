import React, { useState, useEffect } from 'react';
import { Camera, Send, Mic, AlertCircle, CheckCircle2 } from 'lucide-react';

const Interview = () => {
    const [questions, setQuestions] = useState([
        { id: 1, text: "Explain the concept of Virtual DOM in React.", category: "Technical" },
        { id: 2, text: "What is the difference between supervised and unsupervised learning?", category: "AI/ML" },
        { id: 3, text: "How do you handle conflict in a team environment?", category: "Behavioral" }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [answer, setAnswer] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        let ws;
        let frameInterval;
        const currentInterviewId = 1; // Simulation ID

        const startWebcam = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                const video = document.getElementById('webcam-preview');
                if (video) {
                    video.srcObject = stream;
                }

                // Connect WebSocket
                ws = new WebSocket(`ws://localhost:8000/ws/alerts/${currentInterviewId}`);
                
                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    if (data.type === "ALERT") {
                        setAlerts(prev => [...new Set([...prev, data.message])]);
                    }
                };

                // Capture and send frames every 2 seconds
                frameInterval = setInterval(() => {
                    if (ws.readyState === WebSocket.OPEN && video) {
                        const canvas = document.createElement('canvas');
                        canvas.width = video.videoWidth;
                        canvas.height = video.videoHeight;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(video, 0, 0);
                        const dataURL = canvas.toDataURL('image/jpeg', 0.5);
                        ws.send(dataURL);
                    }
                }, 2000);

            } catch (err) {
                console.error("Error accessing webcam: ", err);
                setAlerts(prev => [...prev, "Webcam access denied. Please enable camera for monitoring."]);
            }
        };

        startWebcam();
        
        return () => {
            if (frameInterval) clearInterval(frameInterval);
            if (ws) ws.close();
            const video = document.getElementById('webcam-preview');
            if (video && video.srcObject) {
                video.srcObject.getTracks().forEach(track => track.stop());
            }
        };
    }, []);

    const handleNext = () => {
        setIsSubmitting(true);
        // Simulate API call
        setTimeout(() => {
            if (currentStep < questions.length - 1) {
                setCurrentStep(currentStep + 1);
                setAnswer("");
                setIsSubmitting(false);
            } else {
                alert("Interview Completed!");
            }
        }, 1000);
    };

    return (
        <div className="container py-10 min-h-screen fade-in">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Side: Video Preview (Placeholder for Phase 2) */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="glass-card aspect-video relative overflow-hidden flex items-center justify-center bg-black/40">
                        <video 
                            id="webcam-preview"
                            autoPlay 
                            playsInline 
                            muted 
                            className="w-full h-full object-cover"
                        />
                        <div className="absolute top-4 left-4 flex items-center gap-2 px-3 py-1 bg-accent/20 rounded-full border border-accent/30">
                            <div className="w-2 h-2 rounded-full bg-accent animate-ping" />
                            <span className="text-accent text-xs font-bold uppercase tracking-wider">Live Monitoring</span>
                        </div>
                    </div>

                    <div className="glass-card p-6">
                        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <AlertCircle className="text-secondary" size={20} /> Real-time Audit
                        </h3>
                        <div className="space-y-3">
                            {alerts.length === 0 ? (
                                <p className="text-text-secondary text-sm">No suspicious behavior detected.</p>
                            ) : (
                                alerts.map((a, i) => (
                                    <div key={i} className="flex gap-2 text-sm text-accent">
                                        <span>•</span>
                                        <p>{a}</p>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Side: Question & Response area */}
                <div className="lg:col-span-2">
                    <div className="glass-card p-10 h-full flex flex-col">
                        <div className="mb-8">
                            <div className="flex justify-between items-center mb-4">
                                <span className="text-primary text-sm font-bold uppercase tracking-widest">
                                    Question {currentStep + 1} of {questions.length}
                                </span>
                                <span className="px-3 py-1 bg-surface rounded-full text-xs font-medium border border-glass-border">
                                    {questions[currentStep].category}
                                </span>
                            </div>
                            <h2 className="text-3xl font-bold">
                                {questions[currentStep].text}
                            </h2>
                        </div>

                        <div className="flex-grow">
                            <textarea 
                                value={answer}
                                onChange={(e) => setAnswer(e.target.value)}
                                placeholder="State your answer clearly..."
                                className="input-field h-64 resize-none text-lg leading-relaxed"
                            />
                        </div>

                        <div className="mt-8 flex justify-between items-center">
                            <div className="flex gap-4">
                                <button className="p-3 rounded-full bg-surface border border-glass-border hover:text-primary transition-all">
                                    <Mic size={24} />
                                </button>
                            </div>
                            <button 
                                onClick={handleNext}
                                disabled={isSubmitting || !answer}
                                className="btn-primary flex items-center gap-2 group"
                            >
                                {isSubmitting ? 'Processing AI scoring...' : (
                                    <>Submit Answer <Send size={18} className="group-hover:translate-x-1 transition-transform" /></>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Interview;

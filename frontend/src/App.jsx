import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Camera, Video, Mic, CheckCircle, AlertCircle, Play } from 'lucide-react';

const API_BASE = "http://localhost:8000";

function App() {
  const [session, setSession] = useState(null);
  const [name, setName] = useState('');
  const [questions, setQuestions] = useState([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [analysis, setAnalysis] = useState({ emotion: 'Neutral', focus: 100 });
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const wsRef = useRef(null);

  useEffect(() => {
    if (session && !wsRef.current) {
      const ws = new WebSocket(`ws://localhost:8000/ws/analyze/${session.session_id}`);
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setAnalysis({ emotion: data.emotion, focus: data.focus_score * 100 });
      };
      wsRef.current = ws;

      const interval = setInterval(() => {
        captureFrame();
      }, 500); // Send frame every 500ms

      return () => {
        clearInterval(interval);
        ws.close();
      };
    }
  }, [session]);

  const captureFrame = () => {
    if (videoRef.current && wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      canvas.toBlob((blob) => {
        if (blob) wsRef.current.send(blob);
      }, 'image/jpeg', 0.5);
    }
  };

  const startSession = async () => {
    try {
      const formData = new FormData();
      formData.append('candidate_name', name);
      const res = await axios.post(`${API_BASE}/session/start`, formData);
      setSession(res.data);
      const qRes = await axios.get(`${API_BASE}/questions`);
      setQuestions(qRes.data);
      startCamera();
    } catch (err) {
      console.error("Start session failed", err);
    }
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      if (videoRef.current) videoRef.current.srcObject = stream;
    } catch (err) {
      console.error("Camera access failed", err);
    }
  };

  const nextQuestion = async () => {
    try {
      // Analyze current answer (simulation of speech-to-text here)
      const formData = new FormData();
      formData.append('session_id', session.session_id);
      formData.append('question_id', questions[currentIdx].id);
      formData.append('text', "The candidate explained the concepts clearly."); // Mock speech text
      await axios.post(`${API_BASE}/analyze/speech`, formData);

      if (currentIdx < questions.length - 1) {
        setCurrentIdx(currentIdx + 1);
      } else {
        finishInterview();
      }
    } catch (err) {
      console.error("Failed to submit answer", err);
    }
  };

  const finishInterview = async () => {
    try {
      const res = await axios.get(`${API_BASE}/report/${session.session_id}`);
      alert("Interview Complete! Your report is being generated.");
      window.open(`${API_BASE}${res.data.report_url}`, '_blank');
      setSession(null);
    } catch (err) {
      console.error("Failed to finish interview", err);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-900 text-white font-sans p-8">
      {!session ? (
        <div className="max-w-md mx-auto mt-20 text-center">
          <h1 className="text-4xl font-extrabold mb-6 text-indigo-400">AI Interview Portal</h1>
          <div className="bg-neutral-800 p-8 rounded-2xl shadow-2xl">
            <input
              type="text"
              placeholder="Enter your full name"
              className="w-full bg-neutral-700 p-4 rounded-xl mb-6 text-white text-lg focus:ring-2 focus:ring-indigo-500 outline-none"
              onChange={(e) => setName(e.target.value)}
            />
            <button
              onClick={startSession}
              disabled={!name}
              className="w-full bg-indigo-600 hover:bg-indigo-500 p-4 rounded-xl font-bold flex items-center justify-center gap-2 transition"
            >
              <Play size={20} /> Begin Interview
            </button>
          </div>
        </div>
      ) : (
        <div className="flex gap-8">
          {/* Video Section */}
          <div className="flex-1 space-y-4">
            <div className="relative bg-black rounded-3xl overflow-hidden shadow-2xl aspect-video border-4 border-indigo-600">
              <video ref={videoRef} autoPlay muted className="w-full h-full object-cover" />
              <div className="absolute top-4 left-4 bg-indigo-600/80 px-4 py-2 rounded-full flex items-center gap-2">
                <Video size={16} /> LIVE
              </div>
              <div className="absolute bottom-4 right-4 bg-black/60 p-4 rounded-xl border border-white/20">
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-gray-300">Emotion:</span>
                  <span className="text-green-400 font-bold">{analysis.emotion}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-gray-300">Focus:</span>
                  <span className="text-indigo-400 font-bold">{analysis.focus}%</span>
                </div>
              </div>
            </div>
            <div className="flex gap-4">
               <div className="bg-neutral-800 p-4 rounded-xl flex-1 border border-white/10">
                 <div className="flex items-center gap-2 text-indigo-400 mb-1">
                   <AlertCircle size={16} /> Status
                 </div>
                 <p className="text-sm">Recording in progress...</p>
               </div>
               <div className="bg-neutral-800 p-4 rounded-xl flex-1 border border-white/10">
                 <div className="flex items-center gap-2 text-green-400 mb-1">
                   <CheckCircle size={16} /> Audio
                 </div>
                 <p className="text-sm">Signal Strong</p>
               </div>
            </div>
          </div>

          {/* Question Section */}
          <div className="w-1/3 space-y-4 flex flex-col">
            <div className="bg-neutral-800 p-8 rounded-3xl border border-white/10 flex-1 relative overflow-hidden">
               <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-600/10 blur-3xl -mr-16 -mt-16"></div>
               <h2 className="text-indigo-400 text-sm font-bold uppercase tracking-wider mb-2">
                 Question {currentIdx + 1} of {questions.length}
               </h2>
               <p className="text-2xl font-semibold mb-8 h-24 overflow-auto">
                 {questions[currentIdx]?.text}
               </p>
               <button
                 onClick={nextQuestion}
                 className="w-full bg-white text-black hover:bg-gray-200 p-4 rounded-xl font-bold transition flex items-center justify-center gap-2"
               >
                 Submit Answer and Continue
               </button>
            </div>
            <div className="bg-neutral-800 p-6 rounded-3xl border border-white/10">
               <p className="text-gray-400 text-xs mb-2">CANDIDATE: {session.candidate_name}</p>
               <p className="text-gray-400 text-xs">SESSION ID: {session.session_id}</p>
            </div>
          </div>
        </div>
      )}
      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
}

export default App;

import React from 'react';
import { Shield, Cpu, Zap, Camera, Mic, BarChart3 } from 'lucide-react';

const Home = () => {
  return (
    <div className="container py-20 fade-in">
      <header className="text-center mb-16">
        <h1 className="text-6xl font-bold mb-4">
          <span className="premium-gradient-text">AI Interview</span> Ecosystem
        </h1>
        <p className="text-text-secondary text-xl max-w-2xl mx-auto">
          The next generation of autonomous recruitment intelligence. 
          Real-time surveillance, behavioral analysis, and explainable scoring.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
        <FeatureCard 
          icon={<Camera className="text-primary" size={32} />}
          title="AI Surveillance"
          desc="Face, gaze, and object detection with YOLO and MediaPipe. Integrated WebRTC streaming."
        />
        <FeatureCard 
          icon={<Cpu className="text-secondary" size={32} />}
          title="Core Intelligence"
          desc="Transformer-based NLP models evaluate answer quality and semantic relevance."
        />
        <FeatureCard 
          icon={<Shield className="text-accent" size={32} />}
          title="Anti-Cheating"
          desc="Real-time alerts for suspicious behavior with multi-factor risk assessment."
        />
      </div>

      <div className="glass-card p-12 text-center">
        <h2 className="text-3xl font-bold mb-6">Ready to transform your hiring?</h2>
        <div className="flex justify-center gap-4">
          <button className="btn-primary flex items-center gap-2">
            Get Started <Zap size={18} />
          </button>
          <button className="px-8 py-3 rounded-lg border border-glass-border font-semibold hover:bg-glass transition-all">
            View Analytics
          </button>
        </div>
      </div>
    </div>
  );
};

const FeatureCard = ({ icon, title, desc }) => (
  <div className="glass-card p-8 hover:transform hover:scale-105 transition-all duration-300">
    <div className="mb-4">{icon}</div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-text-secondary">{desc}</p>
  </div>
);

export default Home;

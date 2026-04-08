import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, User, ArrowRight } from 'lucide-react';

const Login = () => {
  const [isLogin, setIsLogin] = useState(true);
  const navigate = useNavigate();

  const handleAuth = (e) => {
    e.preventDefault();
    // Simulate login
    navigate('/interview');
  };

  return (
    <div className="container min-h-screen flex items-center justify-center fade-in">
      <div className="glass-card p-10 w-full max-w-md">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold premium-gradient-text">
            {isLogin ? 'Welcome Back' : 'Join the Future'}
          </h2>
          <p className="text-text-secondary mt-2">
            {isLogin ? 'Login to continue your journey' : 'Create an account to get started'}
          </p>
        </div>

        <form onSubmit={handleAuth} className="space-y-6">
          {!isLogin && (
            <div className="relative">
              <User className="absolute left-3 top-3.5 text-text-secondary" size={20} />
              <input 
                type="text" 
                placeholder="Full Name" 
                className="input-field pl-12"
                required={!isLogin}
              />
            </div>
          )}

          <div className="relative">
            <Mail className="absolute left-3 top-3.5 text-text-secondary" size={20} />
            <input 
              type="email" 
              placeholder="Email Address" 
              className="input-field pl-12"
              required
            />
          </div>

          <div className="relative">
            <Lock className="absolute left-3 top-3.5 text-text-secondary" size={20} />
            <input 
              type="password" 
              placeholder="Password" 
              className="input-field pl-12"
              required
            />
          </div>

          <button type="submit" className="btn-primary w-full flex items-center justify-center gap-2">
            {isLogin ? 'Sign In' : 'Create Account'} <ArrowRight size={18} />
          </button>
        </form>

        <div className="mt-8 text-center text-text-secondary">
          <button 
            onClick={() => setIsLogin(!isLogin)}
            className="hover:text-primary transition-colors"
          >
            {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Login"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;

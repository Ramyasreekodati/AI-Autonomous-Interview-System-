import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Users, FileText, AlertTriangle, TrendingUp, Search } from 'lucide-react';

const API_BASE = "http://localhost:8000";

function Admin() {
  const [sessions, setSessions] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const res = await axios.get(`${API_BASE}/admin/sessions`);
      setSessions(res.data);
    } catch (err) {
      console.error("Failed to fetch sessions", err);
    }
  };

  const filteredSessions = sessions.filter(s => 
    s.candidate_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-neutral-950 text-white p-8 font-sans">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center mb-12">
          <div>
            <h1 className="text-4xl font-black bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Admin Analytics
            </h1>
            <p className="text-gray-400 mt-2">Monitoring {sessions.length} interview sessions</p>
          </div>
          <div className="relative">
            <Search className="absolute left-4 top-3.5 text-gray-500" size={18} />
            <input 
              type="text" 
              placeholder="Search candidates..."
              className="bg-neutral-900 border border-white/10 rounded-full py-3 pl-12 pr-6 outline-none focus:ring-2 focus:ring-indigo-500 transition"
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <StatCard icon={<Users className="text-indigo-400" />} label="Total Candidates" value={sessions.length} />
          <StatCard icon={<TrendingUp className="text-green-400" />} label="Avg. Score" value="82%" />
          <StatCard icon={<AlertTriangle className="text-yellow-400" />} label="Alerts Flagged" value="14" />
        </div>

        <div className="bg-neutral-900 border border-white/10 rounded-3xl overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-white/5 text-gray-400 uppercase text-xs font-bold tracking-widest">
              <tr>
                <th className="px-8 py-6">Candidate</th>
                <th className="px-8 py-6">ID</th>
                <th className="px-8 py-6">Status</th>
                <th className="px-8 py-6">Date</th>
                <th className="px-8 py-6 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {filteredSessions.map((session) => (
                <tr key={session.id} className="hover:bg-white/5 transition">
                  <td className="px-8 py-6 font-bold">{session.candidate_name}</td>
                  <td className="px-8 py-6 text-gray-400 text-sm font-mono">{session.id}</td>
                  <td className="px-8 py-6">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      session.status === 'completed' ? 'bg-green-500/20 text-green-400' : 'bg-indigo-500/20 text-indigo-400'
                    }`}>
                      {session.status}
                    </span>
                  </td>
                  <td className="px-8 py-6 text-gray-400">{new Date(session.started_at).toLocaleDateString()}</td>
                  <td className="px-8 py-6 text-right">
                    <button 
                      onClick={() => window.open(`${API_BASE}/reports/report_${session.id}.pdf`, '_blank')}
                      className="text-indigo-400 hover:text-indigo-300 flex items-center gap-2 justify-end font-bold"
                    >
                      <FileText size={18} /> View Report
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value }) {
  return (
    <div className="bg-neutral-900 border border-white/10 p-8 rounded-3xl flex items-center gap-6">
      <div className="bg-white/5 p-4 rounded-2xl">{icon}</div>
      <div>
        <p className="text-gray-400 text-sm font-bold uppercase tracking-widest">{label}</p>
        <p className="text-3xl font-black mt-1">{value}</p>
      </div>
    </div>
  );
}

export default Admin;

import React, { useState } from 'react';
import { Users, BarChart3, ShieldAlert, CheckCircle, ExternalLink, Search } from 'lucide-react';

const Admin = () => {
    const [candidates, setCandidates] = useState([
        { id: 1, name: "John Doe", score: 8.5, risk: "Low", status: "Completed", date: "2026-04-08" },
        { id: 2, name: "Jane Smith", score: 4.2, risk: "High", status: "Under Review", date: "2026-04-07" },
        { id: 3, name: "Alice Brown", score: 9.1, risk: "Low", status: "Completed", date: "2026-04-08" },
        { id: 4, name: "Bob Wilson", score: 6.8, risk: "Medium", status: "Completed", date: "2026-04-06" }
    ]);

    return (
        <div className="container py-20 fade-in">
            <header className="mb-12 flex justify-between items-end">
                <div>
                    <h1 className="text-4xl font-bold mb-2">Recruitment <span className="premium-gradient-text">Intelligence</span></h1>
                    <p className="text-text-secondary">Monitor candidate performance and behavioral audit logs.</p>
                </div>
                <div className="flex gap-4">
                    <div className="glass-card px-6 py-4 flex items-center gap-4">
                        <Users className="text-primary" />
                        <div>
                            <p className="text-xs text-text-secondary uppercase">Total Candidates</p>
                            <p className="text-xl font-bold">1,284</p>
                        </div>
                    </div>
                    <div className="glass-card px-6 py-4 flex items-center gap-4">
                        <ShieldAlert className="text-secondary" />
                        <div>
                            <p className="text-xs text-text-secondary uppercase">Risk Alerts</p>
                            <p className="text-xl font-bold">12</p>
                        </div>
                    </div>
                </div>
            </header>

            <div className="glass-card overflow-hidden">
                <div className="p-6 border-b border-glass-border flex gap-4">
                    <div className="relative flex-grow">
                        <Search className="absolute left-3 top-2.5 text-text-secondary" size={18} />
                        <input type="text" placeholder="Search candidates..." className="input-field pl-10 h-10 py-0" />
                    </div>
                    <button className="btn-primary py-2 px-6 text-sm">Export PDF</button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-surface/50 text-text-secondary text-xs uppercase tracking-widest">
                                <th className="px-8 py-4">Candidate</th>
                                <th className="px-8 py-4">Score</th>
                                <th className="px-8 py-4">Behavior Risk</th>
                                <th className="px-8 py-4">Status</th>
                                <th className="px-8 py-4">Date</th>
                                <th className="px-8 py-4">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-glass-border">
                            {candidates.map((c) => (
                                <tr key={c.id} className="hover:bg-accent/5 transition-colors">
                                    <td className="px-8 py-6 font-bold">{c.name}</td>
                                    <td className="px-8 py-6">
                                        <div className="flex items-center gap-2">
                                            <div className="w-12 h-2 bg-surface rounded-full overflow-hidden">
                                                <div 
                                                    className={`h-full ${c.score > 7 ? 'bg-primary' : c.score > 5 ? 'bg-yellow-400' : 'bg-secondary'}`} 
                                                    style={{ width: `${c.score * 10}%` }}
                                                />
                                            </div>
                                            <span className="font-mono">{c.score}</span>
                                        </div>
                                    </td>
                                    <td className="px-8 py-6">
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
                                            c.risk === 'Low' ? 'bg-primary/20 text-primary' : 
                                            c.risk === 'Medium' ? 'bg-yellow-400/20 text-yellow-400' : 
                                            'bg-secondary/20 text-secondary'
                                        }`}>
                                            {c.risk}
                                        </span>
                                    </td>
                                    <td className="px-8 py-6 text-sm flex items-center gap-2">
                                        {c.status === 'Completed' ? <CheckCircle size={14} className="text-primary" /> : <BarChart3 size={14} className="text-text-secondary" />}
                                        {c.status}
                                    </td>
                                    <td className="px-8 py-6 text-sm text-text-secondary">{c.date}</td>
                                    <td className="px-8 py-6">
                                        <button className="text-primary hover:underline flex items-center gap-1 text-sm font-bold">
                                            View Details <ExternalLink size={14} />
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
};

export default Admin;

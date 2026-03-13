"use client";
import ResumeChatbot from './ResumeChatbot';

export default function AnalysisResults({ data }: { data: any }) {
    if (!data) return null;

    const scoreColor = data.ats_score >= 80 ? '#22c55e' : data.ats_score >= 60 ? '#eab308' : '#ef4444';

    return (
        <div style={{ marginTop: '3rem', width: '100%', animation: 'fadeIn 0.5s ease-in-out' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 1fr) 2fr', gap: '2rem', alignItems: 'start' }} className="dashboard-grid">

                {/* Left Column: Stats & DNA */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

                    {/* ATS Score Card */}
                    <div className="card" style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '3rem 1.5rem' }}>
                        <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>ATS Compatibility Score</h2>
                        <div style={{
                            width: '160px', height: '160px', borderRadius: '50%', border: `10px solid ${scoreColor}`,
                            display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto',
                            fontSize: '3.5rem', fontWeight: 'bold', color: scoreColor, boxShadow: `0 0 40px ${scoreColor}20`
                        }}>
                            {data.ats_score}
                        </div>
                    </div>

                    {/* Resume DNA */}
                    <div className="card">
                        <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            🧬 Resume DNA
                        </h2>

                        {/* Contact Info */}
                        <div style={{ marginBottom: '1.5rem', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <span>📧</span> <span>{data.details?.contact_info?.email || 'No Email'}</span>
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <span>📱</span> <span>{data.details?.contact_info?.phone || 'No Phone'}</span>
                                </div>
                            </div>
                        </div>

                        {/* Breakdown Bars */}
                        {data.score_breakdown && (
                            <div style={{ marginBottom: '1.5rem' }}>
                                {Object.entries(data.score_breakdown).map(([key, score]: [string, any]) => (
                                    <div key={key} style={{ marginBottom: '0.8rem' }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.25rem', textTransform: 'capitalize', color: 'var(--text-secondary)' }}>
                                            <span>{key}</span>
                                            <span>{score}/100</span>
                                        </div>
                                        <div style={{ width: '100%', height: '6px', background: '#334155', borderRadius: '3px' }}>
                                            <div style={{
                                                width: `${score}%`,
                                                height: '100%',
                                                background: score > 70 ? '#4ade80' : score > 40 ? '#eab308' : '#f87171',
                                                borderRadius: '3px'
                                            }}></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Skills Cloud */}
                        <div>
                            <h3 style={{ fontSize: '0.9rem', marginBottom: '0.75rem', color: '#c4b5fd', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Detected Skills</h3>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                {data.details?.extracted_skills && data.details.extracted_skills.length > 0 ? (
                                    data.details.extracted_skills.map((skill: string, i: number) => (
                                        <span key={i} style={{
                                            background: 'rgba(139, 92, 246, 0.1)',
                                            color: 'var(--primary)',
                                            border: '1px solid rgba(139, 92, 246, 0.2)',
                                            padding: '0.25rem 0.6rem',
                                            borderRadius: '12px',
                                            fontSize: '0.8rem'
                                        }}>
                                            {skill}
                                        </span>
                                    ))
                                ) : (
                                    <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>No specific skills detected.</span>
                                )}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Analysis & Matches */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

                    {/* Job Target Banner */}
                    {data.job_role && (
                        <div className="card" style={{ borderLeft: '4px solid var(--primary)', background: 'linear-gradient(to right, rgba(139, 92, 246, 0.1), transparent)' }}>
                            <h2 style={{ fontSize: '1.5rem', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                🎯 Target: <span style={{ color: 'var(--primary)' }}>{data.job_role}</span>
                            </h2>
                            <p style={{ color: 'var(--text-secondary)' }}>Optimization analysis based on this specific role.</p>
                        </div>
                    )}

                    {/* Company Eligibility */}
                    {data.company_matches && data.company_matches.length > 0 && (
                        <div className="card">
                            <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem' }}>🏢 Company Eligibility</h2>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
                                {data.company_matches.map((match: any, i: number) => (
                                    <div key={i} style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border)' }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                                            <span style={{ fontWeight: '600' }}>{match.company}</span>
                                            <span style={{
                                                fontSize: '0.9rem',
                                                padding: '0.2rem 0.5rem',
                                                borderRadius: '4px',
                                                background: match.match_score >= 75 ? 'rgba(74, 222, 128, 0.2)' : 'rgba(248, 113, 113, 0.2)',
                                                color: match.match_score >= 75 ? '#4ade80' : '#f87171',
                                            }}>{match.match_score}%</span>
                                        </div>
                                        {match.missing_skills.length > 0 ? (
                                            <div style={{ marginTop: '0.75rem' }}>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Consider Adding:</div>
                                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem' }}>
                                                    {match.missing_skills.map((skill: string, j: number) => (
                                                        <span key={j} style={{ fontSize: '0.75rem', color: '#fca5a5' }}>• {skill}</span>
                                                    ))}
                                                </div>
                                            </div>
                                        ) : (
                                            <div style={{ fontSize: '0.8rem', color: '#4ade80', marginTop: '0.5rem' }}>✓ Good Skill Match</div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Insights Grid */}
                    <div className="card">
                        <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem' }}>📝 Detailed Insights</h2>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                            <div>
                                <h3 style={{ color: '#4ade80', fontSize: '1rem', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <span>✓</span> Strengths
                                </h3>
                                <ul style={{ paddingLeft: '0', listStyle: 'none', color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                                    {data.strengths.map((s: string, i: number) => (
                                        <li key={i} style={{ marginBottom: '0.5rem', display: 'flex', alignItems: 'start', gap: '0.5rem' }}>
                                            <span style={{ color: '#4ade80', marginTop: '4px', fontSize: '0.6rem' }}>●</span>
                                            {s}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div>
                                <h3 style={{ color: '#f87171', fontSize: '1rem', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <span>!</span> Improvements
                                </h3>
                                <ul style={{ paddingLeft: '0', listStyle: 'none', color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                                    {data.weaknesses.map((w: string, i: number) => (
                                        <li key={i} style={{ marginBottom: '0.5rem', display: 'flex', alignItems: 'start', gap: '0.5rem' }}>
                                            <span style={{ color: '#f87171', marginTop: '4px', fontSize: '0.6rem' }}>●</span>
                                            {w}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>

                </div>
            </div>

            <ResumeChatbot />
        </div>
    );
}

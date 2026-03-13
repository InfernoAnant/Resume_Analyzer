"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ResumeChatbot from '@/components/ResumeChatbot';

export default function Dashboard() {
    const [data, setData] = useState<any>(null);
    const router = useRouter();

    useEffect(() => {
        const stored = localStorage.getItem('resumeAnalysis');
        if (!stored) {
            router.push('/');
            return;
        }
        setData(JSON.parse(stored));
    }, [router]);

    if (!data) return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'white' }}>Loading results...</div>;

    const scoreColor = data.ats_score >= 80 ? '#22c55e' : data.ats_score >= 60 ? '#eab308' : '#ef4444';

    return (
        <div className="container" style={{ padding: '2rem 0' }}>
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
                <h1 style={{ margin: 0, fontSize: '2rem' }}>Analysis Results</h1>
                <button onClick={() => router.push('/')} className="btn" style={{ background: 'rgba(255,255,255,0.1)', color: 'white' }}>Upload New Resume</button>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
                {/* Score Card */}
                <div className="card" style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                    <h2 style={{ fontSize: '1.5rem', marginBottom: '2rem' }}>ATS Compatibility</h2>
                    <div style={{
                        width: '200px', height: '200px', borderRadius: '50%', border: `12px solid ${scoreColor}`,
                        display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto',
                        fontSize: '4.5rem', fontWeight: 'bold', color: scoreColor, boxShadow: `0 0 30px ${scoreColor}40`
                    }}>
                        {data.ats_score}
                    </div>
                    <p style={{ marginTop: '2rem', fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
                        {data.ats_score >= 80 ? 'Excellent! Your resume is well-optimized.' : 'Good start, but needs improvement.'}
                    </p>
                </div>

                {/* Details */}
                <div className="card">
                    <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Insight Breakdown</h2>

                    <div style={{ marginBottom: '2rem' }}>
                        <h3 style={{ color: '#4ade80', fontSize: '1.1rem', marginBottom: '0.5rem' }}>✅ Strength Areas</h3>
                        <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-secondary)' }}>
                            {data.strengths.map((s: string, i: number) => <li key={i} style={{ marginBottom: '0.25rem' }}>{s}</li>)}
                        </ul>
                    </div>

                    <div style={{ marginBottom: '2rem' }}>
                        <h3 style={{ color: '#f87171', fontSize: '1.1rem', marginBottom: '0.5rem' }}>⚠️ Areas for Improvement</h3>
                        <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-secondary)' }}>
                            {data.weaknesses.map((w: string, i: number) => <li key={i} style={{ marginBottom: '0.25rem' }}>{w}</li>)}
                        </ul>
                    </div>

                    <div>
                        <h3 style={{ fontSize: '1.1rem' }}>Metrics</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
                            <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Word Count</div>
                                <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{data.details.word_count}</div>
                            </div>
                            <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Sentences</div>
                                <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{data.details.sentences}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Extracted Skills */}
            <div className="card" style={{ marginTop: '2rem' }}>
                <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Detected Keywords & Entities</h2>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
                    {data.details.extracted_skills_demo?.length > 0 ? data.details.extracted_skills_demo.map((skill: string, i: number) => (
                        <span key={i} style={{
                            background: 'rgba(139, 92, 246, 0.1)',
                            color: '#c4b5fd',
                            padding: '0.5rem 1rem',
                            borderRadius: '20px',
                            fontSize: '0.9rem',
                            border: '1px solid rgba(139, 92, 246, 0.2)'
                        }}>
                            {skill}
                        </span>
                    )) : <span style={{ color: 'var(--text-secondary)' }}>No specific keywords detected.</span>}
                </div>
            </div>
            <ResumeChatbot />
        </div>
    );
}

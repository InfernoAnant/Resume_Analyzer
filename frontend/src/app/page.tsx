"use client";
import ResumeUpload from '@/components/ResumeUpload';
import AnalysisResults from '@/components/AnalysisResults';
import { useState, useRef } from 'react';

export default function Home() {
  const [results, setResults] = useState<any>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  const handleComplete = (data: any) => {
    setResults(data);
    setTimeout(() => {
      resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  return (
    <main style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '4rem 2rem', background: 'radial-gradient(circle at top center, #1e293b 0%, #0f172a 100%)' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem', maxWidth: '800px' }}>
        <h1 style={{ fontSize: '3.5rem', background: 'linear-gradient(to right, #8b5cf6, #06b6d4)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: '1.5rem' }}>
          AI-Powered Resume Optimization
        </h1>
        <p style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          Beat the ATS and land your dream job. Upload your resume and add your target roles to get instant, tailored feedback.
        </p>
      </div>

      <div style={{ width: '100%', maxWidth: '800px' }}>
        <ResumeUpload onAnalysisComplete={handleComplete} />
      </div>

      {results ? (
        <div ref={resultsRef} style={{ width: '100%', maxWidth: '1000px' }}>
          <AnalysisResults data={results} />
          <button
            onClick={() => { setResults(null); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
            style={{ display: 'block', margin: '2rem auto 0', background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', textDecoration: 'underline' }}
          >
            Analyze Another Resume
          </button>
        </div>
      ) : (
        <div style={{ marginTop: '5rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', maxWidth: '1200px', width: '100%' }}>
          {[
            { icon: '🎯', title: 'Smart Scoring', desc: 'Get a detailed ATS compatibility score based on modern hiring algorithms.' },
            { icon: '🔍', title: 'Gap Analysis', desc: 'Identify missing keywords and skills crucial for your target role.' },
            { icon: '🏢', title: 'Company Match Check', desc: 'See how well you fit specifically for companies like Google, Amazon, etc.' }
          ].map((feat, i) => (
            <div key={i} className="card" style={{ textAlign: 'left', background: 'rgba(30, 41, 59, 0.4)' }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>{feat.icon}</div>
              <h3 style={{ fontSize: '1.25rem', color: 'white' }}>{feat.title}</h3>
              <p style={{ color: 'var(--text-secondary)' }}>{feat.desc}</p>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}

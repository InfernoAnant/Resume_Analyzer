"use client";
import { useState } from 'react';

export default function ResumeUpload({ onAnalysisComplete }: { onAnalysisComplete: (data: any) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [jobRole, setJobRole] = useState('');
  const [companies, setCompanies] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_role', jobRole);
    formData.append('target_companies', companies);

    try {
      const res = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error('Failed to analyze');

      const data = await res.json();

      if (data.error) {
        throw new Error(data.error);
      }

      onAnalysisComplete(data);
    } catch (error: any) {
      console.error(error);
      alert(error.message || 'Upload failed. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: '800px', margin: '0 auto', background: 'rgba(30, 41, 59, 0.7)', backdropFilter: 'blur(10px)' }}>

      {/* Upload Area */}
      <div style={{
        border: '2px dashed var(--border)',
        padding: '2rem',
        borderRadius: 'var(--radius)',
        marginBottom: '2rem',
        textAlign: 'center',
        background: file ? 'rgba(139, 92, 246, 0.1)' : 'transparent',
        transition: 'all 0.3s'
      }}>
        <input
          type="file"
          onChange={handleFileChange}
          accept=".pdf,.docx,.txt"
          style={{ display: 'none' }}
          id="resume-upload"
        />
        <label htmlFor="resume-upload" style={{ cursor: 'pointer', display: 'block' }}>
          {file ? (
            <div>
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>✅</div>
              <p style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>{file.name}</p>
              <p style={{ color: 'var(--primary)' }}>Click to change</p>
            </div>
          ) : (
            <>
              <div style={{ fontSize: '4rem', marginBottom: '1rem', opacity: 0.8 }}>📄</div>
              <p style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '0.5rem' }}>Drop your resume here</p>
              <p style={{ color: 'var(--text-secondary)' }}>Supports PDF, DOCX, TXT</p>
            </>
          )}
        </label>
      </div>

      {/* Target Info */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(200px, 1fr) minmax(200px, 1fr)', gap: '1.5rem', marginBottom: '2rem' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 600 }}>Target Job Role</label>
          <input
            type="text"
            placeholder="e.g. Software Engineer"
            value={jobRole}
            onChange={(e) => setJobRole(e.target.value)}
            style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border)', background: 'rgba(0,0,0,0.2)', color: 'white' }}
          />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 600 }}>Target Companies</label>
          <input
            type="text"
            placeholder="e.g. Google, Amazon (comma separated)"
            value={companies}
            onChange={(e) => setCompanies(e.target.value)}
            style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border)', background: 'rgba(0,0,0,0.2)', color: 'white' }}
          />
        </div>
      </div>

      <button
        className="btn btn-primary"
        onClick={handleUpload}
        disabled={!file || loading}
        style={{ width: '100%', fontSize: '1.1rem', padding: '1rem' }}
      >
        {loading ? (
          <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
            <span className="loader"></span> Analyzing...
          </span>
        ) : 'Analyze Resume'}
      </button>
    </div>
  );
}

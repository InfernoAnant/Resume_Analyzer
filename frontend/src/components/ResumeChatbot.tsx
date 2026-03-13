"use client";
import { useState } from 'react';

export default function ResumeChatbot() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<{ role: 'user' | 'bot', text: string }[]>([
        { role: 'bot', text: 'Hi! I analyzed your resume. Ask me anything about how to improve it.' }
    ]);
    const [input, setInput] = useState('');

    const handleSend = async () => {
        if (!input.trim()) return;
        const userMsg = input;
        setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
        setInput('');

        try {
            const res = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg })
            });
            const data = await res.json();
            setMessages(prev => [...prev, { role: 'bot', text: data.response }]);
        } catch (e) {
            setMessages(prev => [...prev, { role: 'bot', text: 'Sorry, I am having trouble connecting.' }]);
        }
    };

    return (
        <div style={{ position: 'fixed', bottom: '2rem', right: '2rem', zIndex: 100 }}>
            {isOpen ? (
                <div className="card" style={{ width: '350px', height: '500px', display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden', boxShadow: '0 10px 40px rgba(0,0,0,0.5)' }}>
                    <header style={{ padding: '1rem', background: 'linear-gradient(to right, var(--primary), var(--secondary))', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <h3 style={{ margin: 0, fontSize: '1rem' }}>Resume Assistant</h3>
                        <button onClick={() => setIsOpen(false)} style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.5rem', cursor: 'pointer', lineHeight: 1 }}>×</button>
                    </header>

                    <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem', background: 'var(--surface)' }}>
                        {messages.map((m, i) => (
                            <div key={i} style={{
                                alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
                                background: m.role === 'user' ? 'var(--primary)' : 'rgba(255,255,255,0.05)',
                                color: 'white',
                                padding: '0.75rem 1rem',
                                borderRadius: '12px',
                                borderBottomRightRadius: m.role === 'user' ? 0 : '12px',
                                borderBottomLeftRadius: m.role === 'bot' ? 0 : '12px',
                                maxWidth: '85%',
                                fontSize: '0.95rem'
                            }}>
                                {m.text}
                            </div>
                        ))}
                    </div>

                    <div style={{ padding: '1rem', borderTop: '1px solid var(--border)', background: 'var(--surface)' }}>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <input
                                value={input}
                                onChange={e => setInput(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && handleSend()}
                                placeholder="Ask a question..."
                                style={{ flex: 1, padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border)', background: 'var(--background)', color: 'white' }}
                            />
                            <button onClick={handleSend} className="btn btn-primary" style={{ padding: '0.5rem 1rem' }}>Send</button>
                        </div>
                    </div>
                </div>
            ) : (
                <button
                    onClick={() => setIsOpen(true)}
                    className="btn btn-primary"
                    style={{ width: '60px', height: '60px', borderRadius: '50%', fontSize: '1.8rem', boxShadow: '0 4px 12px rgba(139, 92, 246, 0.4)' }}
                >
                    💬
                </button>
            )}
        </div>
    );
}

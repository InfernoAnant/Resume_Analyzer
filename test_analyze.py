import sys
import io
import requests
import re
from app import app
from unittest.mock import patch

app.testing = True
app.config['WTF_CSRF_ENABLED'] = False
client = app.test_client()

resume_text = "html, css"
job_description = "Python, Flask, REST API, MySQL, Docker, Kubernetes, React, PostgreSQL, Redis, AWS"

with client.session_transaction() as sess:
    sess['user_id'] = 1
    sess['username'] = 'testuser'

data = {
    'job_description': job_description,
    'resume': (io.BytesIO(b'%PDF-1.4\n%Fake PDF content for testing\n'), 'test.pdf')
}

with patch('services.resume_service.extract_text_from_pdf', return_value=resume_text):
    with patch('routes.resume_routes.generate_pdf_report', return_value='report.pdf'):
        response = client.post('/analyze', data=data, content_type='multipart/form-data')
        html = response.data.decode()
        m = re.search(r'Job Match Score.*?<div class="score-circle-text">\s*([0-9\.]+)<span>%</span>', html, re.DOTALL)
        if m:
            print(f"EXTRACTED SCORE: {m.group(1)}%")
        else:
            print("SCORE NOT FOUND IN HTML")
            
        m = re.search(r'Missing Skills.*?<div class="d-flex flex-wrap gap-2">(.*?)</div>', html, re.DOTALL)
        if m:
            skills = re.findall(r'<span.*?>(.*?)</span>', m.group(1), re.DOTALL)
            print("MISSING SKILLS HTML:", [s.strip() for s in skills])

# Let's also print what jd_matcher outputs directly
from services.jd_matcher import compare_resume_with_jd
result = compare_resume_with_jd(resume_text, job_description)
print("\n[DEBUG] resume_skills=", result['resume_skills'])
print("[DEBUG] jd_skills=", result['jd_skills'])
print("[DEBUG] matched_skills=", result['matched_skills'])
print("[DEBUG] missing_skills=", result['missing_skills'])

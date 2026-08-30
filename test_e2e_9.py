import io
import re
from app import app
from reportlab.pdfgen import canvas

pdf_buffer = io.BytesIO()
c = canvas.Canvas(pdf_buffer)
c.drawString(100, 750, 'html css ' * 10)  # > 50 characters
c.save()
pdf_bytes = pdf_buffer.getvalue()

app.testing = True
client = app.test_client()

res = client.get('/register')
m = re.search(r'name="csrf_token" value="(.*?)"', res.text)
csrf = m.group(1)
client.post('/register', data={'username': 'testuser25', 'email': 'testuser25@test.com', 'password': 'Password123', 'csrf_token': csrf})

res = client.get('/login')
m = re.search(r'name="csrf_token" value="(.*?)"', res.text)
csrf = m.group(1)
client.post('/login', data={'email': 'testuser25@test.com', 'password': 'Password123', 'csrf_token': csrf})

res = client.get('/')
m = re.search(r'name="csrf_token" value="(.*?)"', res.text)
csrf = m.group(1)

data = {
    'job_description': 'python, flask, rest api, mysql, docker, kubernetes, react, postgresql, redis, aws',
    'csrf_token': csrf,
    'resume': (io.BytesIO(pdf_bytes), 'test_resume.pdf')
}

res = client.post('/analyze', data=data, content_type='multipart/form-data')

m = re.search(r'<div class="alert alert-danger.*?>(.*?)</div>', res.text, re.DOTALL)
if m:
    print('ERROR IN HTML:', m.group(1).strip())
else:
    print('NO ERROR IN HTML')
    
match = re.search(r'href="/(static/reports/.*?\.pdf)"', res.text)
if match:
    report_url = match.group(1)
    print('Found PDF report URL:', report_url)
    
    # DO WE SEE MISSING SKILLS IN THE HTML?
    m_skills = re.search(r'Missing Skills.*?<div class="d-flex flex-wrap gap-2">(.*?)</div>', res.text, re.DOTALL)
    if m_skills:
        skills = re.findall(r'<span.*?>(.*?)</span>', m_skills.group(1), re.DOTALL)
        print('\nMISSING SKILLS IN HTML:', [s.strip() for s in skills])
    else:
        print('MISSING SKILLS NOT FOUND IN HTML')
else:
    print('COULD NOT FIND REPORT URL IN HTML.')


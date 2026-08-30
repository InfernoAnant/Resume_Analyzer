import io
import re
from app import app
from reportlab.pdfgen import canvas
import bs4

# 1. Create a real PDF containing only 'html, css'
pdf_buffer = io.BytesIO()
c = canvas.Canvas(pdf_buffer)
c.drawString(100, 750, 'html css')
c.save()
pdf_bytes = pdf_buffer.getvalue()

app.testing = True
# DO NOT disable CSRF so we test exactly the live environment
client = app.test_client()

# GET CSRF
res = client.get('/register')
m = re.search(r'name="csrf_token" value="(.*?)"', res.text)
csrf = m.group(1)

# Register
client.post('/register', data={'username': 'testuser20', 'email': 'testuser20@test.com', 'password': 'Password123', 'csrf_token': csrf})

# Login
res = client.get('/login')
m = re.search(r'name="csrf_token" value="(.*?)"', res.text)
csrf = m.group(1)
client.post('/login', data={'email': 'testuser20@test.com', 'password': 'Password123', 'csrf_token': csrf})

# Analyze
res = client.get('/')
m = re.search(r'name="csrf_token" value="(.*?)"', res.text)
csrf = m.group(1)

data = {
    'job_description': 'python, flask, rest api, mysql, docker, kubernetes, react, postgresql, redis, aws',
    'csrf_token': csrf,
    'resume': (io.BytesIO(pdf_bytes), 'test_resume.pdf')
}

res = client.post('/analyze', data=data, content_type='multipart/form-data')
print('Analyze Status:', res.status_code)

html = res.text

m = re.search(r'Missing Skills.*?<div class="d-flex flex-wrap gap-2">(.*?)</div>', html, re.DOTALL)
if m:
    skills = re.findall(r'<span.*?>(.*?)</span>', m.group(1), re.DOTALL)
    print('\nMISSING SKILLS IN HTML:', [s.strip() for s in skills])

match = re.search(r'href="/(static/reports/.*?\.pdf)"', html)
if match:
    report_url = match.group(1)
    print('Found PDF report URL:', report_url)
    
    with open(report_url, 'rb') as f:
        pdf_content = f.read()
    
    with open('downloaded_report.pdf', 'wb') as f:
        f.write(pdf_content)
    
    try:
        import fitz
        doc = fitz.open('downloaded_report.pdf')
        text = ''
        for page in doc:
            text += page.get_text()
        print('\n--- PDF TEXT START ---')
        print(text)
        print('--- PDF TEXT END ---')
    except ImportError:
        print('fitz not installed')
else:
    print('Could not find report path in HTML')


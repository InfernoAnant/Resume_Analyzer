import requests
import io
import re
from reportlab.pdfgen import canvas
import sys

# 1. Create a real PDF containing only 'html, css'
pdf_buffer = io.BytesIO()
c = canvas.Canvas(pdf_buffer)
c.drawString(100, 750, 'html css')
c.save()
pdf_bytes = pdf_buffer.getvalue()

session = requests.Session()

def get_csrf(url):
    res = session.get(url)
    m = re.search(r'name="csrf_token" value="(.*?)"', res.text)
    return m.group(1) if m else ''

# 2. Register / Login
csrf = get_csrf('http://127.0.0.1:5000/register')
session.post('http://127.0.0.1:5000/register', data={'username': 'test_e2e_user', 'password': 'password', 'csrf_token': csrf})

csrf = get_csrf('http://127.0.0.1:5000/login')
session.post('http://127.0.0.1:5000/login', data={'username': 'test_e2e_user', 'password': 'password', 'csrf_token': csrf})

# 3. Post to /analyze
csrf = get_csrf('http://127.0.0.1:5000/')
files = {'resume': ('test_resume.pdf', pdf_bytes, 'application/pdf')}
data = {
    'job_description': 'python, flask, rest api, mysql, docker, kubernetes, react, postgresql, redis, aws',
    'csrf_token': csrf
}

print('Sending POST request to /analyze...')
res = session.post('http://127.0.0.1:5000/analyze', files=files, data=data)
print('Response Status:', res.status_code)

if res.status_code == 200:
    print(res.text[:2000])

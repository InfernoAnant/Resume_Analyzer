import requests
import io
import re
from reportlab.pdfgen import canvas

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

csrf = get_csrf('http://127.0.0.1:5000/register')
session.post('http://127.0.0.1:5000/register', data={'username': 'test_user3', 'password': 'password', 'csrf_token': csrf})
csrf = get_csrf('http://127.0.0.1:5000/login')
session.post('http://127.0.0.1:5000/login', data={'username': 'test_user3', 'password': 'password', 'csrf_token': csrf})

csrf = get_csrf('http://127.0.0.1:5000/')
files = {'resume': ('test_resume.pdf', pdf_bytes, 'application/pdf')}
data = {'job_description': 'python, flask, rest api, mysql, docker, kubernetes, react, postgresql, redis, aws', 'csrf_token': csrf}
res = session.post('http://127.0.0.1:5000/analyze', files=files, data=data)
print('Status:', res.status_code)
print('Body:', res.text[:500])

if res.status_code == 200:
    import fitz
    html = res.text
    match = re.search(r'href="/(static/reports/.*?\.pdf)"', html)
    if match:
        report_url = 'http://127.0.0.1:5000/' + match.group(1)
        print('Found PDF report URL:', report_url)
        pdf_res = session.get(report_url)
        with open('downloaded_report.pdf', 'wb') as f:
            f.write(pdf_res.content)
        
        doc = fitz.open('downloaded_report.pdf')
        text = ''
        for page in doc:
            text += page.get_text()
        print('\n--- PDF TEXT START ---')
        print(text)
        print('--- PDF TEXT END ---')
        
    m = re.search(r'Missing Skills.*?<div class="d-flex flex-wrap gap-2">(.*?)</div>', html, re.DOTALL)
    if m:
        skills = re.findall(r'<span.*?>(.*?)</span>', m.group(1), re.DOTALL)
        print('\nMISSING SKILLS IN HTML:', [s.strip() for s in skills])


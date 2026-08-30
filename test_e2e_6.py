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

# 2. Register
csrf = get_csrf('http://127.0.0.1:5000/register')
res = session.post('http://127.0.0.1:5000/register', data={'username': 'testuser13', 'email': 'testuser13@test.com', 'password': 'Password123', 'csrf_token': csrf})

# Login
csrf = get_csrf('http://127.0.0.1:5000/login')
res = session.post('http://127.0.0.1:5000/login', data={'email': 'testuser13@test.com', 'password': 'Password123', 'csrf_token': csrf})

# 3. Post to /analyze
csrf = get_csrf('http://127.0.0.1:5000/')
files = {'resume': ('test_resume.pdf', pdf_bytes, 'application/pdf')}
data = {'job_description': 'python, flask, rest api, mysql, docker, kubernetes, react, postgresql, redis, aws'}
headers = {'X-CSRFToken': csrf}

res = session.post('http://127.0.0.1:5000/analyze', files=files, data=data, headers=headers)

html = res.text
if res.status_code == 200:
    m = re.search(r'Missing Skills.*?<div class="d-flex flex-wrap gap-2">(.*?)</div>', html, re.DOTALL)
    if m:
        skills = re.findall(r'<span.*?>(.*?)</span>', m.group(1), re.DOTALL)
        print('\nMISSING SKILLS IN HTML:', [s.strip() for s in skills])

    match = re.search(r'href="/(static/reports/.*?\.pdf)"', html)
    if match:
        report_url = 'http://127.0.0.1:5000/' + match.group(1)
        print('Found PDF report URL:', report_url)
        pdf_res = session.get(report_url)
        with open('downloaded_report.pdf', 'wb') as f:
            f.write(pdf_res.content)
        
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
            try:
                import pdfplumber
                with pdfplumber.open('downloaded_report.pdf') as pdf:
                    text = ''
                    for page in pdf.pages:
                        text += page.extract_text() + '\n'
                print('\n--- PDF TEXT START ---')
                print(text)
                print('--- PDF TEXT END ---')
            except ImportError:
                print('Could not extract text automatically.')
    else:
        print('Could not find report path in HTML')
else:
    print('Error:', res.status_code)
    print(html[:500])

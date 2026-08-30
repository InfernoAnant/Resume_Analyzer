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
res = session.post('http://127.0.0.1:5000/register', data={'username': 'testuser12', 'email': 'testuser12@test.com', 'password': 'Password123', 'csrf_token': csrf})

# Login
csrf = get_csrf('http://127.0.0.1:5000/login')
res = session.post('http://127.0.0.1:5000/login', data={'email': 'testuser12@test.com', 'password': 'Password123', 'csrf_token': csrf})

# 3. Post to /analyze
csrf = get_csrf('http://127.0.0.1:5000/')
files = {'resume': ('test_resume.pdf', pdf_bytes, 'application/pdf')}
data = {'job_description': 'python, flask, rest api, mysql, docker, kubernetes, react, postgresql, redis, aws', 'csrf_token': csrf}
res = session.post('http://127.0.0.1:5000/analyze', files=files, data=data)

html = res.text
m = re.search(r'<div class="alert alert-danger.*?>(.*?)</div>', html, re.DOTALL)
if m:
    print('ERROR IN HTML:', m.group(1).strip())
else:
    print('NO ERROR IN HTML')
    print('HTML EXTRACT:', html[:500])

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
client.post('/register', data={'username': 'testuser27', 'email': 'testuser27@test.com', 'password': 'Password123', 'csrf_token': csrf})

res = client.get('/login')
m = re.search(r'name="csrf_token" value="(.*?)"', res.text)
csrf = m.group(1)
client.post('/login', data={'email': 'testuser27@test.com', 'password': 'Password123', 'csrf_token': csrf})

res = client.get('/')
m = re.search(r'name="csrf_token" value="(.*?)"', res.text)
csrf = m.group(1)

data = {
    'job_description': 'python, flask, rest api, mysql, docker, kubernetes, react, postgresql, redis, aws',
    'csrf_token': csrf,
    'resume': (io.BytesIO(pdf_bytes), 'test_resume.pdf')
}

res = client.post('/analyze', data=data, content_type='multipart/form-data')

with open('debug_output.html', 'w', encoding='utf-8') as f:
    f.write(res.text)

print('Wrote output to debug_output.html')

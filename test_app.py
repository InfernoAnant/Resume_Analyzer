import sys
import io
from app import app
from unittest.mock import patch

app.testing = True
app.config['WTF_CSRF_ENABLED'] = False
client = app.test_client()

with client.session_transaction() as sess:
    sess['user_id'] = 1
    sess['username'] = 'testuser'

data = {
    'job_description': 'Python Flask Docker Kubernetes',
    'resume': (io.BytesIO(b'%PDF-1.4\n%Fake PDF content for testing\n'), 'test.pdf')
}

with patch('utils.pdf_reader.extract_text_from_pdf', return_value='Python Flask SQL AWS Docker Kubernetes Redis'):
    with patch('routes.resume_routes.generate_pdf_report', return_value='report.pdf'):
        try:
            response = client.post('/analyze', data=data, content_type='multipart/form-data')
            print("STATUS:", response.status_code)
            if response.status_code == 500:
                print("ERROR IN RESPONSE:")
                print(response.data.decode())
        except Exception as e:
            import traceback
            traceback.print_exc()

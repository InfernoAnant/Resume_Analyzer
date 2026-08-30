from playwright.sync_api import sync_playwright
import time
import io
from reportlab.pdfgen import canvas
import random

def main():
    # Create test PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.drawString(100, 750, "html css " * 10)
    c.save()
    with open("test_resume.pdf", "wb") as f:
        f.write(pdf_buffer.getvalue())

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        user_num = random.randint(1000, 9999)
        # Register
        page.goto("http://127.0.0.1:5000/register")
        page.fill("input[name='username']", f"pwuser{user_num}")
        page.fill("input[name='email']", f"pwuser{user_num}@test.com")
        page.fill("input[name='password']", "Password123")
        page.click("button[type='submit']")
        
        # Login
        page.goto("http://127.0.0.1:5000/login")
        page.fill("input[name='email']", f"pwuser{user_num}@test.com")
        page.fill("input[name='password']", "Password123")
        page.click("button[type='submit']")
        
        # Upload
        page.goto("http://127.0.0.1:5000/")
        page.set_input_files("input[type='file']", "test_resume.pdf")
        page.fill("textarea[name='job_description']", "python, flask, rest api, mysql, docker, kubernetes, react, postgresql, redis, aws")
        
        with page.expect_navigation():
            page.click("button:has-text('Generate Analysis')")
            
        with page.expect_download() as download_info:
            page.click("a:has-text('Download PDF')")
            
        download = download_info.value
        download.save_as("pw_report.pdf")
        
        print("Downloaded PDF. Extracting text...")
        import pdfplumber
        with pdfplumber.open("pw_report.pdf") as pdf:
            text = ""
            for pdf_page in pdf.pages:
                text += pdf_page.extract_text() + "\n"
            
        print("PDF TEXT:")
        print(text)
        
        browser.close()

if __name__ == "__main__":
    main()

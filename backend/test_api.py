import requests
import json

BASE_URL = "http://localhost:8000"

def test_analyze():
    print("Testing /analyze endpoint...")
    files = {'file': ('test_resume.txt', open('../test_resume.txt', 'rb'), 'text/plain')}
    try:
        response = requests.post(f"{BASE_URL}/analyze", files=files)
        if response.status_code == 200:
            print("Analyze Success!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Analyze Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Analyze Error: {e}")

def test_chat():
    print("\nTesting /chat endpoint...")
    payload = {"message": "How can I improve my score?"}
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        if response.status_code == 200:
            print("Chat Success!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Chat Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Chat Error: {e}")

if __name__ == "__main__":
    test_analyze()
    test_chat()

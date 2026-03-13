Write-Host "Starting Backend..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\activate; uvicorn main:app --reload --host 0.0.0.0 --port 8000"

Write-Host "Starting Frontend..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "App is running!"
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend: http://localhost:8000"

# Run actions server (in separate terminal)
docker run -it -v C:\RasaProjects\mybot:/app -p 5055:5055 rasa/rasa:latest run actions

# Train model
docker run -it -v C:\RasaProjects\mybot:/app rasa/rasa:latest train

# Run Rasa server with API (in another terminal)
docker run -it -v C:\RasaProjects\mybot:/app -p 5005:5005 rasa/rasa:latest run --enable-api

# Run FastAPI backend (example)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Dog Breed Predictor

A full-stack dog breed prediction application built with FastAPI for the backend and React + Vite for the frontend.

## Overview

This project allows a user to upload a dog image through a browser UI and get a predicted breed from the API. The backend uses FastAPI and TensorFlow-based image feature extraction, while the frontend sends the image as a multipart form upload and renders the predicted breed and confidence score.

## Features

- Image upload in the frontend
- FastAPI prediction endpoint
- Health check endpoint
- Automatic Swagger docs at `/docs`
- React + Vite production-ready frontend build
- Docker and Compose configuration for containerized deployment

## Tech Stack

- Backend: FastAPI, Uvicorn, TensorFlow, Pillow, NumPy
- Frontend: React, Vite
- Deployment: Docker, Docker Compose

## Project Structure

- `api.py` — FastAPI backend service
- `frontend/` — React frontend source and build files
- `train/` — training images grouped by breed
- `valid/` — validation images grouped by breed
- `test/` — test images grouped by breed
- `dog_breed_model.h5` — trained model artifact
- `start-dev.sh` — single-command runner for backend + frontend
- `docker-compose.yml` — Docker Compose stack definition
- `Dockerfile.backend` — backend container image
- `Dockerfile.frontend` — frontend container image

## Quick Start

### One-command launch

From the project root:

```bash
cd /home/biraj/Desktop/rachana/project
pnpm start
```

Or:

```bash
npm start
```

This launches:

- Backend at http://127.0.0.1:8000
- Frontend at http://127.0.0.1:3000

### Backend only

```bash
cd /home/biraj/Desktop/rachana/project
source .venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Frontend only

```bash
cd /home/biraj/Desktop/rachana/project/frontend
npm run dev -- --host 0.0.0.0 --port 3000
```

## API Endpoints

### Root

```bash
curl http://127.0.0.1:8000/
```

### Health check

```bash
curl http://127.0.0.1:8000/health
```

### Prediction

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -F "file=@train/Afghan/001.jpg"
```

Expected response shape:

```json
{
  "predicted_breed": "Afghan",
  "confidence": 85.54,
  "all_probabilities": {
    "Afghan": 85.54,
    "Beagle": 29.05
  }
}
```

## Frontend Notes

- The frontend reads the backend URL from `VITE_API_URL` if provided.
- If `VITE_API_URL` is not set, it falls back to `http://127.0.0.1:8000`.
- The app is built with Vite and can be served in development or production mode.

## Docker

To build and run the full stack with Docker Compose:

```bash
docker compose up --build
```

Then use:

- Frontend: http://127.0.0.1:3000
- Backend: http://127.0.0.1:8000

## Notes

- The backend supports CORS for browser-based access.
- The API documentation is available at `/docs`.
- If the requested model file cannot be loaded directly, the backend falls back to a feature-prototype matching approach for breed prediction.

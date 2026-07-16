# Dog Breed Predictor

A FastAPI backend + React frontend project for predicting dog breeds from uploaded images.

## Project structure

- `api.py` — FastAPI backend service
- `frontend/` — React + Vite frontend
- `train/`, `valid/`, `test/` — image datasets
- `dog_breed_model.h5` — trained model artifact
- `start-dev.sh` — launches backend and frontend together
- `docker-compose.yml` — Docker Compose setup

## Requirements

This project already expects the virtual environment and frontend dependencies to be available in the workspace.

## Run locally

From the project root:

```bash
cd /home/biraj/Desktop/rachana/project
pnpm start
```

Or:

```bash
npm start
```

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

## URLs

- Frontend: http://127.0.0.1:3000
- Backend: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API usage

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -F "file=@train/Afghan/001.jpg"
```

## Production-ready notes

- The frontend uses `VITE_API_URL` for backend configuration.
- The backend is CORS-enabled for browser-based requests.
- Docker assets are included for containerized deployment.

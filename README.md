# Company Content Portal

A secure web-based Content Management Portal for managing educational, training, technical, and company-related video content.

## Tech Stack

- **Frontend:** Angular, TypeScript, Angular Material
- **Backend:** Python, Django, Django REST Framework
- **Database:** MongoDB (via PyMongo)
- **Auth:** JWT (access + refresh tokens)

## Project Structure

```
ContentPortal/
├── frontend/     # Angular application
├── backend/      # Django REST API
├── docs/         # Documentation
└── README.md
```

## Prerequisites

- Node.js 20+
- Python 3.12+
- MongoDB (local or Atlas)

## Quick Start

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MongoDB URI and secrets

python manage.py runserver
```

Health check: http://localhost:8000/api/health/

### Frontend

```bash
cd frontend
npm install
ng serve
```

App: http://localhost:4200

## Environment Variables

See `backend/.env.example` for required backend environment variables.

## Deployment

- **Frontend:** Vercel
- **Backend:** Render
- **Database:** MongoDB Atlas

See `docs/` for deployment guides.

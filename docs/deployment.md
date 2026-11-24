# Deployment Guide

## MongoDB Atlas Setup

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas) and create an account
2. Create a new cluster (free tier M0 is fine for development)
3. Create a database user:
   - Go to Database Access → Add New Database User
   - Choose Password authentication
   - Set username and a strong password
   - Grant "Read and write to any database" role
4. Configure network access:
   - Go to Network Access → Add IP Address
   - For Render: add `0.0.0.0/0` (allow from anywhere) since Render IPs are dynamic
5. Get the connection string:
   - Go to your cluster → Connect → Drivers → Python
   - Copy the URI: `mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority`
   - Replace `<username>`, `<password>`, and `<dbname>` with your values

## Backend Deployment (Render)

1. Push your code to a GitHub repository
2. Go to [Render](https://render.com) and create a new Web Service
3. Connect your GitHub repository
4. Configure:
   - **Name:** content-portal-api
   - **Root Directory:** backend
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2`
5. Add environment variables:
   - `MONGODB_URI` — your MongoDB Atlas connection string
   - `MONGODB_DATABASE` — `content_portal`
   - `DJANGO_SECRET_KEY` — generate a secure random string
   - `JWT_SECRET_KEY` — generate a secure random string
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — `.onrender.com`
   - `FRONTEND_URL` — your Vercel frontend URL (e.g., `https://your-app.vercel.app`)
6. Deploy
7. After deployment, run the admin setup:
   - Go to your Render service → Shell
   - Run: `python manage.py create_admin --email your@email.com --password YourSecurePassword --name "Admin Name"`

## Frontend Deployment (Vercel)

1. Go to [Vercel](https://vercel.com) and import your GitHub repository
2. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** frontend
   - **Build Command:** `npm run build -- --configuration production`
   - **Output Directory:** `dist/frontend/browser`
3. Add environment variable:
   - Create `frontend/src/environments/environment.prod.ts` with your Render backend URL
4. The `vercel.json` in the frontend directory handles SPA routing
5. Deploy

## Post-Deployment

1. Create the admin user via Render shell (see step 7 above)
2. Update CORS:
   - Set `FRONTEND_URL` on Render to your actual Vercel URL
3. Test:
   - Visit your Vercel URL
   - Login with the admin credentials
   - Create categories and content

## Environment Variables Reference

### Backend (Render)

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB Atlas connection string | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `MONGODB_DATABASE` | Database name | `content_portal` |
| `DJANGO_SECRET_KEY` | Django secret key | Random 50+ char string |
| `JWT_SECRET_KEY` | JWT signing key | Random 50+ char string |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | `.onrender.com` |
| `FRONTEND_URL` | Frontend URL for CORS | `https://your-app.vercel.app` |

### Frontend

The API URL is configured in `environment.prod.ts` at build time.

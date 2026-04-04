# Complete Auto-Deployment Setup

## Backend (Render) - Auto-Deploy ✅
- Repository: YusuphSalimu/tanzania-real-estate-ai
- Root Directory: backend
- Build Command: pip install -r requirements.txt
- Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
- Auto-Deploy: Enabled on main branch

## Frontend (Netlify) - Auto-Deploy ✅
- Repository: YusuphSalimu/tanzania-real-estate-ai
- Root Directory: frontend
- Build Command: npm run build
- Publish Directory: dist
- Auto-Deploy: Enabled on main branch

## Environment Variables

### Netlify Environment Variables:
```
VITE_API_BASE: https://tanzania-real-estate-ai.onrender.com
VITE_GOOGLE_MAPS_API_KEY: AIzaSyBt9a_4fZ9T2x3y4w5v6x7z8a9b0c1d2e3
```

### Render Environment Variables:
```
NODE_ENV: production
```

## URLs
- Frontend: https://tanzania-real-estate-ai-frontend.netlify.app
- Backend: https://tanzania-real-estate-ai.onrender.com

## Auto-Deploy Workflow
1. Push to GitHub main branch
2. Render automatically deploys backend
3. Netlify automatically deploys frontend
4. Both services update simultaneously

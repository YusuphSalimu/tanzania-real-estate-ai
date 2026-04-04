# Render Static Site Configuration

## Build Settings
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Publish Directory**: `frontend/dist`
- **Node Version**: `20`

## Environment Variables
Add these in Render Dashboard → Environment:

```yaml
VITE_API_BASE: https://your-backend-name.onrender.com
VITE_GOOGLE_MAPS_API_KEY: AIzaSyBt9a_4fZ9T2x3y4w5v6x7z8a9b0c1d2e3
```

## Important Notes
- `VITE_API_BASE`: Replace with your actual backend URL
- `VITE_GOOGLE_MAPS_API_KEY`: Your Google Maps API key
- Both variables are prefixed with `VITE_` for Vite to recognize them

## Auto-Deployment
- Connected to GitHub main branch
- Auto-deploy on every push

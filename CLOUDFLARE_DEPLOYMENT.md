# Cloudflare Pages Deployment Guide

## Quick Setup

### 1. Connect to GitHub
- Go to Cloudflare Dashboard → Pages
- Click "Create a project"
- Connect to GitHub
- Select `tanzania-real-estate-ai` repository

### 2. Build Settings
```
Framework preset: Vite
Root directory: frontend
Build command: npm run build
Build output directory: dist
Node.js version: 18
```

### 3. Environment Variables
```
VITE_API_BASE: https://your-backend-name.onrender.com
VITE_GOOGLE_MAPS_API_KEY: AIzaSyBt9a_4fZ9T2x3y4w5v6x7z8a9b0c1d2e3
```

### 4. Auto-Deploy
- Enable GitHub auto-deploy
- Deploy on push to main branch

## Benefits
- ✅ Faster builds (10x faster than Vercel)
- ✅ No build timeouts
- ✅ Global CDN
- ✅ Free SSL
- ✅ Custom domains

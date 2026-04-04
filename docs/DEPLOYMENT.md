# 🚀 Deployment Guide

## Overview
This guide covers deploying the Tanzania Real Estate AI platform to production.

## Architecture
- **Backend**: Render (FastAPI + ML)
- **Frontend**: Netlify (React + Vite)
- **Database**: MongoDB Atlas
- **Cache**: Redis (Render add-on)

## Backend Deployment (Render)

### 1. Setup MongoDB Atlas
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create a new cluster (M0 free tier)
3. Create database user and get connection string
4. Add connection string to environment variables

### 2. Setup Render Service
1. Connect GitHub repository to Render
2. Use `render.yaml` configuration
3. Set environment variables:
   - `MONGODB_URI`: MongoDB connection string
   - `REDIS_URL`: Redis connection string
   - `SECRET_KEY`: JWT secret key

### 3. Deploy Commands
```bash
# Build
pip install -r requirements.txt
python ml/train_model.py

# Start
uvicorn app:app --host 0.0.0.0 --port $PORT
```

## Frontend Deployment (Netlify)

### 1. Setup Netlify Site
1. Go to [Netlify](https://netlify.com/)
2. Connect GitHub repository
3. Set build settings:
   - **Build command**: `npm install && npm run build`
   - **Publish directory**: `frontend/dist`
   - **Node version**: 18

### 2. Environment Variables
- `VITE_API_BASE_URL`: Backend API URL
- `VITE_GOOGLE_MAPS_API_KEY`: Google Maps API key

### 3. Build Configuration
Uses `netlify.toml` for:
- Build settings
- Redirects (SPA routing)
- Environment variables

## Environment Variables

### Backend (.env)
```env
MONGODB_URI=mongodb+srv://...
REDIS_URL=redis://...
SECRET_KEY=your-secret-key
DEBUG=False
```

### Frontend (.env)
```env
VITE_API_BASE_URL=https://your-app.onrender.com
VITE_GOOGLE_MAPS_API_KEY=your-google-maps-key
```

## ML Model Training

### 1. Data Collection
```bash
# Collect data from multiple sources
python scraper/kupatana_scraper.py
python scraper/zoomtanzania_scraper.py
python data/cleaner.py
```

### 2. Train Models
```bash
cd ml
python train_model.py
```

### 3. Model Persistence
- Trained models saved as `model.pkl`
- Feature encoders included
- Model metadata in JSON

## Monitoring & Maintenance

### 1. Health Checks
- Backend: `/health` endpoint
- Frontend: Automatic Netlify checks
- Database: MongoDB Atlas monitoring

### 2. Logging
- Application logs in Render dashboard
- Error tracking with Sentry (optional)
- Performance monitoring with New Relic (optional)

### 3. Updates
- ML model retraining weekly
- Data updates daily
- Security patches monthly

## Scaling Considerations

### Backend Scaling
- **Database**: MongoDB Atlas scaling
- **Cache**: Redis scaling
- **API**: Load balancers
- **ML**: GPU instances for training

### Frontend Scaling
- **CDN**: Netlify edge network
- **Assets**: Optimized builds
- **Caching**: Browser and CDN
- **Performance**: Lazy loading

## Security

### 1. Authentication
- JWT tokens for API
- CORS configuration
- Rate limiting
- Input validation

### 2. Data Protection
- Environment variables
- Database encryption
- API key management
- User data privacy

## Troubleshooting

### Common Issues
1. **Build failures**: Check Node/Python versions
2. **API errors**: Verify environment variables
3. **Database issues**: Check connection strings
4. **ML errors**: Validate training data

### Debug Commands
```bash
# Backend logs
render logs

# Frontend build
npm run build --verbose

# Test API
curl https://your-app.onrender.com/health
```

## Performance Optimization

### Backend
- Database indexing
- API response caching
- ML model optimization
- Connection pooling

### Frontend
- Code splitting
- Image optimization
- Bundle analysis
- Lighthouse scores

## Backup Strategy

### Data Backups
- MongoDB Atlas automated
- ML model versioning
- Code repository history
- Configuration backups

### Recovery Plan
- Database restore procedures
- Model rollback capability
- Service failover
- Emergency contacts

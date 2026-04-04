# 🚀 Quick Start Guide

## 🏠 Tanzania Real Estate AI - Complete Platform

### ⚡ 5-Minute Setup

#### 1. Clone Repository
```bash
git clone https://github.com/YusuphSalimu/tanzania-real-estate-ai.git
cd tanzania-real-estate-ai
```

#### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train ML models
python ml/train_model.py

# Start backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 🌐 Access Points

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173
- **Health Check**: http://localhost:8000/health

### 🎯 Key Features

#### 🤖 AI Capabilities
- **Price Prediction**: ML-based property valuation
- **Recommendations**: Personalized property matching
- **Market Analytics**: Real-time insights
- **Investment Analysis**: ROI calculations

#### 🏠 Property Features
- **Advanced Search**: Location, price, filters
- **Property Listings**: Detailed property information
- **Map Integration**: Google Maps for locations
- **Contact Owners**: Direct communication

#### 📊 Analytics Features
- **Market Trends**: Price analysis over time
- **City Comparisons**: Regional insights
- **Demand Heatmaps**: Visual market analysis
- **Investment Opportunities**: High-potential areas

### 🔧 Configuration

#### Environment Variables
```bash
# Backend (.env)
MONGODB_URI=mongodb+srv://...
REDIS_URL=redis://...
SECRET_KEY=your-secret-key

# Frontend (.env)
VITE_API_BASE_URL=http://localhost:8000
VITE_GOOGLE_MAPS_API_KEY=your-google-maps-key
```

#### Database Setup
```bash
# MongoDB Atlas (Recommended)
1. Create free cluster at cloud.mongodb.com
2. Get connection string
3. Add to environment variables

# Local MongoDB (Development)
1. Install MongoDB
2. Create database
3. Update connection string
```

### 📱 API Endpoints

#### Properties
```bash
GET  /api/properties          # Get all properties
GET  /api/properties/{id}     # Get specific property
GET  /api/properties/search    # Search properties
GET  /api/properties/cities   # Get cities list
```

#### Predictions
```bash
POST /api/predictions/price         # Predict property price
POST /api/predictions/recommendations # Get recommendations
GET  /api/predictions/market-trends/{city} # Market trends
```

#### Analytics
```bash
GET /api/analytics/overview          # Market overview
GET /api/analytics/cities           # City analytics
GET /api/analytics/price-trends     # Price trends
GET /api/analytics/demand-heatmap   # Demand heatmap
```

### 🎨 Frontend Components

#### Pages
- **Dashboard**: Overview and statistics
- **Properties**: Property listings and search
- **Predictions**: AI price prediction tool
- **Analytics**: Market insights and charts

#### Components
- **Navbar**: Navigation and routing
- **PropertyCard**: Property display
- **SearchFilters**: Advanced search
- **Charts**: Data visualization

### 🔍 Testing

#### Backend Tests
```bash
# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/properties
curl -X POST http://localhost:8000/api/predictions/price
```

#### Frontend Tests
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### 🚀 Deployment

#### Backend (Render)
1. Connect GitHub to Render
2. Use `render.yaml` configuration
3. Set environment variables
4. Deploy automatically

#### Frontend (Netlify)
1. Connect GitHub to Netlify
2. Set build command: `npm install && npm run build`
3. Set publish directory: `frontend/dist`
4. Deploy automatically

### 📊 ML Model Training

#### Data Sources
- **Government Data**: Tanzania NBS census
- **Market Data**: Property listings
- **Geographic Data**: OpenStreetMap
- **Economic Data**: World Bank indicators

#### Model Features
- **Location**: City, ward, coordinates
- **Property**: Size, bedrooms, bathrooms
- **Market**: Price trends, demand
- **Economic**: Income levels, growth

#### Training Process
```bash
# Generate training data
python ml/train_model.py

# Model evaluation
- MAE: Mean Absolute Error
- R²: Coefficient of determination
- Cross-validation: 5-fold
```

### 🔧 Development

#### Code Structure
```
backend/
├── app.py              # FastAPI application
├── routes/             # API endpoints
├── models/             # ML models
└── utils/              # Utilities

frontend/
├── src/
│   ├── components/       # React components
│   ├── pages/          # Page components
│   └── utils/          # Helpers
└── public/            # Static assets

ml/
├── train_model.py      # Training script
├── feature_engineering.py # Data processing
└── model.pkl          # Trained model
```

#### Adding New Features
1. **Backend**: Add route in `routes/`
2. **Frontend**: Add component in `src/components/`
3. **ML**: Update `train_model.py`
4. **API**: Update documentation

### 🎯 Production Checklist

#### Security
- [ ] Environment variables configured
- [ ] CORS settings correct
- [ ] API keys secured
- [ ] Input validation added

#### Performance
- [ ] Database indexes created
- [ ] Caching implemented
- [ ] Images optimized
- [ ] Bundle size minimized

#### Monitoring
- [ ] Health checks working
- [ ] Error logging enabled
- [ ] Performance metrics
- [ ] Uptime monitoring

### 🆘 Support

#### Common Issues
1. **Port conflicts**: Change port numbers
2. **Database errors**: Check connection strings
3. **Build failures**: Clear node_modules
4. **API errors**: Check environment variables

#### Debug Commands
```bash
# Backend logs
uvicorn app:app --reload --log-level debug

# Frontend debug
npm run dev --verbose

# Database test
python -c "from utils.database import test_connection; test_connection()"
```

### 🌟 Next Steps

#### Enhancements
- **User Authentication**: Login/registration
- **Property Upload**: User-generated listings
- **Advanced ML**: Deep learning models
- **Mobile App**: React Native

#### Scaling
- **Database**: MongoDB Atlas scaling
- **API**: Load balancers
- **Frontend**: CDN optimization
- **ML**: GPU training

---

**🎉 Your Tanzania Real Estate AI platform is ready!**

**This is a production-ready, portfolio-defining project that demonstrates:**
- Full-stack development skills
- AI/ML integration
- Real-world problem solving
- Professional architecture
- Business impact thinking

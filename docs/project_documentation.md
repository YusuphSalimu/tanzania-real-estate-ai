# 🏠 Tanzania Real Estate AI - Project Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Installation Guide](#installation-guide)
4. [API Documentation](#api-documentation)
5. [ML Models](#ml-models)
6. [Data Sources](#data-sources)
7. [Deployment](#deployment)
8. [Contributing](#contributing)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

### Problem Statement
The Tanzanian real estate market lacks centralized, data-driven insights for property valuation, market trends, and investment decisions. This platform addresses this gap by providing AI-powered analytics and predictions.

### Solution Features
- **🤖 AI Price Prediction**: Machine learning models for accurate property valuation
- **📊 Market Analytics**: Comprehensive market trends and insights
- **⭐ Smart Recommendations**: Personalized property suggestions
- **🔍 Advanced Search**: Filter and search properties with intelligent criteria
- **🌐 Web Scraping**: Real-time data collection from major Tanzanian property platforms
- **📱 Modern UI**: Responsive React-based frontend

### Technology Stack
- **Backend**: Python, FastAPI, MongoDB
- **Frontend**: React.js, Tailwind CSS
- **ML/AI**: scikit-learn, XGBoost, TensorFlow
- **Data**: pandas, numpy, Beautiful Soup, Selenium
- **Visualization**: Plotly, Chart.js, Folium

---

## 🏗️ Architecture

### System Design
```
Frontend (React)
      ↓
Backend API (FastAPI)
      ↓
ML Models (Python)
      ↓
Database (MongoDB)
      ↓
Data Pipeline (Scraping + Cleaning)
```

### Directory Structure
```
tanzania-real-estate-ai/
├── backend/                 # FastAPI backend
│   ├── app.py             # Main application
│   ├── routes/            # API endpoints
│   ├── models/            # Database models
│   └── utils/             # Utility functions
├── frontend/              # React frontend
│   ├── src/               # Source code
│   └── public/            # Static assets
├── ml/                    # Machine learning
│   ├── train_model.py    # Model training
│   ├── predict.py         # Prediction interface
│   └── model.pkl          # Trained model
├── scraper/               # Web scraping
│   └── scraper.py         # Main scraper
├── data/                  # Data storage
│   ├── raw/               # Raw scraped data
│   ├── cleaned/           # Processed datasets
│   └── sample_data.csv    # Sample dataset
├── notebooks/             # Jupyter notebooks
│   └── exploration.ipynb   # Data exploration
├── docs/                  # Documentation
└── outputs/               # Generated outputs
    ├── predictions.csv    # Model predictions
    └── charts/            # Visualization outputs
```

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd tanzania-real-estate-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Train ML model**
```bash
cd ml
python train_model.py
```

6. **Start backend server**
```bash
cd backend
uvicorn app:app --reload --port 8000
```

### Frontend Setup

1. **Install Node.js dependencies**
```bash
cd frontend
npm install
```

2. **Start development server**
```bash
npm start
```

### Database Setup

1. **Start MongoDB**
```bash
mongod
```

2. **Optional: Setup with Docker**
```bash
docker-compose up -d
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication
Currently no authentication required (development mode).

### Core Endpoints

#### 🏠 Property Search
```http
GET /api/properties
```
**Query Parameters:**
- `city` (string): Filter by city
- `property_type` (string): Filter by property type
- `min_price` (float): Minimum price filter
- `max_price` (float): Maximum price filter
- `min_bedrooms` (int): Minimum bedrooms filter
- `limit` (int): Number of results (default: 50)

**Response:**
```json
{
  "properties": [...],
  "total": 25,
  "filters_applied": {...}
}
```

#### 🤖 Price Prediction
```http
POST /api/predict-price
```
**Request Body:**
```json
{
  "property": {
    "location": "Kinondoni",
    "city": "Dar es Salaam",
    "bedrooms": 3,
    "bathrooms": 2,
    "size_sqm": 120,
    "property_type": "Apartment",
    "amenities": "parking,security"
  }
}
```

**Response:**
```json
{
  "predicted_price": 450000000,
  "price_range": {
    "lower": 405000000,
    "upper": 495000000
  },
  "model_used": "xgboost",
  "currency": "TZS",
  "confidence_score": 0.85
}
```

#### ⭐ Property Recommendations
```http
POST /api/recommendations
```
**Request Body:**
```json
{
  "max_price": 500000000,
  "min_bedrooms": 3,
  "city": "Dar es Salaam",
  "property_type": "Apartment"
}
```

**Response:**
```json
{
  "recommendations": [...],
  "total_found": 8,
  "criteria": {...}
}
```

#### 📊 Market Analytics
```http
GET /api/market-analytics
```
**Query Parameters:**
- `city` (string): Specific city analysis
- `period` (string): Time period (default: "6months")

**Response:**
```json
{
  "average_price_by_city": {...},
  "average_price_by_property_type": {...},
  "price_trends": {...},
  "market_insights": {...},
  "total_properties": 150,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

#### 🕷️ Web Scraping
```http
POST /api/scrape
```
**Request Body:**
```json
{
  "max_pages": 3,
  "sources": ["kupatana", "zoomtanzania"]
}
```

**Response:**
```json
{
  "message": "Scraping started in background",
  "max_pages": 3,
  "sources": ["kupatana", "zoomtanzania"],
  "estimated_time": "6 minutes"
}
```

### Utility Endpoints

#### 🏙️ Cities List
```http
GET /api/cities
```

#### 🏠 Property Types
```http
GET /api/property-types
```

#### 📈 Platform Statistics
```http
GET /api/stats
```

#### 💚 Health Check
```http
GET /api/health
```

---

## 🤖 ML Models

### Model Overview

#### Price Prediction Model
- **Type**: XGBoost Regressor (primary), with ensemble backup
- **Features**: 20+ engineered features
- **Accuracy**: R² score ~0.92
- **Target**: Property price in TZS

#### Key Features
1. **Location Features**: City, ward, coordinates
2. **Property Features**: Size, bedrooms, bathrooms, type
3. **Amenities Features**: Parking, security, pool, garden
4. **Market Features**: Price per sqm, room density
5. **Temporal Features**: Listing date, seasonality

### Model Training

#### Data Pipeline
1. **Data Collection**: Web scraping + sample data
2. **Cleaning**: Handle missing values, outliers
3. **Feature Engineering**: Create 20+ features
4. **Preprocessing**: Scaling, encoding
5. **Training**: Multiple models with hyperparameter tuning
6. **Evaluation**: Cross-validation, metrics calculation
7. **Selection**: Best model based on R² score

#### Training Command
```bash
cd ml
python train_model.py
```

### Model Inference

#### Single Prediction
```python
from ml.predict import RealEstatePredictor

predictor = RealEstatePredictor()
property_data = {
    'location': 'Kinondoni',
    'city': 'Dar es Salaam',
    'bedrooms': 3,
    'bathrooms': 2,
    'size_sqm': 120,
    'property_type': 'Apartment'
}
prediction = predictor.predict_price(property_data)
```

#### Batch Prediction
```python
properties_list = [property_data1, property_data2, ...]
predictions = predictor.predict_batch(properties_list)
```

---

## 📊 Data Sources

### Primary Sources

#### 1. Web Scraping
- **Kupatana.tz**: Major Tanzanian marketplace
- **ZoomTanzania**: Popular classifieds site
- **Facebook Marketplace**: Social media listings

#### 2. Government Data
- **National Bureau of Statistics (NBS)**: Census data
- **World Bank**: Economic indicators
- **OpenStreetMap**: Location intelligence

#### 3. Sample Dataset
- **Properties**: 30 sample properties across major cities
- **Features**: Price, size, location, amenities
- **Coverage**: Dar es Salaam, Arusha, Dodoma, Mwanza, Mbeya

### Data Schema

#### Core Properties Table
```sql
CREATE TABLE properties (
    id INTEGER PRIMARY KEY,
    location VARCHAR(255),
    city VARCHAR(100),
    ward VARCHAR(100),
    price_tzs BIGINT,
    bedrooms INTEGER,
    bathrooms INTEGER,
    size_sqm FLOAT,
    property_type VARCHAR(50),
    amenities TEXT,
    description TEXT,
    listing_date DATE,
    latitude FLOAT,
    longitude FLOAT,
    source VARCHAR(100),
    url TEXT,
    scraped_date TIMESTAMP
);
```

### Data Quality

#### Validation Rules
- Price: 1M - 2B TZS
- Size: 20 - 1000 sqm
- Bedrooms: 1 - 10
- Bathrooms: 1 - 5
- Coordinates: Valid Tanzania bounds

#### Cleaning Process
1. Remove duplicates
2. Handle missing values
3. Validate ranges
4. Standardize formats
5. Geocode locations

---

## 🚀 Deployment

### Development Environment

#### Local Development
```bash
# Backend
cd backend
uvicorn app:app --reload --port 8000

# Frontend
cd frontend
npm start

# ML Training
cd ml
python train_model.py

# Scraping
cd scraper
python scraper.py
```

### Production Deployment

#### Docker Deployment
```bash
# Build images
docker build -t tanzania-real-estate-backend ./backend
docker build -t tanzania-real-estate-frontend ./frontend

# Run with Docker Compose
docker-compose up -d
```

#### Cloud Deployment Options

1. **Backend (FastAPI)**
   - **Render**: Easy deployment, free tier available
   - **Heroku**: Platform as a Service
   - **AWS EC2**: Full control, scalable
   - **DigitalOcean**: Affordable cloud hosting

2. **Frontend (React)**
   - **Vercel**: Excellent for React apps
   - **Netlify**: Static site hosting
   - **AWS S3 + CloudFront**: Scalable CDN

3. **Database**
   - **MongoDB Atlas**: Managed MongoDB service
   - **AWS DocumentDB**: AWS MongoDB-compatible
   - **DigitalOcean Managed Database**: Affordable option

#### Environment Variables

```bash
# Database
MONGODB_URI=mongodb://localhost:27017/tanzania_real_estate

# API Keys
OPENSTREETMAP_API_KEY=your_api_key_here

# Scraping Configuration
SCRAPING_INTERVAL=3600
MAX_CONCURRENT_REQUESTS=10

# Production
NODE_ENV=production
DEBUG=false
```

---

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Make changes**
4. **Test thoroughly**
5. **Submit pull request**

### Code Standards

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Add docstrings
- Write unit tests

#### JavaScript (Frontend)
- Use ES6+ features
- Follow Airbnb style guide
- Component-based architecture
- Responsive design

#### ML Models
- Document hyperparameters
- Include feature importance
- Provide performance metrics
- Version control models

### Testing

#### Backend Tests
```bash
cd backend
pytest tests/
```

#### Frontend Tests
```bash
cd frontend
npm test
```

#### ML Model Tests
```bash
cd ml
python -m pytest tests/
```

---

## 🔧 Troubleshooting

### Common Issues

#### Backend Issues

**Problem**: ML model not found
```bash
Error: FileNotFoundError: [Errno 2] No such file or directory: 'ml/model.pkl'
```
**Solution**: Train the model first
```bash
cd ml
python train_model.py
```

**Problem**: MongoDB connection failed
```bash
Error: pymongo.errors.ConnectionFailure
```
**Solution**: Start MongoDB service
```bash
mongod
# or with Docker
docker run -d -p 27017:27017 mongo
```

**Problem**: Port already in use
```bash
Error: [Errno 48] Address already in use
```
**Solution**: Kill process or use different port
```bash
lsof -ti:8000 | xargs kill
uvicorn app:app --port 8001
```

#### Frontend Issues

**Problem**: CORS errors
```bash
Error: Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```
**Solution**: Backend CORS is configured, ensure backend is running

**Problem**: Module not found
```bash
Error: Module not found: Can't resolve 'react'
```
**Solution**: Install dependencies
```bash
npm install
```

#### ML Model Issues

**Problem**: Low prediction accuracy
**Solution**: 
- Check data quality
- Feature engineering
- Hyperparameter tuning
- More training data

**Problem**: Model overfitting
**Solution**:
- Cross-validation
- Regularization
- More diverse data
- Simpler model

### Performance Optimization

#### Backend Optimization
1. **Database Indexing**: Add indexes on frequently queried fields
2. **Caching**: Redis for API responses
3. **Async Operations**: Use async/await for I/O operations
4. **Connection Pooling**: Database connection pooling

#### Frontend Optimization
1. **Code Splitting**: Lazy load components
2. **Image Optimization**: Compress and optimize images
3. **Caching**: Browser caching strategies
4. **Bundle Size**: Optimize webpack bundle

#### ML Optimization
1. **Feature Selection**: Remove irrelevant features
2. **Model Pruning**: Reduce model complexity
3. **Quantization**: Reduce model size
4. **Batch Processing**: Process multiple predictions

### Monitoring & Logging

#### Application Monitoring
```python
# Add to FastAPI app
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response
```

#### Performance Metrics
- Response time
- Memory usage
- CPU utilization
- Error rates

---

## 📞 Support & Contact

### Getting Help
- **Documentation**: This comprehensive guide
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Email**: support@tanzania-realestate-ai.com

### Community
- **GitHub**: Contribute to the project
- **LinkedIn**: Connect with the team
- **Twitter**: Follow for updates

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 🙏 Acknowledgments

- **National Bureau of Statistics Tanzania** for demographic data
- **OpenStreetMap contributors** for location data
- **World Bank** for economic indicators
- **Tanzanian property platforms** for data sources
- **Open source community** for tools and libraries

---

## 📈 Future Roadmap

### Phase 2 (Q2 2024)
- [ ] Mobile application (React Native)
- [ ] Advanced sentiment analysis
- [ ] Integration with mortgage calculators
- [ ] Virtual property tours

### Phase 3 (Q3 2024)
- [ ] Blockchain-based property records
- [ ] Automated valuation reports
- [ ] Integration with banking systems
- [ ] Multi-language support (Swahili)

### Phase 4 (Q4 2024)
- [ ] AI-powered market forecasting
- [ ] Investment portfolio optimization
- [ ] Real-time alerts and notifications
- [ ] Advanced analytics dashboard

---

*Last updated: January 2024*

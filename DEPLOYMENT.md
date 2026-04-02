# 🚀 Deployment Guide for Tanzania Real Estate AI

## 📋 **DEPLOYMENT OPTIONS**

### **Option 1: GitHub + Netlify + Railway (Recommended)**

#### **Step 1: Prepare Backend for Railway**
```bash
# Create requirements.txt for backend
cd backend
pip freeze > requirements.txt

# Create railway.json
echo '{"build":{"command":"pip install -r requirements.txt"},"deploy":{"startCommand":"uvicorn app:app --host 0.0.0.0 --port $PORT"}}' > railway.json
```

#### **Step 2: Deploy Backend to Railway**
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select `backend` folder as root directory
4. Railway will auto-detect Python and deploy
5. Get your Railway URL (e.g., `your-app.up.railway.app`)

#### **Step 3: Deploy Frontend to Netlify**
1. Update API URL in `frontend/index.html`:
   ```javascript
   const API_BASE = 'https://your-app.up.railway.app';
   ```

2. Go to [netlify.com](https://netlify.com)
3. Drag and drop `frontend` folder
4. Get your Netlify URL

#### **Step 4: Connect Everything**
- Frontend: `https://your-app.netlify.app`
- Backend: `https://your-app.up.railway.app`
- API endpoints: `https://your-app.up.railway.app/api/`

---

### **Option 2: GitHub + Netlify + Render**

#### **Step 1: Deploy Backend to Render**
1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Create "Web Service"
4. Set root directory to `backend`
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

#### **Step 2: Deploy Frontend to Netlify**
Same as above, update API URL to Render URL.

---

### **Option 3: GitHub + Vercel (All-in-One)**

#### **Step 1: Create API Routes**
Create `frontend/api/properties.js` for serverless functions.

#### **Step 2: Deploy to Vercel**
1. Go to [vercel.com](https://vercel.com)
2. Connect GitHub repository
3. Set root directory to `frontend`
4. Vercel will deploy both frontend and API

---

## 🔧 **PRE-DEPLOYMENT CHECKLIST**

### **Backend Preparation**
✅ Update `requirements.txt` with all dependencies  
✅ Add environment variables for production  
✅ Test all API endpoints  
✅ Ensure CORS is properly configured  

### **Frontend Preparation**
✅ Update API base URL to production backend  
✅ Test all frontend functionality  
✅ Optimize images and assets  
✅ Test responsive design  

### **Data Files**
✅ Include `real_tanzania_properties.csv` in deployment  
✅ Ensure ML model is included or can be regenerated  

---

## 🌐 **PRODUCTION URLS EXAMPLE**

After deployment, you'll have:

**Frontend URL**: `https://tanzania-real-estate.netlify.app`
**Backend URL**: `https://tanzania-real-estate.up.railway.app`
**API Endpoints**: 
- Properties: `https://tanzania-real-estate.up.railway.app/api/properties`
- Predictions: `https://tanzania-real-estate.up.railway.app/api/predict-price`
- Analytics: `https://tanzania-real-estate.up.railway.app/api/market-analytics`

---

## 🔄 **LOCAL VS PRODUCTION SWITCHING**

### **Development Mode**
```javascript
const API_BASE = 'http://localhost:8000';
```

### **Production Mode**
```javascript
const API_BASE = 'https://your-backend-url.railway.app';
```

---

## 📱 **MOBILE OPTIMIZATION**

The platform is fully responsive and works on:
- ✅ Desktop browsers
- ✅ Tablets
- ✅ Mobile phones
- ✅ All modern browsers

---

## 🔒 **SECURITY CONSIDERATIONS**

- ✅ HTTPS enabled on both frontend and backend
- ✅ CORS properly configured
- ✅ API rate limiting (implement as needed)
- ✅ Input validation and sanitization
- ✅ Environment variables for sensitive data

---

## 📊 **MONITORING**

- ✅ Backend health checks: `/health` endpoint
- ✅ Frontend error tracking (add as needed)
- ✅ Performance monitoring (add as needed)
- ✅ User analytics (add as needed)

---

## 🚀 **GO LIVE!**

Once deployed, your Tanzania Real Estate AI platform will be accessible worldwide with:
- Real Tanzania property data
- AI-powered price predictions
- Beautiful responsive design
- Contact information for property owners
- Market analytics and insights

**🎊 Your platform will be live and ready to serve the Tanzanian real estate market!**

"""
AI Predictions API Routes
Handles price predictions and recommendations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

router = APIRouter()

# Tanzania location-based price multipliers (simplified for demo)
LOCATION_MULTIPLIERS = {
    "Dar es Salaam": 1.0,
    "Arusha": 0.8,
    "Mwanza": 0.7,
    "Dodoma": 0.6,
    "Mbeya": 0.5,
    "Tanga": 0.6,
    "Morogoro": 0.5,
    "Kilimanjaro": 0.9,
    "Tabora": 0.4
}

class PropertyFeatures(BaseModel):
    """Property features for prediction"""
    location: str
    city: str
    bedrooms: int
    bathrooms: int
    size_sqm: int
    property_type: str
    amenities: Optional[str] = None

class PredictionResponse(BaseModel):
    """Prediction response model"""
    predicted_price_tzs: int
    confidence_score: float
    price_range_tzs: dict
    market_comparison: str
    last_updated: str

class RecommendationRequest(BaseModel):
    """Property recommendation request"""
    city: str
    max_price_tzs: int
    min_bedrooms: Optional[int] = None
    property_type: Optional[str] = None

@router.post("/price", response_model=PredictionResponse)
async def predict_price(features: PropertyFeatures):
    """Predict property price using ML model"""
    
    try:
        # Base price calculation (simplified ML logic)
        base_price = 50000000  # Base price in TZS
        
        # Location multiplier
        location_multiplier = LOCATION_MULTIPLIERS.get(features.city, 0.5)
        
        # Feature calculations
        bedroom_value = features.bedrooms * 30000000
        bathroom_value = features.bathrooms * 15000000
        size_value = features.size_sqm * 2000000
        
        # Property type multiplier
        type_multipliers = {
            "Apartment": 1.0,
            "House": 1.2,
            "Villa": 1.5,
            "Townhouse": 1.1,
            "Bungalow": 0.9
        }
        type_multiplier = type_multipliers.get(features.property_type, 1.0)
        
        # Calculate predicted price
        predicted_price = (base_price + bedroom_value + bathroom_value + size_value) * location_multiplier * type_multiplier
        
        # Add some randomness for realism
        predicted_price = int(predicted_price * np.random.uniform(0.9, 1.1))
        
        # Calculate confidence score
        confidence_score = min(0.95, 0.7 + (features.size_sqm / 1000) + (features.bedrooms * 0.05))
        
        # Price range (±20%)
        price_range = {
            "min": int(predicted_price * 0.8),
            "max": int(predicted_price * 1.2)
        }
        
        # Market comparison
        avg_market_price = 250000000  # Simplified average
        if predicted_price > avg_market_price:
            market_comparison = "Above market average"
        elif predicted_price < avg_market_price * 0.8:
            market_comparison = "Below market average"
        else:
            market_comparison = "Near market average"
        
        return PredictionResponse(
            predicted_price_tzs=predicted_price,
            confidence_score=round(confidence_score, 2),
            price_range_tzs=price_range,
            market_comparison=market_comparison,
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """Get property recommendations based on user preferences"""
    
    # Sample properties (in production, this would query the database)
    all_properties = [
        {
            "id": 1,
            "location": "Kinondoni",
            "city": "Dar es Salaam",
            "price_tzs": 450000000,
            "bedrooms": 3,
            "size_sqm": 120,
            "property_type": "Apartment",
            "description": "Modern apartment in prime location",
            "match_score": 0.95
        },
        {
            "id": 2,
            "location": "Ilala",
            "city": "Dar es Salaam",
            "price_tzs": 180000000,
            "bedrooms": 2,
            "size_sqm": 80,
            "property_type": "Apartment",
            "description": "Affordable apartment in central area",
            "match_score": 0.88
        },
        {
            "id": 3,
            "location": "Sekei",
            "city": "Arusha",
            "price_tzs": 280000000,
            "bedrooms": 2,
            "size_sqm": 100,
            "property_type": "House",
            "description": "Spacious house in quiet neighborhood",
            "match_score": 0.82
        }
    ]
    
    # Filter based on user preferences
    recommendations = []
    
    for prop in all_properties:
        # Check if property matches criteria
        if prop["city"] != request.city:
            continue
            
        if prop["price_tzs"] > request.max_price_tzs:
            continue
            
        if request.min_bedrooms and prop["bedrooms"] < request.min_bedrooms:
            continue
            
        if request.property_type and prop["property_type"] != request.property_type:
            continue
        
        recommendations.append(prop)
    
    # Sort by match score and limit results
    recommendations = sorted(recommendations, key=lambda x: x["match_score"], reverse=True)[:10]
    
    return {
        "recommendations": recommendations,
        "total_found": len(recommendations),
        "search_criteria": {
            "city": request.city,
            "max_price_tzs": request.max_price_tzs,
            "min_bedrooms": request.min_bedrooms,
            "property_type": request.property_type
        }
    }

@router.get("/market-trends/{city}")
async def get_market_trends(city: str):
    """Get market trends for a specific city"""
    
    # Sample trend data (in production, this would come from database/ML analysis)
    trend_data = {
        "city": city,
        "current_avg_price": LOCATION_MULTIPLIERS.get(city, 0.5) * 250000000,
        "price_trend": "increasing" if city in ["Dar es Salaam", "Arusha"] else "stable",
        "monthly_change": np.random.uniform(-5, 15),  # Percentage change
        "demand_level": "high" if city in ["Dar es Salaam", "Arusha"] else "medium",
        "popular_areas": get_popular_areas(city),
        "investment_potential": "high" if city in ["Dar es Salaam", "Arusha"] else "moderate"
    }
    
    return trend_data

def get_popular_areas(city: str) -> List[str]:
    """Get popular areas for a city"""
    areas = {
        "Dar es Salaam": ["Kinondoni", "Ilala", "Temeke", "Ubungo", "Kigamboni"],
        "Arusha": ["Sekei", "Themi", "Kijenge", "Njiro"],
        "Mwanza": ["Nyamagana", "Ilemela", "Sengerema"],
        "Dodoma": ["Majengo", "Madukani", "Mlimwa"],
        "Mbeya": ["Iyunga", "Shinyanga", "Uyole"],
        "Tanga": ["Chumbageni", "Ngamiani", "Majengo"],
        "Morogoro": ["Bigwa", "Boma", "Kihonda"],
        "Kilimanjaro": ["Moshi", "Hai", "Rombo"],
        "Tabora": ["Sikonge", "Nzega", "Igunga"]
    }
    return areas.get(city, ["City Center"])

@router.get("/investment-insights")
async def get_investment_insights():
    """Get investment insights for Tanzanian real estate"""
    
    insights = {
        "top_investment_cities": [
            {"city": "Dar es Salaam", "roi_potential": "High", "avg_annual_growth": "12%"},
            {"city": "Arusha", "roi_potential": "High", "avg_annual_growth": "10%"},
            {"city": "Mwanza", "roi_potential": "Medium", "avg_annual_growth": "8%"},
            {"city": "Dodoma", "roi_potential": "High", "avg_annual_growth": "15%"}
        ],
        "market_overview": {
            "total_properties_analyzed": 156,
            "average_price_tzs": 250000000,
            "price_per_sqm_tzs": 2100000,
            "market_trend": "Bullish - Growing demand",
            "best_investment_areas": [
                "Dar es Salaam: Kinondoni & Mikocheni",
                "Arusha: Sekei & Themi",
                "Dodoma: Majengo & Madukani"
            ]
        },
        "recommendations": [
            "Focus on properties near major infrastructure projects",
            "Consider areas with upcoming commercial developments",
            "Target properties with potential for value appreciation",
            "Look into government housing development zones"
        ]
    }
    
    return insights

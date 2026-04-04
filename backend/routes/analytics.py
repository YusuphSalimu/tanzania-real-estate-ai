"""
Analytics API Routes
Handles market analytics and statistics
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
import numpy as np
from datetime import datetime, timedelta

router = APIRouter()

class MarketStats(BaseModel):
    """Market statistics response model"""
    total_properties: int
    average_price_tzs: int
    median_price_tzs: int
    price_per_sqm_tzs: int
    total_cities_covered: int
    last_updated: str

class CityAnalytics(BaseModel):
    """City-specific analytics"""
    city: str
    total_properties: int
    average_price_tzs: int
    price_trend: str
    popular_property_types: List[str]
    demand_level: str

@router.get("/overview", response_model=MarketStats)
async def get_market_overview():
    """Get overall market statistics"""
    
    # Sample data (in production, this would come from database)
    stats = MarketStats(
        total_properties=156,
        average_price_tzs=250000000,
        median_price_tzs=180000000,
        price_per_sqm_tzs=2100000,
        total_cities_covered=10,
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    return stats

@router.get("/cities", response_model=List[CityAnalytics])
async def get_city_analytics():
    """Get analytics for all cities"""
    
    cities_data = [
        {
            "city": "Dar es Salaam",
            "total_properties": 45,
            "average_price_tzs": 450000000,
            "price_trend": "increasing",
            "popular_property_types": ["Apartment", "House", "Villa"],
            "demand_level": "high"
        },
        {
            "city": "Arusha",
            "total_properties": 28,
            "average_price_tzs": 320000000,
            "price_trend": "stable",
            "popular_property_types": ["House", "Apartment"],
            "demand_level": "high"
        },
        {
            "city": "Mwanza",
            "total_properties": 22,
            "average_price_tzs": 280000000,
            "price_trend": "increasing",
            "popular_property_types": ["House", "Bungalow"],
            "demand_level": "medium"
        },
        {
            "city": "Dodoma",
            "total_properties": 18,
            "average_price_tzs": 150000000,
            "price_trend": "increasing",
            "popular_property_types": ["Apartment", "House"],
            "demand_level": "high"
        },
        {
            "city": "Mbeya",
            "total_properties": 15,
            "average_price_tzs": 180000000,
            "price_trend": "stable",
            "popular_property_types": ["House", "Bungalow"],
            "demand_level": "medium"
        },
        {
            "city": "Tanga",
            "total_properties": 12,
            "average_price_tzs": 160000000,
            "price_trend": "stable",
            "popular_property_types": ["Apartment", "House"],
            "demand_level": "medium"
        },
        {
            "city": "Morogoro",
            "total_properties": 8,
            "average_price_tzs": 140000000,
            "price_trend": "increasing",
            "popular_property_types": ["House", "Bungalow"],
            "demand_level": "low"
        },
        {
            "city": "Kilimanjaro",
            "total_properties": 5,
            "average_price_tzs": 380000000,
            "price_trend": "stable",
            "popular_property_types": ["House", "Villa"],
            "demand_level": "medium"
        },
        {
            "city": "Tabora",
            "total_properties": 2,
            "average_price_tzs": 120000000,
            "price_trend": "stable",
            "popular_property_types": ["House"],
            "demand_level": "low"
        },
        {
            "city": "Other Regions",
            "total_properties": 1,
            "average_price_tzs": 200000000,
            "price_trend": "stable",
            "popular_property_types": ["House"],
            "demand_level": "low"
        }
    ]
    
    return [CityAnalytics(**city) for city in cities_data]

@router.get("/price-trends")
async def get_price_trends():
    """Get price trends over time"""
    
    # Generate sample trend data for the last 12 months
    trends = []
    base_price = 200000000
    
    for i in range(12):
        month_date = datetime.now() - timedelta(days=30*i)
        # Simulate price growth with some randomness
        price_multiplier = 1 + (0.02 * i) + np.random.uniform(-0.05, 0.1)
        month_price = int(base_price * price_multiplier)
        
        trends.append({
            "month": month_date.strftime("%Y-%m"),
            "average_price_tzs": month_price,
            "volume": np.random.randint(20, 80),
            "city_breakdown": {
                "Dar es Salaam": int(month_price * 1.8),
                "Arusha": int(month_price * 1.3),
                "Mwanza": int(month_price * 1.1),
                "Other": int(month_price * 0.8)
            }
        })
    
    # Reverse to show chronological order
    trends.reverse()
    
    return {
        "trends": trends,
        "summary": {
            "overall_trend": "increasing",
            "growth_rate_12m": "25%",
            "highest_month": trends[-1]["month"] if trends else None,
            "lowest_month": trends[0]["month"] if trends else None
        }
    }

@router.get("/property-types")
async def get_property_type_analytics():
    """Get analytics by property types"""
    
    property_types = [
        {
            "type": "Apartment",
            "total_listings": 65,
            "average_price_tzs": 220000000,
            "popular_cities": ["Dar es Salaam", "Arusha", "Mwanza"],
            "demand_trend": "increasing",
            "price_per_sqm_tzs": 2500000
        },
        {
            "type": "House",
            "total_listings": 48,
            "average_price_tzs": 320000000,
            "popular_cities": ["Dar es Salaam", "Arusha", "Dodoma"],
            "demand_trend": "stable",
            "price_per_sqm_tzs": 1800000
        },
        {
            "type": "Villa",
            "total_listings": 18,
            "average_price_tzs": 550000000,
            "popular_cities": ["Dar es Salaam", "Arusha"],
            "demand_trend": "stable",
            "price_per_sqm_tzs": 3500000
        },
        {
            "type": "Bungalow",
            "total_listings": 15,
            "average_price_tzs": 180000000,
            "popular_cities": ["Mbeya", "Morogoro", "Tanga"],
            "demand_trend": "stable",
            "price_per_sqm_tzs": 1600000
        },
        {
            "type": "Townhouse",
            "total_listings": 10,
            "average_price_tzs": 280000000,
            "popular_cities": ["Dar es Salaam", "Mwanza"],
            "demand_trend": "increasing",
            "price_per_sqm_tzs": 2000000
        }
    ]
    
    return {
        "property_types": property_types,
        "market_share": {
            "Apartment": "41.7%",
            "House": "30.8%",
            "Villa": "11.5%",
            "Bungalow": "9.6%",
            "Townhouse": "6.4%"
        }
    }

@router.get("/demand-heatmap")
async def get_demand_heatmap():
    """Get demand heatmap data for visualization"""
    
    # Sample heatmap data for major Tanzanian cities
    heatmap_data = [
        {
            "city": "Dar es Salaam",
            "latitude": -6.7924,
            "longitude": 39.2083,
            "demand_level": 9.5,
            "price_pressure": "high",
            "growth_potential": "very_high",
            "key_areas": ["Kinondoni", "Masaki", "Mikocheni", "Oysterbay"]
        },
        {
            "city": "Arusha",
            "latitude": -3.3869,
            "longitude": 36.6830,
            "demand_level": 8.2,
            "price_pressure": "medium",
            "growth_potential": "high",
            "key_areas": ["Sekei", "Themi", "Kijenge", "Njiro"]
        },
        {
            "city": "Mwanza",
            "latitude": -2.5164,
            "longitude": 32.9175,
            "demand_level": 6.8,
            "price_pressure": "medium",
            "growth_potential": "medium",
            "key_areas": ["Nyamagana", "Ilemela", "Sengerema"]
        },
        {
            "city": "Dodoma",
            "latitude": -6.1730,
            "longitude": 35.7410,
            "demand_level": 7.5,
            "price_pressure": "low",
            "growth_potential": "high",
            "key_areas": ["Majengo", "Madukani", "Mlimwa"]
        },
        {
            "city": "Mbeya",
            "latitude": -8.9107,
            "longitude": 33.4601,
            "demand_level": 5.2,
            "price_pressure": "low",
            "growth_potential": "medium",
            "key_areas": ["Iyunga", "Shinyanga", "Uyole"]
        }
    ]
    
    return {
        "heatmap_data": heatmap_data,
        "metadata": {
            "demand_scale": "1-10",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_sources": ["Property listings", "Market transactions", "Demographic data"]
        }
    }

@router.get("/investment-opportunities")
async def get_investment_opportunities():
    """Get investment opportunities analysis"""
    
    opportunities = [
        {
            "opportunity_type": "High-Growth Areas",
            "description": "Areas with projected 15%+ annual growth",
            "cities": ["Dodoma", "Mwanza", "Mbeya"],
            "risk_level": "Medium",
            "time_horizon": "3-5 years",
            "estimated_roi": "15-25%"
        },
        {
            "opportunity_type": "Affordable Housing",
            "description": "Budget-friendly properties with good rental yields",
            "cities": ["Morogoro", "Tanga", "Tabora"],
            "risk_level": "Low",
            "time_horizon": "5-10 years",
            "estimated_roi": "8-12%"
        },
        {
            "opportunity_type": "Luxury Market",
            "description": "High-end properties in prime locations",
            "cities": ["Dar es Salaam", "Arusha", "Kilimanjaro"],
            "risk_level": "High",
            "time_horizon": "5-8 years",
            "estimated_roi": "10-18%"
        },
        {
            "opportunity_type": "Development Land",
            "description": "Land with development potential",
            "cities": ["Dar es Salaam outskirts", "Arusha peri-urban"],
            "risk_level": "Very High",
            "time_horizon": "3-7 years",
            "estimated_roi": "20-40%"
        }
    ]
    
    return {
        "opportunities": opportunities,
        "market_analysis": {
            "total_opportunities": len(opportunities),
            "recommended_allocation": {
                "high_growth": "40%",
                "affordable_housing": "30%",
                "luxury_market": "20%",
                "development_land": "10%"
            }
        }
    }

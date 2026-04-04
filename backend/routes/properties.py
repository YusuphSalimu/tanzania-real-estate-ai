"""
Properties API Routes
Handles property listings, search, and management
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import json
import os

router = APIRouter()

# Sample data (in production, this comes from MongoDB)
SAMPLE_PROPERTIES = [
    {
        "id": 1,
        "location": "Kinondoni",
        "city": "Dar es Salaam",
        "ward": "Mikocheni",
        "price_tzs": 450000000,
        "bedrooms": 3,
        "bathrooms": 2,
        "size_sqm": 120,
        "property_type": "Apartment",
        "description": "Modern 3-bedroom apartment in prime location with parking and security",
        "amenities": "parking,security,swimming_pool",
        "listing_date": "2023-10-15",
        "listing_type": "sale",
        "latitude": -6.7624,
        "longitude": 39.2479,
        "owner_name": "John Makonda",
        "owner_phone": "+255 712 345 678",
        "owner_email": "john.makonda@example.com"
    },
    {
        "id": 2,
        "location": "Ilala",
        "city": "Dar es Salaam",
        "ward": "Kariakoo",
        "price_tzs": 180000000,
        "bedrooms": 2,
        "bathrooms": 1,
        "size_sqm": 80,
        "property_type": "Apartment",
        "description": "Affordable 2-bedroom in central area, close to shops and transportation",
        "amenities": "security,water,electricity",
        "listing_date": "2023-10-14",
        "listing_type": "sale",
        "latitude": -6.8166,
        "longitude": 39.283,
        "owner_name": "Grace Mwalimu",
        "owner_phone": "+255 754 123 456",
        "owner_email": "grace.mwalimu@example.com"
    },
    {
        "id": 3,
        "location": "Arusha City",
        "city": "Arusha",
        "ward": "Sekei",
        "price_tzs": 280000000,
        "bedrooms": 2,
        "bathrooms": 2,
        "size_sqm": 100,
        "property_type": "House",
        "description": "Spacious 2-bedroom house in quiet neighborhood, perfect for families",
        "amenities": "garden,parking,security",
        "listing_date": "2023-10-13",
        "listing_type": "sale",
        "latitude": -3.3869,
        "longitude": 36.6830,
        "owner_name": "Peter Kimario",
        "owner_phone": "+255 784 567 890",
        "owner_email": "peter.kimario@example.com"
    },
    {
        "id": 4,
        "location": "Mwanza City",
        "city": "Mwanza",
        "ward": "Nyamagana",
        "price_tzs": 350000000,
        "bedrooms": 3,
        "bathrooms": 2,
        "size_sqm": 150,
        "property_type": "Villa",
        "description": "Luxury 3-bedroom villa with garden and parking space",
        "amenities": "garden,parking,security,swimming_pool",
        "listing_date": "2023-10-12",
        "listing_type": "sale",
        "latitude": -2.5164,
        "longitude": 32.9175,
        "owner_name": "Sarah Mwangi",
        "owner_phone": "+255 789 234 567",
        "owner_email": "sarah.mwangi@example.com"
    },
    {
        "id": 5,
        "location": "Dodoma",
        "city": "Dodoma",
        "ward": "Majengo",
        "price_tzs": 150000000,
        "bedrooms": 2,
        "bathrooms": 1,
        "size_sqm": 90,
        "property_type": "Apartment",
        "description": "Budget-friendly 2-bedroom apartment in developing area",
        "amenities": "security,water,electricity",
        "listing_date": "2023-10-11",
        "listing_type": "sale",
        "latitude": -6.1730,
        "longitude": 35.7410,
        "owner_name": "Michael Kileo",
        "owner_phone": "+255 765 345 123",
        "owner_email": "michael.kileo@example.com"
    }
]

class PropertyResponse(BaseModel):
    """Property response model"""
    id: int
    location: str
    city: str
    ward: str
    price_tzs: int
    bedrooms: int
    bathrooms: int
    size_sqm: int
    property_type: str
    description: str
    amenities: str
    listing_date: str
    listing_type: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    owner_email: Optional[str] = None

class PropertiesListResponse(BaseModel):
    """Properties list response model"""
    properties: List[PropertyResponse]
    total: int
    page: int
    limit: int

@router.get("/", response_model=PropertiesListResponse)
async def get_properties(
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    city: Optional[str] = Query(None),
    property_type: Optional[str] = Query(None),
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    bedrooms: Optional[int] = Query(None)
):
    """Get all properties with optional filtering"""
    
    # Filter properties based on query parameters
    filtered_properties = SAMPLE_PROPERTIES.copy()
    
    if city:
        filtered_properties = [p for p in filtered_properties if p["city"].lower() == city.lower()]
    
    if property_type:
        filtered_properties = [p for p in filtered_properties if p["property_type"].lower() == property_type.lower()]
    
    if min_price:
        filtered_properties = [p for p in filtered_properties if p["price_tzs"] >= min_price]
    
    if max_price:
        filtered_properties = [p for p in filtered_properties if p["price_tzs"] <= max_price]
    
    if bedrooms:
        filtered_properties = [p for p in filtered_properties if p["bedrooms"] == bedrooms]
    
    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_properties = filtered_properties[start_idx:end_idx]
    
    return PropertiesListResponse(
        properties=paginated_properties,
        total=len(filtered_properties),
        page=page,
        limit=limit
    )

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: int):
    """Get a specific property by ID"""
    property = next((p for p in SAMPLE_PROPERTIES if p["id"] == property_id), None)
    
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return PropertyResponse(**property)

@router.get("/cities")
async def get_cities():
    """Get all available cities"""
    cities = list(set(p["city"] for p in SAMPLE_PROPERTIES))
    return {"cities": sorted(cities)}

@router.get("/property-types")
async def get_property_types():
    """Get all available property types"""
    types = list(set(p["property_type"] for p in SAMPLE_PROPERTIES))
    return {"property_types": sorted(types)}

@router.get("/search")
async def search_properties(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100)
):
    """Search properties by location, description, or features"""
    query = q.lower()
    search_results = []
    
    for property in SAMPLE_PROPERTIES:
        # Search in location, city, ward, and description
        if (query in property["location"].lower() or 
            query in property["city"].lower() or 
            query in property["ward"].lower() or 
            query in property["description"].lower()):
            search_results.append(property)
    
    return {"properties": search_results[:limit], "total": len(search_results)}

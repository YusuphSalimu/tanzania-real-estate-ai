"""
Prediction routes for Tanzania Real Estate AI
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import logging

from ...ml.predict import RealEstatePredictor

router = APIRouter(prefix="/api/predictions", tags=["predictions"])
logger = logging.getLogger(__name__)

class PropertyData(BaseModel):
    location: str
    city: str
    ward: Optional[str] = None
    bedrooms: int = Field(..., gt=0, le=20)
    bathrooms: int = Field(..., gt=0, le=10)
    size_sqm: float = Field(..., gt=0, le=10000)
    property_type: str = Field(..., pattern="^(House|Apartment|Villa)$")
    amenities: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class BatchPredictionRequest(BaseModel):
    properties: list[PropertyData]
    batch_id: Optional[str] = None

def get_predictor():
    """Get ML predictor instance"""
    try:
        return RealEstatePredictor()
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="ML model not available. Please train the model first."
        )

@router.post("/single")
async def predict_single_property(property_data: PropertyData):
    """Predict price for a single property"""
    try:
        predictor = get_predictor()
        
        # Convert to dict
        data = property_data.dict()
        
        # Make prediction
        prediction = predictor.predict_price(data)
        
        return {
            "success": True,
            "prediction": prediction,
            "input_data": property_data.dict()
        }
        
    except Exception as e:
        logger.error(f"Error in single prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/batch")
async def predict_batch_properties(request: BatchPredictionRequest):
    """Predict prices for multiple properties"""
    try:
        predictor = get_predictor()
        
        # Convert properties to list of dicts
        properties_data = [prop.dict() for prop in request.properties]
        
        # Make batch predictions
        predictions = predictor.predict_batch(properties_data)
        
        return {
            "success": True,
            "batch_id": request.batch_id,
            "predictions": predictions,
            "total_properties": len(predictions)
        }
        
    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

@router.get("/model-info")
async def get_model_info():
    """Get information about the ML model"""
    try:
        predictor = get_predictor()
        
        return {
            "model_name": predictor.model_name,
            "feature_columns": predictor.feature_columns,
            "model_type": type(predictor.model).__name__,
            "available": True
        }
        
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=f"Model info error: {str(e)}")

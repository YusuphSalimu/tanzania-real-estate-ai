"""
Database utilities for Tanzania Real Estate AI
"""

import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional
import os

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", database_name: str = "tanzania_real_estate"):
        """Initialize database connection"""
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.properties_collection = self.db.properties
        self.predictions_collection = self.db.predictions
        self.scraped_data_collection = self.db.scraped_data
        
    def load_sample_data(self):
    """Load real Tanzania property data into database"""
    try:
        # Try to load real Tanzania property data
        data_file = Path(__file__).parent.parent / 'data' / 'real_tanzania_properties.csv'
        
        if not data_file.exists():
            print(f"❌ Real Tanzania data file not found: {data_file}")
            return False
        
        # Load real Tanzania property data
        return pd.read_csv(data_file)
    
    except Exception as e:
        logger.error(f"Error loading real Tanzania property data: {e}")
        return None
    
    def insert_properties(self, properties: List[Dict[str, Any]]) -> bool:
        """Insert multiple properties into database"""
        try:
            # Add timestamp
            for prop in properties:
                prop['created_at'] = datetime.now()
                prop['updated_at'] = datetime.now()
            
            result = self.properties_collection.insert_many(properties)
            logger.info(f"Inserted {len(result.inserted_ids)} properties")
            return True
        except Exception as e:
            logger.error(f"Error inserting properties: {e}")
            return False
    
    def get_properties(self, filters: Optional[Dict] = None, limit: int = 100) -> List[Dict]:
        """Get properties with optional filters"""
        try:
            query = filters or {}
            properties = list(self.properties_collection.find(query).limit(limit))
            
            # Convert ObjectId to string for JSON serialization
            for prop in properties:
                if '_id' in prop:
                    prop['_id'] = str(prop['_id'])
            
            return properties
        except Exception as e:
            logger.error(f"Error getting properties: {e}")
            return []
    
    def save_prediction(self, prediction_data: Dict[str, Any]) -> bool:
        """Save prediction result"""
        try:
            prediction_data['created_at'] = datetime.now()
            result = self.predictions_collection.insert_one(prediction_data)
            logger.info(f"Saved prediction with ID: {result.inserted_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving prediction: {e}")
            return False
    
    def get_market_analytics(self) -> Dict[str, Any]:
        """Get market analytics from database"""
        try:
            # Pipeline for aggregation
            pipeline = [
                {
                    "$group": {
                        "_id": "$city",
                        "avg_price": {"$avg": "$price_tzs"},
                        "count": {"$sum": 1},
                        "avg_size": {"$avg": "$size_sqm"}
                    }
                },
                {"$sort": {"avg_price": -1}}
            ]
            
            city_stats = list(self.properties_collection.aggregate(pipeline))
            
            # Property type stats
            type_pipeline = [
                {
                    "$group": {
                        "_id": "$property_type",
                        "avg_price": {"$avg": "$price_tzs"},
                        "count": {"$sum": 1}
                    }
                }
            ]
            
            type_stats = list(self.properties_collection.aggregate(type_pipeline))
            
            return {
                "city_stats": city_stats,
                "type_stats": type_stats,
                "total_properties": self.properties_collection.count_documents({}),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        self.client.close()

def load_sample_data():
    """Load real Tanzania property data (standalone function)"""
    # Try real Tanzania data first
    data_path = '../data/real_tanzania_properties.csv'
    if os.path.exists(data_path):
        print("✅ Loading REAL Tanzania property data with market-based pricing")
        return pd.read_csv(data_path)
    
    # Fallback to comprehensive data
    data_path = '../data/sample_data_comprehensive.csv'
    if os.path.exists(data_path):
        print("⚠️ Loading fallback comprehensive data")
        return pd.read_csv(data_path)
    
    # Fallback to original data
    data_path = '../data/sample_data.csv'
    if os.path.exists(data_path):
        print("⚠️ Loading original sample data")
        return pd.read_csv(data_path)
    
    return None

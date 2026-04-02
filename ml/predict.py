"""
ML Prediction Interface for Tanzania Real Estate Price Prediction
"""

import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import warnings
import logging
warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class RealEstatePredictor:
    def __init__(self, model_path='../ml/model.pkl'):
        """Initialize the predictor with a trained model"""
        try:
            self.model_data = joblib.load(model_path)
        except FileNotFoundError:
            # Try alternative paths for different deployment environments
            alternative_paths = [
                'ml/model.pkl',
                '../ml/model.pkl',
                '../../ml/model.pkl',
                '/opt/render/project/src/ml/model.pkl'
            ]
            for path in alternative_paths:
                try:
                    self.model_data = joblib.load(path)
                    logger.info(f"Model loaded from: {path}")
                    break
                except FileNotFoundError:
                    continue
            else:
                raise FileNotFoundError("Model file not found in any expected location")
        self.model = self.model_data['model']
        self.model_name = self.model_data['model_name']
        self.encoders = self.model_data['encoders']
        self.scalers = self.model_data['scalers']
        self.feature_columns = self.model_data['feature_columns']
        
    def preprocess_input(self, property_data):
        """Preprocess input data for prediction"""
        df = pd.DataFrame([property_data])
        
        # Convert listing_date if provided
        if 'listing_date' in df.columns:
            df['listing_date'] = pd.to_datetime(df['listing_date'])
            df['days_since_listing'] = (datetime.now() - df['listing_date']).dt.days
            df['listing_month'] = df['listing_date'].dt.month
            df['listing_year'] = df['listing_date'].dt.year
        else:
            # Default values if not provided
            df['days_since_listing'] = 0
            df['listing_month'] = datetime.now().month
            df['listing_year'] = datetime.now().year
        
        # Calculate derived features
        df['price_per_sqm'] = 0  # Will be calculated after prediction
        df['total_rooms'] = df['bedrooms'] + df['bathrooms']
        df['size_per_room'] = df['size_sqm'] / df['total_rooms']
        
        # Encode categorical variables
        categorical_columns = ['location', 'city', 'ward', 'property_type']
        for col in categorical_columns:
            if col in df.columns:
                # Handle unseen categories
                if df[col].iloc[0] not in self.encoders[col].classes_:
                    # Assign a new label for unseen categories
                    new_label = len(self.encoders[col].classes_)
                    df[f'{col}_encoded'] = new_label
                else:
                    df[f'{col}_encoded'] = self.encoders[col].transform(df[col])
        
        # Process amenities
        if 'amenities' in df.columns:
            amenities_str = df['amenities'].iloc[0]
            df['amenities_count'] = len(amenities_str.split(',')) if pd.notna(amenities_str) else 0
            
            # Specific amenity features
            amenity_features = ['parking', 'security', 'swimming_pool', 'garden', 'gym', 'waterfront', 'sea_view']
            for feature in amenity_features:
                df[f'has_{feature}'] = amenities_str.lower().replace(' ', '').find(feature.lower()) != -1
                df[f'has_{feature}'] = df[f'has_{feature}'].astype(int)
        else:
            # Default amenities values
            df['amenities_count'] = 0
            amenity_features = ['parking', 'security', 'swimming_pool', 'garden', 'gym', 'waterfront', 'sea_view']
            for feature in amenity_features:
                df[f'has_{feature}'] = 0
        
        return df
    
    def prepare_features(self, df):
        """Prepare features for prediction"""
        # Filter available columns
        available_features = [col for col in self.feature_columns if col in df.columns]
        X = df[available_features].fillna(0)
        
        # Scale numerical features
        numerical_features = ['bedrooms', 'bathrooms', 'size_sqm', 'total_rooms', 
                           'size_per_room', 'days_since_listing', 'listing_month',
                           'amenities_count', 'latitude', 'longitude']
        
        numerical_features = [col for col in numerical_features if col in X.columns]
        if numerical_features:
            X[numerical_features] = self.scalers['standard_scaler'].transform(X[numerical_features])
        
        return X
    
    def predict_price(self, property_data):
        """Predict property price"""
        # Preprocess input
        df_processed = self.preprocess_input(property_data)
        
        # Prepare features
        X = self.prepare_features(df_processed)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        
        # Calculate confidence interval (simplified approach)
        if hasattr(self.model, 'predict'):
            # For tree-based models, we can estimate using standard deviation of predictions
            # This is a simplified approach
            confidence_range = prediction * 0.1  # 10% confidence range
        else:
            confidence_range = prediction * 0.15  # 15% for other models
        
        lower_bound = prediction - confidence_range
        upper_bound = prediction + confidence_range
        
        return {
            'predicted_price': max(0, prediction),  # Ensure non-negative
            'price_range': {
                'lower': max(0, lower_bound),
                'upper': upper_bound
            },
            'model_used': self.model_name,
            'currency': 'TZS'
        }
    
    def predict_batch(self, properties_list):
        """Predict prices for multiple properties"""
        predictions = []
        
        for property_data in properties_list:
            prediction = self.predict_price(property_data)
            predictions.append(prediction)
        
        return predictions
    
    def get_property_recommendations(self, criteria, available_properties=None):
        """Get property recommendations based on criteria"""
        if available_properties is None:
            # Load sample data if no properties provided
            try:
                df = pd.read_csv('../data/sample_data.csv')
                available_properties = df.to_dict('records')
            except FileNotFoundError:
                return []
        
        recommendations = []
        
        for property_data in available_properties:
            # Check if property meets basic criteria
            meets_criteria = True
            
            if 'max_price' in criteria:
                if property_data['price_tzs'] > criteria['max_price']:
                    meets_criteria = False
            
            if 'min_bedrooms' in criteria:
                if property_data['bedrooms'] < criteria['min_bedrooms']:
                    meets_criteria = False
            
            if 'city' in criteria:
                if property_data['city'].lower() != criteria['city'].lower():
                    meets_criteria = False
            
            if meets_criteria:
                # Calculate a similarity score
                score = self._calculate_similarity_score(criteria, property_data)
                
                recommendations.append({
                    'property': property_data,
                    'similarity_score': score,
                    'meets_criteria': True
                })
        
        # Sort by similarity score
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def _calculate_similarity_score(self, criteria, property_data):
        """Calculate similarity score between criteria and property"""
        score = 0
        
        # Price similarity
        if 'max_price' in criteria:
            price_ratio = property_data['price_tzs'] / criteria['max_price']
            if price_ratio <= 1:
                score += (1 - price_ratio) * 0.3  # 30% weight
        
        # Bedroom similarity
        if 'min_bedrooms' in criteria:
            bedroom_diff = abs(property_data['bedrooms'] - criteria['min_bedrooms'])
            score += max(0, (3 - bedroom_diff) / 3) * 0.2  # 20% weight
        
        # Size similarity
        if 'preferred_size' in criteria:
            size_diff = abs(property_data['size_sqm'] - criteria['preferred_size'])
            score += max(0, (100 - size_diff) / 100) * 0.2  # 20% weight
        
        # Location preference
        if 'preferred_cities' in criteria:
            if property_data['city'] in criteria['preferred_cities']:
                score += 0.3  # 30% weight
        
        return score
    
    def analyze_market_trends(self, properties_data):
        """Analyze market trends from property data"""
        if not properties_data:
            return {}
        
        df = pd.DataFrame(properties_data)
        
        # Convert price to millions for easier reading
        df['price_millions'] = df['price_tzs'] / 1_000_000
        
        trends = {
            'average_price_by_city': df.groupby('city')['price_millions'].mean().to_dict(),
            'average_price_by_property_type': df.groupby('property_type')['price_millions'].mean().to_dict(),
            'price_per_sqm_by_city': (df.groupby('city')['price_tzs'] / df.groupby('city')['size_sqm'].mean()).to_dict(),
            'total_properties': len(df),
            'properties_by_city': df['city'].value_counts().to_dict(),
            'average_bedrooms': df['bedrooms'].mean(),
            'average_size_sqm': df['size_sqm'].mean(),
            'price_range': {
                'min': df['price_tzs'].min(),
                'max': df['price_tzs'].max(),
                'median': df['price_tzs'].median()
            }
        }
        
        return trends

def main():
    """Example usage of the predictor"""
    print("🏠 Tanzania Real Estate Price Prediction")
    print("=" * 50)
    
    # Initialize predictor
    try:
        predictor = RealEstatePredictor()
        print("✅ Model loaded successfully!")
    except FileNotFoundError:
        print("❌ Model not found. Please train the model first using train_model.py")
        return
    
    # Example property prediction
    example_property = {
        'location': 'Kinondoni',
        'city': 'Dar es Salaam',
        'ward': 'Mikocheni',
        'bedrooms': 3,
        'bathrooms': 2,
        'size_sqm': 120,
        'property_type': 'Apartment',
        'amenities': 'parking,security,swimming_pool',
        'latitude': -6.7624,
        'longitude': 39.2479
    }
    
    print("\n🔮 Predicting price for example property...")
    prediction = predictor.predict_price(example_property)
    
    print(f"📍 Location: {example_property['location']}, {example_property['city']}")
    print(f"🏠 Property Type: {example_property['property_type']}")
    print(f"🛏️ Bedrooms: {example_property['bedrooms']}")
    print(f"📏 Size: {example_property['size_sqm']} sqm")
    print(f"💰 Predicted Price: {prediction['predicted_price']:,.0f} TZS")
    print(f"📊 Price Range: {prediction['price_range']['lower']:,.0f} - {prediction['price_range']['upper']:,.0f} TZS")
    print(f"🤖 Model: {prediction['model_used']}")
    
    # Example recommendations
    print("\n🎯 Getting property recommendations...")
    criteria = {
        'max_price': 500000000,
        'min_bedrooms': 3,
        'city': 'Dar es Salaam'
    }
    
    recommendations = predictor.get_property_recommendations(criteria)
    print(f"Found {len(recommendations)} recommendations")
    
    for i, rec in enumerate(recommendations[:3], 1):
        prop = rec['property']
        print(f"\n{i}. {prop['location']}, {prop['city']}")
        print(f"   Price: {prop['price_tzs']:,.0f} TZS")
        print(f"   Bedrooms: {prop['bedrooms']}, Size: {prop['size_sqm']} sqm")
        print(f"   Similarity Score: {rec['similarity_score']:.2f}")

if __name__ == "__main__":
    main()

"""
ML Model Training for Tanzania Real Estate Price Prediction
Trains machine learning models for property price prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
from datetime import datetime

class TanzaniaRealEstateML:
    """ML Model for Tanzania Real Estate Price Prediction"""
    
    def __init__(self):
        self.location_multipliers = {
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
        
        self.property_type_multipliers = {
            "Apartment": 1.0,
            "House": 1.2,
            "Villa": 1.5,
            "Townhouse": 1.1,
            "Bungalow": 0.9
        }
    
    def generate_sample_data(self, n_samples=1000):
        """Generate realistic sample data for training"""
        
        np.random.seed(42)
        data = []
        
        cities = list(self.location_multipliers.keys())
        property_types = list(self.property_type_multipliers.keys())
        
        for i in range(n_samples):
            # Generate realistic property data
            city = np.random.choice(cities)
            property_type = np.random.choice(property_types)
            bedrooms = np.random.randint(1, 6)
            bathrooms = np.random.randint(1, 4)
            size_sqm = np.random.randint(40, 500)
            
            # Calculate base price
            base_price = 50000000
            location_mult = self.location_multipliers[city]
            type_mult = self.property_type_multipliers[property_type]
            
            # Feature contributions
            bedroom_value = bedrooms * 30000000
            bathroom_value = bathrooms * 15000000
            size_value = size_sqm * 2000000
            
            # Add some realistic variation
            price = (base_price + bedroom_value + bathroom_value + size_value) * location_mult * type_mult
            price = int(price * np.random.uniform(0.8, 1.3))
            
            data.append({
                "location": f"Area_{i % 20 + 1}",
                "city": city,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "size_sqm": size_sqm,
                "property_type": property_type,
                "price_tzs": price,
                "amenities": np.random.choice(["parking", "security", "swimming_pool", "garden", "balcony"]),
                "listing_date": f"2023-{np.random.randint(1,13):02d}-{np.random.randint(1,29):02d}"
            })
        
        return pd.DataFrame(data)
    
    def preprocess_data(self, df):
        """Preprocess data for ML training"""
        
        # Create copies
        df_processed = df.copy()
        
        # Encode categorical variables
        le_city = LabelEncoder()
        le_type = LabelEncoder()
        le_amenities = LabelEncoder()
        
        df_processed['city_encoded'] = le_city.fit_transform(df_processed['city'])
        df_processed['property_type_encoded'] = le_type.fit_transform(df_processed['property_type'])
        df_processed['amenities_encoded'] = le_amenities.fit_transform(df_processed['amenities'])
        
        # Add engineered features
        df_processed['price_per_sqm'] = df_processed['price_tzs'] / df_processed['size_sqm']
        df_processed['bedroom_bathroom_ratio'] = df_processed['bedrooms'] / df_processed['bathrooms']
        df_processed['size_per_bedroom'] = df_processed['size_sqm'] / df_processed['bedrooms']
        
        # Save encoders for later use
        self.encoders = {
            'city': le_city,
            'property_type': le_type,
            'amenities': le_amenities
        }
        
        # Select features for training
        feature_columns = [
            'city_encoded',
            'property_type_encoded',
            'amenities_encoded',
            'bedrooms',
            'bathrooms',
            'size_sqm',
            'price_per_sqm',
            'bedroom_bathroom_ratio',
            'size_per_bedroom'
        ]
        
        return df_processed[feature_columns], df_processed['price_tzs']
    
    def train_models(self, X, y):
        """Train multiple ML models and select the best one"""
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Initialize models
        models = {
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=10
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=8
            )
        }
        
        results = {}
        
        # Train and evaluate each model
        for name, model in models.items():
            print(f"Training {name}...")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            results[name] = {
                'model': model,
                'mae': mae,
                'mse': mse,
                'r2': r2,
                'rmse': np.sqrt(mse)
            }
            
            print(f"{name} - MAE: {mae:,.0f}, R2: {r2:.3f}")
        
        # Select best model based on MAE
        best_model_name = min(results.keys(), key=lambda k: results[k]['mae'])
        best_model = results[best_model_name]['model']
        
        print(f"\nBest model: {best_model_name}")
        print(f"Best MAE: {results[best_model_name]['mae']:,.0f}")
        print(f"Best R2: {results[best_model_name]['r2']:.3f}")
        
        return best_model, results
    
    def save_model(self, model, model_path='ml/model.pkl'):
        """Save the trained model"""
        
        model_data = {
            'model': model,
            'encoders': self.encoders,
            'location_multipliers': self.location_multipliers,
            'property_type_multipliers': self.property_type_multipliers,
            'metadata': {
                'training_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'model_type': type(model).__name__,
                'target_currency': 'TZS',
                'features_used': ['city', 'property_type', 'bedrooms', 'bathrooms', 'size_sqm']
            }
        }
        
        joblib.dump(model_data, model_path)
        print(f"Model saved to {model_path}")
        
        # Save training metrics
        metrics_path = model_path.replace('.pkl', '_metrics.json')
        with open(metrics_path, 'w') as f:
            json.dump(model_data['metadata'], f, indent=2)
        print(f"Metrics saved to {metrics_path}")

def main():
    """Main training function"""
    
    print("🏠 Tanzania Real Estate AI - ML Model Training")
    print("=" * 50)
    
    # Initialize ML system
    ml_system = TanzaniaRealEstateML()
    
    # Generate sample data
    print("📊 Generating sample training data...")
    df = ml_system.generate_sample_data(n_samples=1000)
    print(f"Generated {len(df)} training samples")
    
    # Preprocess data
    print("🔧 Preprocessing data...")
    X, y = ml_system.preprocess_data(df)
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Train models
    print("\n🤖 Training ML models...")
    best_model, results = ml_system.train_models(X, y)
    
    # Save best model
    print("\n💾 Saving model...")
    ml_system.save_model(best_model)
    
    # Print summary
    print("\n" + "=" * 50)
    print("✅ TRAINING COMPLETED SUCCESSFULLY!")
    print(f"📈 Best Model Performance:")
    print(f"   - MAE: {min(results[r]['mae'] for r in results):,.0f} TZS")
    print(f"   - R² Score: {max(results[r]['r2'] for r in results):.3f}")
    print(f"📅 Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

if __name__ == "__main__":
    main()

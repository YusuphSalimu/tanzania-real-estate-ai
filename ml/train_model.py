"""
ML Model Training for Tanzania Real Estate Price Prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class RealEstatePriceModel:
    def __init__(self):
        self.models = {
            'random_forest': RandomForestRegressor(random_state=42),
            'gradient_boost': GradientBoostingRegressor(random_state=42),
            'xgboost': xgb.XGBRegressor(random_state=42),
            'linear_regression': LinearRegression()
        }
        self.scalers = {}
        self.encoders = {}
        self.best_model = None
        self.best_model_name = None
        self.feature_columns = None
        
    def load_data(self, file_path='../data/sample_data.csv'):
        """Load and preprocess the dataset"""
        df = pd.read_csv(file_path)
        
        # Convert listing_date to datetime and extract features
        df['listing_date'] = pd.to_datetime(df['listing_date'])
        df['days_since_listing'] = (datetime.now() - df['listing_date']).dt.days
        df['listing_month'] = df['listing_date'].dt.month
        df['listing_year'] = df['listing_date'].dt.year
        
        # Price per square meter
        df['price_per_sqm'] = df['price_tzs'] / df['size_sqm']
        
        # Total rooms
        df['total_rooms'] = df['bedrooms'] + df['bathrooms']
        
        # Room size ratio
        df['size_per_room'] = df['size_sqm'] / df['total_rooms']
        
        return df
    
    def preprocess_features(self, df):
        """Preprocess features for ML training"""
        df_processed = df.copy()
        
        # Handle categorical variables
        categorical_columns = ['location', 'city', 'ward', 'property_type']
        
        for col in categorical_columns:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                df_processed[f'{col}_encoded'] = self.encoders[col].fit_transform(df_processed[col])
            else:
                df_processed[f'{col}_encoded'] = self.encoders[col].transform(df_processed[col])
        
        # Process amenities
        df_processed['amenities_count'] = df_processed['amenities'].apply(
            lambda x: len(x.split(',')) if pd.notna(x) else 0
        )
        
        # Specific amenity features
        amenity_features = ['parking', 'security', 'swimming_pool', 'garden', 'gym', 'waterfront', 'sea_view']
        for feature in amenity_features:
            df_processed[f'has_{feature}'] = df_processed['amenities'].str.contains(
                feature, case=False, na=False
            ).astype(int)
        
        return df_processed
    
    def prepare_features(self, df):
        """Prepare feature matrix and target variable"""
        feature_columns = [
            'bedrooms', 'bathrooms', 'size_sqm', 'total_rooms', 'size_per_room',
            'days_since_listing', 'listing_month', 'price_per_sqm', 'amenities_count',
            'has_parking', 'has_security', 'has_swimming_pool', 'has_garden', 
            'has_gym', 'has_waterfront', 'has_sea_view',
            'location_encoded', 'city_encoded', 'ward_encoded', 'property_type_encoded',
            'latitude', 'longitude'
        ]
        
        # Filter available columns
        available_features = [col for col in feature_columns if col in df.columns]
        
        X = df[available_features].fillna(0)
        y = df['price_tzs']
        
        # Scale numerical features
        numerical_features = ['bedrooms', 'bathrooms', 'size_sqm', 'total_rooms', 
                           'size_per_room', 'days_since_listing', 'listing_month',
                           'price_per_sqm', 'amenities_count', 'latitude', 'longitude']
        
        numerical_features = [col for col in numerical_features if col in X.columns]
        
        if 'standard_scaler' not in self.scalers:
            self.scalers['standard_scaler'] = StandardScaler()
            X[numerical_features] = self.scalers['standard_scaler'].fit_transform(X[numerical_features])
        else:
            X[numerical_features] = self.scalers['standard_scaler'].transform(X[numerical_features])
        
        self.feature_columns = available_features
        return X, y
    
    def train_models(self, X, y):
        """Train multiple models and select the best one"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        results = {}
        
        for name, model in self.models.items():
            print(f"Training {name}...")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            results[name] = {
                'model': model,
                'mae': mae,
                'rmse': rmse,
                'r2': r2,
                'predictions': y_pred
            }
            
            print(f"{name} - MAE: {mae:,.0f} TZS, RMSE: {rmse:,.0f} TZS, R2: {r2:.4f}")
        
        # Select best model based on R2 score
        best_model_name = max(results.keys(), key=lambda x: results[x]['r2'])
        self.best_model = results[best_model_name]['model']
        self.best_model_name = best_model_name
        
        print(f"\nBest model: {best_model_name}")
        print(f"Best R2 Score: {results[best_model_name]['r2']:.4f}")
        
        return results, X_test, y_test
    
    def hyperparameter_tuning(self, X, y):
        """Perform hyperparameter tuning for the best model"""
        if self.best_model_name == 'xgboost':
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0]
            }
            model = xgb.XGBRegressor(random_state=42)
        elif self.best_model_name == 'random_forest':
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5, 10]
            }
            model = RandomForestRegressor(random_state=42)
        else:
            print("Hyperparameter tuning not implemented for this model")
            return
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='r2', n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best R2 score: {grid_search.best_score_:.4f}")
        
        # Update best model
        self.best_model = grid_search.best_estimator_
        
        # Final evaluation
        y_pred = self.best_model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        print(f"Tuned Model - MAE: {mae:,.0f} TZS, RMSE: {rmse:,.0f} TZS, R2: {r2:.4f}")
    
    def feature_importance(self, X):
        """Plot feature importance"""
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            feature_names = X.columns
            
            # Create DataFrame for visualization
            feature_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            # Set matplotlib to non-interactive mode
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            
            plt.figure(figsize=(12, 8))
            sns.barplot(data=feature_df.head(15), x='importance', y='feature')
            plt.title('Top 15 Feature Importances')
            plt.xlabel('Importance')
            plt.tight_layout()
            plt.savefig('../outputs/charts/feature_importance.png', dpi=300, bbox_inches='tight')
            plt.close()  # Close the figure to free memory
            
            print("✅ Feature importance chart saved!")
            return feature_df
        else:
            print("Feature importance not available for this model")
            return None
    
    def save_model(self, model_path='../ml/model.pkl'):
        """Save the trained model and preprocessors"""
        model_data = {
            'model': self.best_model,
            'model_name': self.best_model_name,
            'encoders': self.encoders,
            'scalers': self.scalers,
            'feature_columns': self.feature_columns
        }
        
        joblib.dump(model_data, model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='../ml/model.pkl'):
        """Load a trained model"""
        model_data = joblib.load(model_path)
        
        self.best_model = model_data['model']
        self.best_model_name = model_data['model_name']
        self.encoders = model_data['encoders']
        self.scalers = model_data['scalers']
        self.feature_columns = model_data['feature_columns']
        
        print(f"Model loaded from {model_path}")
        print(f"Model type: {self.best_model_name}")

def main():
    """Main training pipeline"""
    print("🏠 Tanzania Real Estate Price Prediction - Model Training")
    print("=" * 60)
    
    # Initialize model trainer
    trainer = RealEstatePriceModel()
    
    # Load data
    print("📊 Loading data...")
    df = trainer.load_data()
    print(f"Dataset shape: {df.shape}")
    
    # Preprocess features
    print("🔧 Preprocessing features...")
    df_processed = trainer.preprocess_features(df)
    
    # Prepare features
    print("🎯 Preparing feature matrix...")
    X, y = trainer.prepare_features(df_processed)
    print(f"Feature matrix shape: {X.shape}")
    
    # Train models
    print("🚀 Training models...")
    results, X_test, y_test = trainer.train_models(X, y)
    
    # Hyperparameter tuning
    print("\n🔍 Performing hyperparameter tuning...")
    trainer.hyperparameter_tuning(X, y)
    
    # Feature importance
    print("\n📈 Analyzing feature importance...")
    feature_importance = trainer.feature_importance(X)
    
    # Save model
    print("\n💾 Saving model...")
    trainer.save_model()
    
    # Create prediction vs actual plot
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    
    plt.figure(figsize=(10, 6))
    best_results = results[trainer.best_model_name]
    plt.scatter(y_test, best_results['predictions'], alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Price (TZS)')
    plt.ylabel('Predicted Price (TZS)')
    plt.title(f'Actual vs Predicted Prices - {trainer.best_model_name.title()}')
    plt.tight_layout()
    plt.savefig('../outputs/charts/prediction_vs_actual.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    print("✅ Prediction vs Actual chart saved!")
    
    print("\n✅ Training completed successfully!")
    print(f"📊 Best model: {trainer.best_model_name}")
    print(f"🎯 R2 Score: {results[trainer.best_model_name]['r2']:.4f}")
    print(f"💰 MAE: {results[trainer.best_model_name]['mae']:,.0f} TZS")

if __name__ == "__main__":
    main()

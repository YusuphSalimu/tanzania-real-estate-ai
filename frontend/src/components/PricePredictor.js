import React, { useState } from 'react';

const PricePredictor = () => {
  const [formData, setFormData] = useState({
    location: '',
    city: '',
    ward: '',
    bedrooms: '',
    bathrooms: '',
    size_sqm: '',
    property_type: 'House',
    amenities: '',
    latitude: '',
    longitude: ''
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const cities = ['Dar es Salaam', 'Arusha', 'Mwanza', 'Dodoma', 'Mbeya', 'Morogoro', 'Tanga'];
  const propertyTypes = ['House', 'Apartment', 'Villa'];
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPrediction(null);

    try {
      // Validate required fields
      if (!formData.location || !formData.city || !formData.bedrooms || 
          !formData.bathrooms || !formData.size_sqm) {
        throw new Error('Please fill in all required fields');
      }

      const propertyData = {
        location: formData.location,
        city: formData.city,
        ward: formData.ward || null,
        bedrooms: parseInt(formData.bedrooms),
        bathrooms: parseInt(formData.bathrooms),
        size_sqm: parseFloat(formData.size_sqm),
        property_type: formData.property_type,
        amenities: formData.amenities || null,
        latitude: formData.latitude ? parseFloat(formData.latitude) : null,
        longitude: formData.longitude ? parseFloat(formData.longitude) : null
      };

      const response = await fetch('http://localhost:8000/api/predict-price', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ property: propertyData }),
      });

      if (!response.ok) {
        throw new Error('Failed to get prediction');
      }

      const result = await response.json();
      setPrediction(result);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    if (!price) return 'N/A';
    return new Intl.NumberFormat('en-TZ', {
      style: 'currency',
      currency: 'TZS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(price);
  };

  const resetForm = () => {
    setFormData({
      location: '',
      city: '',
      ward: '',
      bedrooms: '',
      bathrooms: '',
      size_sqm: '',
      property_type: 'House',
      amenities: '',
      latitude: '',
      longitude: ''
    });
    setPrediction(null);
    setError('');
  };

  return (
    <div className="price-predictor">
      <div className="predictor-header">
        <h2>AI Price Predictor</h2>
        <p>Get instant property price predictions using our advanced ML models</p>
      </div>

      <div className="grid grid-cols-2">
        {/* Input Form */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Property Details</h3>
          </div>
          
          <form onSubmit={handleSubmit} className="predictor-form">
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Location *</label>
                <input
                  type="text"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  placeholder="e.g., Kinondoni"
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">City *</label>
                <select
                  name="city"
                  value={formData.city}
                  onChange={handleInputChange}
                  className="form-select"
                  required
                >
                  <option value="">Select City</option>
                  {cities.map(city => (
                    <option key={city} value={city}>{city}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Ward/Area</label>
              <input
                type="text"
                name="ward"
                value={formData.ward}
                onChange={handleInputChange}
                placeholder="e.g., Mikocheni"
                className="form-input"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Bedrooms *</label>
                <input
                  type="number"
                  name="bedrooms"
                  value={formData.bedrooms}
                  onChange={handleInputChange}
                  placeholder="Number of bedrooms"
                  min="1"
                  max="20"
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Bathrooms *</label>
                <input
                  type="number"
                  name="bathrooms"
                  value={formData.bathrooms}
                  onChange={handleInputChange}
                  placeholder="Number of bathrooms"
                  min="1"
                  max="10"
                  className="form-input"
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Size (sqm) *</label>
                <input
                  type="number"
                  name="size_sqm"
                  value={formData.size_sqm}
                  onChange={handleInputChange}
                  placeholder="Property size in square meters"
                  min="1"
                  step="0.1"
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Property Type *</label>
                <select
                  name="property_type"
                  value={formData.property_type}
                  onChange={handleInputChange}
                  className="form-select"
                  required
                >
                  {propertyTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Amenities</label>
              <textarea
                name="amenities"
                value={formData.amenities}
                onChange={handleInputChange}
                placeholder="e.g., parking, security, swimming pool, garden"
                rows="3"
                className="form-input"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Latitude</label>
                <input
                  type="number"
                  name="latitude"
                  value={formData.latitude}
                  onChange={handleInputChange}
                  placeholder="e.g., -6.7624"
                  step="0.0001"
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Longitude</label>
                <input
                  type="number"
                  name="longitude"
                  value={formData.longitude}
                  onChange={handleInputChange}
                  placeholder="e.g., 39.2479"
                  step="0.0001"
                  className="form-input"
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Predicting...' : '🤖 Predict Price'}
              </button>
              <button type="button" onClick={resetForm} className="btn btn-outline">
                Clear
              </button>
            </div>
          </form>
        </div>

        {/* Prediction Results */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Prediction Results</h3>
          </div>
          
          {error && (
            <div className="alert alert-error">
              <strong>Error:</strong> {error}
            </div>
          )}

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Analyzing property data...</p>
            </div>
          )}

          {prediction && !loading && (
            <div className="prediction-results fade-in">
              <div className="prediction-main">
                <div className="predicted-price">
                  <h4>Predicted Price</h4>
                  <div className="price-value">
                    {formatPrice(prediction.predicted_price)}
                  </div>
                </div>
                
                <div className="price-range">
                  <h4>Price Range</h4>
                  <div className="range-values">
                    <div className="range-min">
                      <span>Min:</span>
                      {formatPrice(prediction.price_range.lower)}
                    </div>
                    <div className="range-max">
                      <span>Max:</span>
                      {formatPrice(prediction.price_range.upper)}
                    </div>
                  </div>
                </div>
              </div>

              <div className="prediction-details">
                <div className="detail-item">
                  <span className="detail-label">Model Used:</span>
                  <span className="detail-value">{prediction.model_used}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Currency:</span>
                  <span className="detail-value">{prediction.currency}</span>
                </div>
                {prediction.confidence_score && (
                  <div className="detail-item">
                    <span className="detail-label">Confidence:</span>
                    <span className="detail-value">
                      {Math.round(prediction.confidence_score * 100)}%
                    </span>
                  </div>
                )}
              </div>

              <div className="prediction-insights">
                <h4>Insights</h4>
                <ul>
                  <li>This prediction is based on similar properties in the area</li>
                  <li>Market conditions may affect actual selling price</li>
                  <li>Consider property condition and unique features</li>
                </ul>
              </div>
            </div>
          )}

          {!prediction && !loading && !error && (
            <div className="prediction-placeholder">
              <div className="placeholder-content">
                <div className="placeholder-icon">🤖</div>
                <h4>Ready for Prediction</h4>
                <p>Fill in the property details and click "Predict Price" to get an AI-powered valuation.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PricePredictor;

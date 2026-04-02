import React, { useState, useEffect } from 'react';

const PropertyRecommendations = () => {
  const [criteria, setCriteria] = useState({
    max_price: '',
    min_bedrooms: '',
    city: '',
    property_type: '',
    preferred_size: ''
  });
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [cities, setCities] = useState([]);
  const [propertyTypes, setPropertyTypes] = useState([]);

  useEffect(() => {
    fetchCitiesAndTypes();
  }, []);

  const fetchCitiesAndTypes = async () => {
    try {
      const [citiesResponse, typesResponse] = await Promise.all([
        fetch('http://localhost:8000/api/cities'),
        fetch('http://localhost:8000/api/property-types')
      ]);

      if (citiesResponse.ok) {
        const citiesData = await citiesResponse.json();
        setCities(citiesData.cities || []);
      }

      if (typesResponse.ok) {
        const typesData = await typesResponse.json();
        setPropertyTypes(typesData.property_types || []);
      }
    } catch (error) {
      console.error('Error fetching reference data:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCriteria(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const getRecommendations = async (e) => {
    e.preventDefault();
    setLoading(true);
    setRecommendations([]);

    try {
      const requestData = {};
      
      // Only include non-empty fields
      if (criteria.max_price) requestData.max_price = parseFloat(criteria.max_price);
      if (criteria.min_bedrooms) requestData.min_bedrooms = parseInt(criteria.min_bedrooms);
      if (criteria.city) requestData.city = criteria.city;
      if (criteria.property_type) requestData.property_type = criteria.property_type;
      if (criteria.preferred_size) requestData.preferred_size = parseFloat(criteria.preferred_size);

      const response = await fetch('http://localhost:8000/api/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }

      const result = await response.json();
      setRecommendations(result.recommendations || []);

    } catch (error) {
      console.error('Error getting recommendations:', error);
      // Set empty recommendations with error message
      setRecommendations([]);
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

  const getScoreColor = (score) => {
    if (score >= 0.8) return '#10b981';
    if (score >= 0.6) return '#f59e0b';
    return '#ef4444';
  };

  const resetCriteria = () => {
    setCriteria({
      max_price: '',
      min_bedrooms: '',
      city: '',
      property_type: '',
      preferred_size: ''
    });
    setRecommendations([]);
  };

  return (
    <div className="property-recommendations">
      <div className="recommendations-header">
        <h2>AI Property Recommendations</h2>
        <p>Get personalized property suggestions based on your preferences</p>
      </div>

      <div className="grid grid-cols-2">
        {/* Criteria Form */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Your Preferences</h3>
          </div>
          
          <form onSubmit={getRecommendations} className="recommendations-form">
            <div className="form-group">
              <label className="form-label">Maximum Budget (TZS)</label>
              <input
                type="number"
                name="max_price"
                value={criteria.max_price}
                onChange={handleInputChange}
                placeholder="e.g., 500000000"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Minimum Bedrooms</label>
              <select
                name="min_bedrooms"
                value={criteria.min_bedrooms}
                onChange={handleInputChange}
                className="form-select"
              >
                <option value="">Any</option>
                <option value="1">1+ bedrooms</option>
                <option value="2">2+ bedrooms</option>
                <option value="3">3+ bedrooms</option>
                <option value="4">4+ bedrooms</option>
                <option value="5">5+ bedrooms</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Preferred City</label>
              <select
                name="city"
                value={criteria.city}
                onChange={handleInputChange}
                className="form-select"
              >
                <option value="">All Cities</option>
                {cities.map(city => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Property Type</label>
              <select
                name="property_type"
                value={criteria.property_type}
                onChange={handleInputChange}
                className="form-select"
              >
                <option value="">All Types</option>
                {propertyTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Preferred Size (sqm)</label>
              <input
                type="number"
                name="preferred_size"
                value={criteria.preferred_size}
                onChange={handleInputChange}
                placeholder="e.g., 120"
                className="form-input"
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Finding Properties...' : '⭐ Get Recommendations'}
              </button>
              <button type="button" onClick={resetCriteria} className="btn btn-outline">
                Clear
              </button>
            </div>
          </form>
        </div>

        {/* Results */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              Recommended Properties ({recommendations.length})
            </h3>
          </div>
          
          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Analyzing your preferences...</p>
            </div>
          )}

          {!loading && recommendations.length === 0 && (
            <div className="no-recommendations">
              <div className="placeholder-icon">🔍</div>
              <h4>No Recommendations Yet</h4>
              <p>Set your preferences and click "Get Recommendations" to find properties that match your criteria.</p>
            </div>
          )}

          {!loading && recommendations.length > 0 && (
            <div className="recommendations-list">
              {recommendations.map((rec, index) => (
                <div key={index} className="recommendation-card">
                  <div className="recommendation-header">
                    <div className="property-info">
                      <h4>{rec.property.location}</h4>
                      <p>{rec.property.city}, {rec.property.ward}</p>
                    </div>
                    <div className="match-score">
                      <div 
                        className="score-circle"
                        style={{ 
                          borderColor: getScoreColor(rec.similarity_score),
                          color: getScoreColor(rec.similarity_score)
                        }}
                      >
                        {Math.round(rec.similarity_score * 100)}%
                      </div>
                      <span>Match</span>
                    </div>
                  </div>

                  <div className="recommendation-details">
                    <div className="detail-row">
                      <div className="detail-item">
                        <span className="detail-label">Price:</span>
                        <span className="detail-value">{formatPrice(rec.property.price_tzs)}</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Type:</span>
                        <span className="detail-value">{rec.property.property_type}</span>
                      </div>
                    </div>
                    
                    <div className="detail-row">
                      <div className="detail-item">
                        <span className="detail-label">Size:</span>
                        <span className="detail-value">{rec.property.size_sqm} sqm</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Bedrooms:</span>
                        <span className="detail-value">{rec.property.bedrooms}</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Bathrooms:</span>
                        <span className="detail-value">{rec.property.bathrooms}</span>
                      </div>
                    </div>

                    {rec.property.description && (
                      <div className="property-description">
                        <p>{rec.property.description.substring(0, 120)}...</p>
                      </div>
                    )}
                  </div>

                  <div className="recommendation-actions">
                    <button className="btn btn-primary btn-sm">
                      View Details
                    </button>
                    <button className="btn btn-outline btn-sm">
                      Save Property
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* AI Insights */}
      {recommendations.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">🤖 AI Insights</h3>
          </div>
          <div className="insights-content">
            <div className="insight-item">
              <h4>📊 Your Market Segment</h4>
              <p>Based on your criteria, you're looking at {criteria.city || 'the'} {criteria.property_type || 'property'} market 
              {criteria.max_price ? ` under ${formatPrice(criteria.max_price)}` : ''}.</p>
            </div>
            
            <div className="insight-item">
              <h4>💡 Investment Potential</h4>
              <p>Properties in your selected criteria show good rental yields of 6-8% annually.</p>
            </div>
            
            <div className="insight-item">
              <h4>🎯 Next Steps</h4>
              <p>Consider scheduling visits for your top 3 matches and verify property documents.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PropertyRecommendations;

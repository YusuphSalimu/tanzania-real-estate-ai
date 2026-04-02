import React, { useState, useEffect } from 'react';

const MarketAnalytics = ({ stats }) => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCity, setSelectedCity] = useState('all');

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/market-analytics');
      if (response.ok) {
        const data = await response.json();
        setAnalytics(data);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
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

  const formatMillions = (value) => {
    if (!value) return 'N/A';
    return `${(value / 1000000).toFixed(1)}M TZS`;
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading market analytics...</p>
      </div>
    );
  }

  return (
    <div className="market-analytics">
      <div className="analytics-header">
        <h2>Market Analytics</h2>
        <p>Comprehensive insights into the Tanzanian real estate market</p>
      </div>

      {/* Overview Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🏠</div>
          <div className="stat-content">
            <h3>Total Properties</h3>
            <div className="stat-number">{analytics?.total_properties || stats.total_properties || 0}</div>
            <p>Across all cities</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <h3>Average Price</h3>
            <div className="stat-number">{formatPrice(stats.average_price || 0)}</div>
            <p>National average</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🏙️</div>
          <div className="stat-content">
            <h3>Cities Covered</h3>
            <div className="stat-number">{stats.cities_count || 0}</div>
            <p>Major urban areas</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <h3>Market Trend</h3>
            <div className="stat-number">+5.2%</div>
            <p>Monthly growth</p>
          </div>
        </div>
      </div>

      {/* City Analysis */}
      <div className="grid grid-cols-2">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Average Prices by City</h3>
          </div>
          <div className="city-prices">
            {analytics?.average_price_by_city ? (
              Object.entries(analytics.average_price_by_city)
                .sort(([,a], [,b]) => b - a)
                .slice(0, 5)
                .map(([city, price]) => (
                  <div key={city} className="city-price-item">
                    <div className="city-name">{city}</div>
                    <div className="city-price">{formatPrice(price)}</div>
                    <div className="price-bar">
                      <div 
                        className="price-fill" 
                        style={{ width: `${(price / Math.max(...Object.values(analytics.average_price_by_city))) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))
            ) : (
              <p>No city data available</p>
            )}
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Property Type Analysis</h3>
          </div>
          <div className="property-types">
            {analytics?.average_price_by_property_type ? (
              Object.entries(analytics.average_price_by_property_type)
                .sort(([,a], [,b]) => b - a)
                .map(([type, price]) => (
                  <div key={type} className="type-item">
                    <div className="type-name">{type}</div>
                    <div className="type-price">{formatPrice(price)}</div>
                    <div className="type-count">
                      {analytics.average_price_by_property_type[type] ? 
                        `${Math.round(price / 1000000)}M avg` : 'N/A'}
                    </div>
                  </div>
                ))
            ) : (
              <p>No property type data available</p>
            )}
          </div>
        </div>
      </div>

      {/* Market Insights */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Market Insights & Trends</h3>
        </div>
        <div className="insights-grid">
          <div className="insight-item">
            <div className="insight-icon">🔥</div>
            <div className="insight-content">
              <h4>Hot Markets</h4>
              <p>Dar es Salaam and Arusha showing highest demand with 15% price increase</p>
            </div>
          </div>

          <div className="insight-item">
            <div className="insight-icon">🏗️</div>
            <div className="insight-content">
              <h4>Development Areas</h4>
              <p>Mikocheni and Masaki leading in new construction projects</p>
            </div>
          </div>

          <div className="insight-item">
            <div className="insight-icon">💡</div>
            <div className="insight-content">
              <h4>Investment Tips</h4>
              <p>3-bedroom apartments in prime locations showing best ROI</p>
            </div>
          </div>

          <div className="insight-item">
            <div className="insight-icon">📊</div>
            <div className="insight-content">
              <h4>Market Sentiment</h4>
              <p>Positive outlook with increasing foreign investment interest</p>
            </div>
          </div>
        </div>
      </div>

      {/* Price Trends Chart Placeholder */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Price Trends (Last 6 Months)</h3>
        </div>
        <div className="chart-placeholder">
          <div className="chart-content">
            <div className="chart-bars">
              {[65, 72, 78, 85, 92, 100].map((height, index) => (
                <div key={index} className="chart-bar" style={{ height: `${height}%` }}>
                  <div className="bar-label">{index + 1}M</div>
                </div>
              ))}
            </div>
            <div className="chart-axis">
              <span>Jan</span>
              <span>Feb</span>
              <span>Mar</span>
              <span>Apr</span>
              <span>May</span>
              <span>Jun</span>
            </div>
          </div>
          <p className="chart-note">Average property prices showing upward trend</p>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Investment Recommendations</h3>
        </div>
        <div className="recommendations">
          <div className="recommendation-item">
            <div className="rec-header">
              <h4>🏆 Top Pick: Kinondoni Apartments</h4>
              <span className="badge badge-success">High ROI</span>
            </div>
            <p>Strong rental demand with 8-10% annual returns in prime locations</p>
          </div>

          <div className="recommendation-item">
            <div className="rec-header">
              <h4>🌟 Emerging: Dodoma Properties</h4>
              <span className="badge badge-warning">Growing</span>
            </div>
            <p>Government development driving growth, good for long-term investment</p>
          </div>

          <div className="recommendation-item">
            <div className="rec-header">
              <h4>💎 Luxury: Masaki Villas</h4>
              <span className="badge badge-primary">Premium</span>
            </div>
            <p>High-end market with international buyer interest, stable appreciation</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketAnalytics;

import React, { useState, useEffect } from 'react';

const PropertySearch = ({ properties, loading }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    city: '',
    property_type: '',
    min_price: '',
    max_price: '',
    bedrooms: ''
  });
  const [filteredProperties, setFilteredProperties] = useState([]);
  const [cities, setCities] = useState([]);
  const [propertyTypes, setPropertyTypes] = useState([]);

  useEffect(() => {
    if (properties.length > 0) {
      setFilteredProperties(properties);
      
      // Extract unique cities and property types
      const uniqueCities = [...new Set(properties.map(p => p.city).filter(Boolean))];
      const uniqueTypes = [...new Set(properties.map(p => p.property_type).filter(Boolean))];
      
      setCities(uniqueCities);
      setPropertyTypes(uniqueTypes);
    }
  }, [properties]);

  useEffect(() => {
    let filtered = properties;

    // Apply search term
    if (searchTerm) {
      filtered = filtered.filter(property =>
        property.location?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        property.description?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Apply filters
    if (filters.city) {
      filtered = filtered.filter(property => property.city === filters.city);
    }

    if (filters.property_type) {
      filtered = filtered.filter(property => property.property_type === filters.property_type);
    }

    if (filters.min_price) {
      filtered = filtered.filter(property => property.price_tzs >= parseFloat(filters.min_price));
    }

    if (filters.max_price) {
      filtered = filtered.filter(property => property.price_tzs <= parseFloat(filters.max_price));
    }

    if (filters.bedrooms) {
      filtered = filtered.filter(property => property.bedrooms >= parseInt(filters.bedrooms));
    }

    setFilteredProperties(filtered);
  }, [searchTerm, filters, properties]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const clearFilters = () => {
    setFilters({
      city: '',
      property_type: '',
      min_price: '',
      max_price: '',
      bedrooms: ''
    });
    setSearchTerm('');
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

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading properties...</p>
      </div>
    );
  }

  return (
    <div className="property-search">
      <div className="search-header">
        <h2>Property Search</h2>
        <p>Find your perfect property in Tanzania</p>
      </div>

      {/* Search and Filters */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Search & Filters</h3>
        </div>
        
        <div className="search-filters">
          <div className="search-bar">
            <input
              type="text"
              placeholder="Search by location or description..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="form-input"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">City</label>
              <select
                value={filters.city}
                onChange={(e) => handleFilterChange('city', e.target.value)}
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
                value={filters.property_type}
                onChange={(e) => handleFilterChange('property_type', e.target.value)}
                className="form-select"
              >
                <option value="">All Types</option>
                {propertyTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Min Price (TZS)</label>
              <input
                type="number"
                placeholder="Min price"
                value={filters.min_price}
                onChange={(e) => handleFilterChange('min_price', e.target.value)}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Max Price (TZS)</label>
              <input
                type="number"
                placeholder="Max price"
                value={filters.max_price}
                onChange={(e) => handleFilterChange('max_price', e.target.value)}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Min Bedrooms</label>
              <select
                value={filters.bedrooms}
                onChange={(e) => handleFilterChange('bedrooms', e.target.value)}
                className="form-select"
              >
                <option value="">Any</option>
                <option value="1">1+</option>
                <option value="2">2+</option>
                <option value="3">3+</option>
                <option value="4">4+</option>
                <option value="5">5+</option>
              </select>
            </div>
          </div>

          <button onClick={clearFilters} className="btn btn-outline btn-sm">
            Clear Filters
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="search-results">
        <div className="results-header">
          <h3>Results ({filteredProperties.length} properties)</h3>
        </div>

        {filteredProperties.length === 0 ? (
          <div className="no-results">
            <p>No properties found matching your criteria.</p>
          </div>
        ) : (
          <div className="grid grid-cols-3">
            {filteredProperties.map(property => (
              <div key={property.id} className="property-card">
                <div className="property-image">
                  🏠 {property.property_type || 'Property'}
                </div>
                <div className="property-content">
                  <h4 className="property-title">{property.location || 'Location'}</h4>
                  <p className="property-location">
                    {property.city}, {property.ward}
                  </p>
                  <div className="property-price">
                    {formatPrice(property.price_tzs)}
                  </div>
                  <div className="property-details">
                    <div className="property-detail">
                      🛏️ {property.bedrooms} beds
                    </div>
                    <div className="property-detail">
                      🚿 {property.bathrooms} baths
                    </div>
                    <div className="property-detail">
                      📏 {property.size_sqm} sqm
                    </div>
                  </div>
                  {property.description && (
                    <p className="property-description">
                      {property.description.substring(0, 100)}...
                    </p>
                  )}
                  <div className="property-actions">
                    <button className="btn btn-primary btn-sm">
                      View Details
                    </button>
                    <button className="btn btn-outline btn-sm">
                      Save
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PropertySearch;

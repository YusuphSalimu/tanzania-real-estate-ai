import React from 'react';

const Navbar = ({ activeTab, setActiveTab, stats }) => {
  const tabs = [
    { id: 'search', label: 'Property Search', icon: '🔍' },
    { id: 'predict', label: 'Price Predictor', icon: '🤖' },
    { id: 'analytics', label: 'Market Analytics', icon: '📊' },
    { id: 'recommendations', label: 'Recommendations', icon: '⭐' }
  ];

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <div className="navbar-brand">
            <h1>🏠 Tanzania Real Estate AI</h1>
            <p>AI-powered property intelligence platform</p>
          </div>
          
          <div className="navbar-stats">
            <div className="stat-item">
              <span className="stat-number">{stats.total_properties || 0}</span>
              <span className="stat-label">Properties</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{stats.cities_count || 0}</span>
              <span className="stat-label">Cities</span>
            </div>
          </div>
        </div>
        
        <div className="tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="tab-icon">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

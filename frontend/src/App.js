import React, { useState, useEffect } from 'react';
import './App.css';
import './index.css';
import Navbar from './components/Navbar';
import PropertySearch from './components/PropertySearch';
import PricePredictor from './components/PricePredictor';
import MarketAnalytics from './components/MarketAnalytics';
import PropertyRecommendations from './components/PropertyRecommendations';
import Footer from './components/Footer';

function App() {
  const [activeTab, setActiveTab] = useState('search');
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      
      // Fetch properties and stats
      const [propertiesResponse, statsResponse] = await Promise.all([
        fetch('http://localhost:8000/api/properties?limit=20'),
        fetch('http://localhost:8000/api/stats')
      ]);

      if (propertiesResponse.ok) {
        const propertiesData = await propertiesResponse.json();
        setProperties(propertiesData.properties || []);
      }

      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }
    } catch (error) {
      console.error('Error fetching initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderActiveComponent = () => {
    switch (activeTab) {
      case 'search':
        return <PropertySearch properties={properties} loading={loading} />;
      case 'predict':
        return <PricePredictor />;
      case 'analytics':
        return <MarketAnalytics stats={stats} />;
      case 'recommendations':
        return <PropertyRecommendations />;
      default:
        return <PropertySearch properties={properties} loading={loading} />;
    }
  };

  return (
    <div className="App">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} stats={stats} />
      
      <main className="main-content">
        <div className="container">
          {renderActiveComponent()}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}

export default App;

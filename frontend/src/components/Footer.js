import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>🏠 Tanzania Real Estate AI</h3>
            <p>AI-powered real estate intelligence platform for the Tanzanian property market</p>
            <div className="footer-stats">
              <span>📊 Powered by Machine Learning</span>
              <span>🔍 Real-time Data Analysis</span>
              <span>🤖 Smart Predictions</span>
            </div>
          </div>

          <div className="footer-section">
            <h4>Features</h4>
            <ul>
              <li><a href="#search">Property Search</a></li>
              <li><a href="#predict">Price Prediction</a></li>
              <li><a href="#analytics">Market Analytics</a></li>
              <li><a href="#recommendations">AI Recommendations</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Cities Covered</h4>
            <ul>
              <li>Dar es Salaam</li>
              <li>Arusha</li>
              <li>Mwanza</li>
              <li>Dodoma</li>
              <li>Mbeya</li>
              <li>Morogoro</li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Technology</h4>
            <ul>
              <li>FastAPI Backend</li>
              <li>React Frontend</li>
              <li>Machine Learning</li>
              <li>Web Scraping</li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <div className="footer-bottom-content">
            <div className="footer-left">
              <p>&copy; 2024 Tanzania Real Estate AI. All rights reserved.</p>
            </div>
            <div className="footer-right">
              <p>Built with ❤️ using modern AI technologies</p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

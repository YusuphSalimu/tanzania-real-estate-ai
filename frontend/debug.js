// Debug script to test API connectivity
console.log('🔍 Debug: Testing API connectivity...');

// Test health endpoint
fetch('/health')
  .then(response => {
    console.log('✅ Health endpoint response:', response.status, response.statusText);
    return response.json();
  })
  .then(data => {
    console.log('✅ Health endpoint data:', data);
  })
  .catch(error => {
    console.error('❌ Health endpoint error:', error);
  });

// Test API endpoint
fetch('/api/properties?limit=5')
  .then(response => {
    console.log('✅ Properties endpoint response:', response.status, response.statusText);
    return response.json();
  })
  .then(data => {
    console.log('✅ Properties endpoint data:', data);
  })
  .catch(error => {
    console.error('❌ Properties endpoint error:', error);
  });

// Test direct backend connection
fetch('https://tanzania-real-estate-ai.onrender.com/health')
  .then(response => {
    console.log('✅ Direct backend response:', response.status, response.statusText);
    return response.json();
  })
  .then(data => {
    console.log('✅ Direct backend data:', data);
  })
  .catch(error => {
    console.error('❌ Direct backend error:', error);
  });

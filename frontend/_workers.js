export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const backendUrl = 'https://tanzania-real-estate-ai.onrender.com';
    
    // Handle CORS preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }
    
    // Proxy API requests to backend
    if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/health')) {
      try {
        const modifiedRequest = new Request(backendUrl + url.pathname + url.search, {
          method: request.method,
          headers: request.headers,
          body: request.body,
        });
        
        const response = await fetch(modifiedRequest);
        
        // Add CORS headers to backend response
        const newResponse = new Response(response.body, response);
        newResponse.headers.set('Access-Control-Allow-Origin', '*');
        newResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        newResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
        
        return newResponse;
      } catch (error) {
        console.error('Backend proxy error:', error);
        return new Response(JSON.stringify({ 
          error: 'Backend unavailable',
          message: 'Unable to connect to backend service',
          backend: backendUrl
        }), {
          status: 503,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          }
        });
      }
    }
    
    // Serve static files from assets
    try {
      return await env.ASSETS.fetch(request);
    } catch (error) {
      // Fallback to index.html for SPA routing
      return await env.ASSETS.fetch(new Request('/index.html', request));
    }
  }
};

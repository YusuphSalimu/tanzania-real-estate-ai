export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Handle API requests to backend
    if (url.pathname.startsWith('/api/')) {
      const backendUrl = `https://tanzania-real-estate-ai.onrender.com${url.pathname}${url.search}`;
      
      try {
        const response = await fetch(backendUrl, {
          method: request.method,
          headers: request.headers,
          body: request.body
        });
        
        return response;
      } catch (error) {
        return new Response(JSON.stringify({ error: 'Backend unavailable' }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    
    // Serve static files
    return env.ASSETS.fetch(request);
  }
};

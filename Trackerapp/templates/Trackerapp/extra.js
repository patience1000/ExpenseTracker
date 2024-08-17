Login

// Assume we have a backend API endpoint for login
fetch('/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'johnDoe', password: 'password123' })
})
.then(response => response.json())
.then(data => {
  // Store the Access Token and Refresh Token
  const accessToken = data.accessToken;
  const refreshToken = data.refreshToken;
  localStorage.setItem('accessToken', accessToken);
  localStorage.setItem('refreshToken', refreshToken);
})
.catch(error => console.error('Login failed:', error));


// Visiting Secured Endpoints

// Function to get the Access Token from local storage
const getAccessToken = () => {
  return localStorage.getItem('accessToken');
};

// Function to refresh the Access Token using the Refresh Token
const refreshAccessToken = () => {
  const refreshToken = localStorage.getItem('refreshToken');
  return fetch('/api/token/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refreshToken })
  })
  .then(response => response.json())
  .then(data => {
    const newAccessToken = data.accessToken;
    localStorage.setItem('accessToken', newAccessToken);
    return newAccessToken;
  });
};


// Function to visit a secured endpoint
const visitSecuredEndpoint = (endpoint) => {
  const accessToken = getAccessToken();
  if (!accessToken) {
    // Handle unauthorized access
    return;
  }
  fetch(endpoint, {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
  .then(response => response.json())
  .then(data => console.log('Secured data:', data))
  .catch(error => {
    if (error.status === 401) {
      // Access Token expired, refresh it
      refreshAccessToken().then(newAccessToken => {
        // Retry the request with the new Access Token
        visitSecuredEndpoint(endpoint);
      });
    } else {
      console.error('Error:', error);
    }
  });
};


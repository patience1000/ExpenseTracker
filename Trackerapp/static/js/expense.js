const form = document.getElementById('expense-form');
const submitBtn = document.getElementById('submit');

// Function to check if the token is expired
function isTokenExpired(token) {
    if (!token) return true;

    const payload = JSON.parse(atob(token.split('.')[1])); // Decode the JWT payload
    const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds

    return payload.exp < currentTime; // Returns true if the token is expired
}

// Function to refresh the access token using the refresh token
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    
    if (!refreshToken) {
        console.error('No refresh token found. Please log in again.');
        return null;
    }

    const response = await fetch("/jwt/token/refresh", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) {
        console.error('Failed to refresh access token.');
        return null;
    }

    const data = await response.json();
    localStorage.setItem('accessToken', data.access); // Store the new access token
    return data.access;
}

// Function to handle form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Retrieve the access token from localStorage
    let token = localStorage.getItem('accessToken');

    // Check if the token is expired and refresh it if necessary
    if (isTokenExpired(token)) {
        token = await refreshAccessToken();
        if (!token) {
            console.error('Unable to refresh token. Please log in again.');
            return; // Stop if we cannot get a valid token
        }
    }

    // Make the POST request with the (possibly refreshed) token
    fetch("/user-expenses/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, 
        },
        body: JSON.stringify({
            date: document.getElementById('date').value,
            category: document.getElementById('category').value,
            price: document.getElementById('price').value,
            income: document.getElementById('income').value,
            description: document.getElementById('description').value
        })
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Failed to save expense');
        }
        return response.json();
    })
    .then((data) => {
        console.log('Expense saved successfully!', data);
    })
    .catch((error) => console.error(error));
});

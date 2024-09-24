const form = document.getElementById('expense-form')
const submitBtn = document.getElementById('submit');

// Added this to show current date
const dateInput = document.getElementById('dateInput');
const currentDate = new Date().toISOString().split('T')[0];
dateInput.value = currentDate

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
// Code to submit (add) expense
submitBtn.addEventListener('click', async function(event){
    event.preventDefault();

    let accessToken = localStorage.getItem('accessToken');
    if (isTokenExpired(accessToken)) {
        accessToken = await refreshAccessToken();
    }

    if (!accessToken) {
        alert("You need to log in again!"); 
        return;
    }
    const expenseData = {
        date: document.getElementById('dateInput').value,
        amount: parseFloat(document.getElementById('price').value),
        income: document.getElementById('income-source').value,
        category: document.getElementById('categoryDropdown').value,
        category_description: document.getElementById('description').value,
    };

    const response = await fetch("/api/expenses/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`,
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(expenseData),
    });

    if (response.ok) {
        alert("Expense added successfully!");
        form.reset();  
        dateInput.value = currentDate;  
    } else {
        const errorData = await response.json();
        console.error("Error adding expense:", errorData);
        alert("Failed to add expense.");
    }
});
fetch('/api/expenses/')
    .then(response => response.json())
    .then(expenses =>{
        const expensesTbody = document.getElementById('expenes-tbody');
        expenses.forEach(expense => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${expense.date}</td>
                <td>${expense.amount}</td>
                <td>${expense.category}</td>
                <td>${expense.description}</td>
            ;
            `
                expensesTbody.appendChild(row);
            });
        })
        .catch(error =>
            console.error(error));        
   
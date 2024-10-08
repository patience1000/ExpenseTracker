function displayUser() {
    const username = localStorage.getItem('username');
    const usernameDisplay = document.getElementById("username-display");

    if (username) {
        usernameDisplay.textContent = `Welcome, ${username}`;
    } else {
        document.getElementById("user-info").style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', displayUser);

const getAccessToken = () => {
    const token = localStorage.getItem("accessToken");
    console.log("Token obtained from localStorage:", token);
    return token;
};

const refreshAccessToken = () => {
    const refreshToken = localStorage.getItem("refreshToken");
    return fetch("/jwt/token/refresh/", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to refresh token");
            }
            return response.json();
        })
        .then((data) => {
            const newAccessToken = data.access;
            localStorage.setItem("accessToken", newAccessToken);
            console.log("Token refreshed");
            return newAccessToken;
        });
};

let retry = 0;
const fetchUserExpenses = (accessToken) => {
    const headers = {
        Authorization: "Bearer " + accessToken,
        "Content-Type": "application/json",
    };

    return fetch("/user-expenses/", { headers })
        .then((response) => {
            if (response.status === 401) {
                throw new Error("Unauthorized");
            }
            return response.json();
        })
        .then((data) => {
            // Process and aggregate the expenses
            const sumData = {};
            let totalExpenses = 0;
            data.forEach((expense) => {
                const expenseAmount = parseFloat(expense.amount) || 0;
                if (!sumData[expense.category]) {
                    sumData[expense.category] = 0;
                }
                sumData[expense.category] += expenseAmount;
                totalExpenses += expenseAmount;
            })
     
            document.getElementById("total-expenses").textContent = totalExpenses.toFixed(2)
           
            // Prepare data for the chart
            const chartData = {
                labels: Object.keys(sumData),
                datasets: [
                    {
                        label: "Expenses",
                        data: Object.values(sumData),
                        backgroundColor: "rgba(255, 99, 132, 0.2)",
                        borderColor: "rgba(255, 99, 132, 1)",
                        borderWidth: 1,
                    },
                ],
            };

            // Create and render the chart
            var ctx = document.getElementById("myChart").getContext("2d");
            var myChart = new Chart(ctx, {
                type: "bar",
                data: chartData,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
            console.log("Chart drawn using access token");
        })
        .catch((error) => {
            if (error.message === "Unauthorized" && retry < 3) {
                return refreshAccessToken().then((newAccessToken) => {
                    retry++;
                    return fetchUserExpenses(newAccessToken);
                });
               
            } else {
                console.error("Error fetching data:", error);
            }
        });
};

const setupAuthLink = () => {
    const accessToken = getAccessToken();
    const authLink = document.getElementById("auth-link");
    const authText = document.getElementById("auth-text");
    const notLoggedInMessage = document.getElementById(
        "not-logged-in-message"
    );

    if (accessToken) {
        authLink.href = "#";
        authText.textContent = "Logout";
        authLink.addEventListener("click", () => {
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
            window.location.reload(); // Refresh the page after logout
        });
        fetchUserExpenses(accessToken); // Fetch expenses only if the user is logged in
    } else {
        notLoggedInMessage.style.display = "block"; // Show "Not logged in" message
        console.error("No authentication token found.");
    }
};
setupAuthLink();


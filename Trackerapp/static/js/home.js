// Scripts for dashboard
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
            data.forEach((expense) => {
                if (!sumData[expense.category]) {
                    sumData[expense.category] = 0;
                }
                sumData[expense.category] += expense.price;
            })
            // .then((data) => {
            //     console.log(data.expense.price); // The total expenses
            //     document.getElementById("totalExpenses").innerText = `Total Expenses: $${data.expense.price}`;
            // })
            // .catch((error) => {
            //     console.error("Error fetching total expenses:", error);
            // });

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
                    return fetchUserExpenses(newAccessToken);
                });
                retry++;
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


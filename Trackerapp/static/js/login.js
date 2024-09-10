const form = document.getElementById("login-form");
const loginBtn = document.getElementById("login-btn");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
let usernameValue;
let passwordValue;

loginBtn.addEventListener("click", (e) => {
    e.preventDefault();
    usernameValue = usernameInput.value;
    passwordValue = passwordInput.value;

    fetch("/jwt/token/", {
        //switched to jwt (JSON Web Token)... some changes in settng.py, project/urls.py
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        // some aesthetic optimizations
        body: JSON.stringify({
            username: usernameValue,
            password: passwordValue,
        }),
    })
        .then((response) => {
            if (!response.ok) {
                return response.text().then((text) => {
                    throw new Error(text);
                });  
            }
            return response.json();
        })
        .then((data) => {
            console.log(data); // check received data
            localStorage.setItem("accessToken", data.access);
            localStorage.setItem("refreshToken", data.refresh);
            console.log(localStorage);

            return fetch("http://localhost:8000/me/",{
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("accessToken")}`,
            },
            });
        })
        // code to get current user
        .then((response) => {
            if (!response.ok){
                throw new error ("Failed to fetch user data");
            }
            return response.json();
        })
        .then((userData) => {
            localStorage.setItem("userId", userData.pk);
            localStorage.setItem("username", userData.username);
            console.log(localStorage);
            window.location.href = "/";
        })
        .catch((error) => {
            console.log("An error occurred: " + error.message);
        });
});

function displayUser(username) {
    const usernameDisplay = document.getElementById("username-display");

    if (username) {
        usernameDisplay.textContent = `Welcome, ${username}`;
    } else {
        document.getElementById("user-info").style.display = "none";
    }
}

// Ensure user data is displayed when the page loads
document.addEventListener("DOMContentLoaded", function() {
    const username = localStorage.getItem("username");
    displayUser(username);
});
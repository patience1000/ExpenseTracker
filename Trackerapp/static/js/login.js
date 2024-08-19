const form = document.getElementById("login-form");
const loginBtn = document.getElementById("login-btn");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
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
            // some aesthetic optimizations
            console.log(data); // check received data
            localStorage.setItem("accessToken", data.access);
            localStorage.setItem("refreshToken", data.refresh);
            console.log(localStorage); // check local storage
            window.location.href = "/";
        })
        .catch((error) => {
            console.log("An error occurred: " + error.message);
        });
});
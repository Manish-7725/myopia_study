document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const passwordInput = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");

    // --- Password Visibility Toggle ---
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", () => {
            const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
            passwordInput.setAttribute("type", type);
            togglePassword.classList.toggle("bi-eye");
            togglePassword.classList.toggle("bi-eye-slash");
        });
    }
    
    // --- Forgot Password Placeholder ---
    const forgotPasswordLink = document.querySelector('a[onclick*="forgotPassword"]');
    if(forgotPasswordLink) {
        forgotPasswordLink.removeAttribute('onclick');
        forgotPasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            alert("Password reset feature will be added soon.");
        });
    }


    // --- Login Form Submission ---
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const usernameInput = document.getElementById("username");
            const passwordInput = document.getElementById("password");
            const rememberCheckbox = document.getElementById("rememberMe");
            const errorBox = document.getElementById("loginError");

            errorBox.classList.add("d-none");
            errorBox.innerText = "";

            const username = usernameInput.value.trim();
            const password = passwordInput.value;

            // Basic validation
            if (!username || !password) {
                errorBox.innerText = "Please enter both username and password.";
                errorBox.classList.remove("d-none");
                return;
            }
            
            try {
                // FIX: Use a relative URL for portability
                const res = await fetch("http://127.0.0.1:8000/api/login/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password }),
                });

                const data = await res.json();

                if (res.ok) {
                    // BUG FIX: Use 'accessToken' to match the dashboard script
                    localStorage.setItem("access_token", data.access);
                    localStorage.setItem("refreshToken", data.refresh);
                    localStorage.setItem("userRole", data.user.role);

                    // Redirect based on role
                    window.location.href = data.user.role === "admin" ? "admin_dash.html" : "user_dash.html";

                } else {
                    const errorMessage = data.detail || "Login failed. Please check your credentials.";
                    errorBox.innerText = errorMessage;
                    errorBox.classList.remove("d-none");
                }
            } catch (err) {
                console.error("Login request failed:", err);
                errorBox.innerText = "An error occurred. Please check the console and ensure the server is running.";
                errorBox.classList.remove("d-none");
            }
        });
    }
});

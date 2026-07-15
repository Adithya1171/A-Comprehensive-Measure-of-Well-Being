// Custom Client-side Interactivity and Validation

document.addEventListener("DOMContentLoaded", () => {
    // 1. Password Confirmation Match Validation (Registration Page)
    const registerForm = document.querySelector("#register-form");
    if (registerForm) {
        const passwordInput = document.querySelector("#password");
        const confirmPasswordInput = document.querySelector("#confirm_password");
        
        registerForm.addEventListener("submit", (event) => {
            if (passwordInput.value !== confirmPasswordInput.value) {
                event.preventDefault();
                alert("Passwords do not match!");
            }
        });
    }

    // 2. Client-side Form Validation for HDI Prediction Form
    const predictForm = document.querySelector("#predict-form");
    if (predictForm) {
        const leInput = document.querySelector("#life_expectancy");
        const mysInput = document.querySelector("#mean_years_schooling");
        const eysInput = document.querySelector("#expected_years_schooling");
        const gniInput = document.querySelector("#gni_per_capita");

        predictForm.addEventListener("submit", (event) => {
            let hasErrors = false;
            let errorMessage = "";

            // Validate Life Expectancy (20 - 100)
            const le = parseFloat(leInput.value);
            if (isNaN(le) || le < 20 || le > 100) {
                hasErrors = true;
                errorMessage += "- Life Expectancy must be a number between 20 and 100 years.\n";
                leInput.classList.add("is-invalid");
            } else {
                leInput.classList.remove("is-invalid");
                leInput.classList.add("is-valid");
            }

            // Validate Mean Years of Schooling (0 - 20)
            const mys = parseFloat(mysInput.value);
            if (isNaN(mys) || mys < 0 || mys > 20) {
                hasErrors = true;
                errorMessage += "- Mean Years of Schooling must be a number between 0 and 20 years.\n";
                mysInput.classList.add("is-invalid");
            } else {
                mysInput.classList.remove("is-invalid");
                mysInput.classList.add("is-valid");
            }

            // Validate Expected Years of Schooling (0 - 25)
            const eys = parseFloat(eysInput.value);
            if (isNaN(eys) || eys < 0 || eys > 25) {
                hasErrors = true;
                errorMessage += "- Expected Years of Schooling must be a number between 0 and 25 years.\n";
                eysInput.classList.add("is-invalid");
            } else {
                eysInput.classList.remove("is-invalid");
                eysInput.classList.add("is-valid");
            }

            // Validate GNI per Capita (positive)
            const gni = parseFloat(gniInput.value);
            if (isNaN(gni) || gni <= 0) {
                hasErrors = true;
                errorMessage += "- Gross National Income (GNI) must be a positive number.\n";
                gniInput.classList.add("is-invalid");
            } else {
                gniInput.classList.remove("is-invalid");
                gniInput.classList.add("is-valid");
            }

            if (hasErrors) {
                event.preventDefault();
                alert("Please correct the following errors before submitting:\n\n" + errorMessage);
            }
        });

        // Add real-time change validation visual cues
        const inputs = [leInput, mysInput, eysInput, gniInput];
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                if (input.value.trim() !== "") {
                    input.classList.remove("is-invalid");
                }
            });
        });
    }

    // 3. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });
});

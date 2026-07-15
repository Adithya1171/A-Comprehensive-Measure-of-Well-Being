from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import functools
from app.predict import predict_hdi
from app.utils import register_user, verify_user, save_prediction, get_prediction_history

main = Blueprint("main", __name__)

def login_required(view):
    """Decorator to protect routes that require user authentication."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user" not in session:
            flash("You must be logged in to access this page.", "danger")
            return redirect(url_for("main.login"))
        return view(**kwargs)
    return wrapped_view

@main.route("/")
def home():
    """Home/Landing page."""
    if "user" in session:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")

@main.route("/register", methods=["GET", "POST"])
def register():
    """User Registration route."""
    if "user" in session:
        return redirect(url_for("main.dashboard"))
        
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        # Validations
        if not full_name or not email or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return render_template("register.html", full_name=full_name, email=email)
            
        if "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "danger")
            return render_template("register.html", full_name=full_name, email=email)
            
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", full_name=full_name, email=email)
            
        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("register.html", full_name=full_name, email=email)
            
        success, message = register_user(full_name, email, password)
        if success:
            flash(message + " Please log in.", "success")
            return redirect(url_for("main.login"))
        else:
            flash(message, "danger")
            return render_template("register.html", full_name=full_name, email=email)
            
    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    """User Login route."""
    if "user" in session:
        return redirect(url_for("main.dashboard"))
        
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        if not email or not password:
            flash("Please fill in all fields.", "danger")
            return render_template("login.html", email=email)
            
        user, message = verify_user(email, password)
        if user:
            # Create session
            session["user"] = {
                "id": user["id"],
                "name": user["full_name"],
                "email": user["email"]
            }
            session.permanent = True
            flash(message, "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash(message, "danger")
            return render_template("login.html", email=email)
            
    return render_template("login.html")

@main.route("/logout")
def logout():
    """User Logout route."""
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("main.login"))

@main.route("/dashboard")
@login_required
def dashboard():
    """User Dashboard page showing summary cards."""
    user = session["user"]
    history = get_prediction_history(user["id"])
    total_predictions = len(history)
    
    # Calculate some quick stats for the dashboard cards
    categories = [p["hdi_category"] for p in history]
    very_high_count = categories.count("Very High")
    high_count = categories.count("High")
    medium_count = categories.count("Medium")
    low_count = categories.count("Low")
    
    latest_prediction = history[0] if history else None
    
    return render_template(
        "dashboard.html",
        user_name=user["name"],
        total_predictions=total_predictions,
        latest_prediction=latest_prediction,
        very_high=very_high_count,
        high=high_count,
        medium=medium_count,
        low=low_count
    )

@main.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    """Protected prediction page."""
    user = session["user"]
    
    if request.method == "POST":
        life_expectancy = request.form.get("life_expectancy", "").strip()
        mean_years_schooling = request.form.get("mean_years_schooling", "").strip()
        expected_years_schooling = request.form.get("expected_years_schooling", "").strip()
        gni_per_capita = request.form.get("gni_per_capita", "").strip()
        
        # Validations
        try:
            le = float(life_expectancy)
            mys = float(mean_years_schooling)
            eys = float(expected_years_schooling)
            gni = float(gni_per_capita)
        except ValueError:
            flash("All inputs must be valid numeric values.", "danger")
            return render_template("predict.html", life_expectancy=life_expectancy, mean_years_schooling=mean_years_schooling, expected_years_schooling=expected_years_schooling, gni_per_capita=gni_per_capita)
            
        # Range checks
        errors = []
        if not (20.0 <= le <= 100.0):
            errors.append("Life Expectancy must be between 20 and 100 years.")
        if not (0.0 <= mys <= 20.0):
            errors.append("Mean Years of Schooling must be between 0 and 20 years.")
        if not (0.0 <= eys <= 25.0):
            errors.append("Expected Years of Schooling must be between 0 and 25 years.")
        if gni <= 0.0:
            errors.append("Gross National Income per Capita must be positive.")
            
        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("predict.html", life_expectancy=life_expectancy, mean_years_schooling=mean_years_schooling, expected_years_schooling=expected_years_schooling, gni_per_capita=gni_per_capita)
            
        try:
            # Predict
            score, category = predict_hdi(le, mys, eys, gni)
            
            # Save to Database
            success, db_msg = save_prediction(user["id"], le, mys, eys, gni, score, category)
            if not success:
                flash(db_msg, "warning")
                
            # Direct to result rendering
            return render_template(
                "result.html",
                predicted_hdi=score,
                hdi_category=category,
                life_expectancy=le,
                mean_years_schooling=mys,
                expected_years_schooling=eys,
                gni_per_capita=gni
            )
        except Exception as e:
            flash(f"Prediction Error: {str(e)}", "danger")
            return render_template("predict.html", life_expectancy=life_expectancy, mean_years_schooling=mean_years_schooling, expected_years_schooling=expected_years_schooling, gni_per_capita=gni_per_capita)
            
    return render_template("predict.html")

@main.route("/history")
@login_required
def history():
    """Protected prediction history page."""
    user = session["user"]
    history_list = get_prediction_history(user["id"])
    return render_template("history.html", history=history_list)

@main.route("/about")
def about():
    """About project page."""
    return render_template("about.html")

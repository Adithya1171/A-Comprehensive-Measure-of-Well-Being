import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_PATH = "database.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionary-like objects
    return conn

def init_db():
    """Initializes the database schema if tables do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            life_expectancy REAL NOT NULL,
            mean_years_schooling REAL NOT NULL,
            expected_years_schooling REAL NOT NULL,
            gni_per_capita REAL NOT NULL,
            predicted_hdi REAL NOT NULL,
            hdi_category TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def register_user(full_name, email, password):
    """Registers a new user after hashing the password."""
    # Basic validations
    if not full_name or not email or not password:
        return False, "All fields are required."
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower(),))
    if cursor.fetchone():
        conn.close()
        return False, "An account with this email already exists."
        
    # Hash password and insert
    pwd_hash = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
            (full_name, email.lower(), pwd_hash)
        )
        conn.commit()
        success = True
        msg = "Registration successful!"
    except sqlite3.Error as e:
        success = False
        msg = f"Database error: {str(e)}"
        
    conn.close()
    return success, msg

def verify_user(email, password):
    """Verifies user login credentials."""
    if not email or not password:
        return None, "Email and password are required."
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower(),))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user["password_hash"], password):
        return {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"]
        }, "Login successful!"
        
    return None, "Invalid email or password."

def save_prediction(user_id, life_expectancy, mean_years_schooling, expected_years_schooling, gni_per_capita, predicted_hdi, hdi_category):
    """Logs a prediction result associated with a specific user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO predictions (
                user_id, life_expectancy, mean_years_schooling, expected_years_schooling, gni_per_capita, predicted_hdi, hdi_category
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, life_expectancy, mean_years_schooling, expected_years_schooling, gni_per_capita, predicted_hdi, hdi_category))
        conn.commit()
        success = True
        msg = "Prediction saved successfully."
    except sqlite3.Error as e:
        success = False
        msg = f"Failed to save prediction: {str(e)}"
        
    conn.close()
    return success, msg

def get_prediction_history(user_id):
    """Fetches all prediction history for the specified user ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM predictions 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    """, (user_id,))
    
    rows = cursor.fetchall()
    history = []
    for row in rows:
        history.append({
            "id": row["id"],
            "life_expectancy": row["life_expectancy"],
            "mean_years_schooling": row["mean_years_schooling"],
            "expected_years_schooling": row["expected_years_schooling"],
            "gni_per_capita": row["gni_per_capita"],
            "predicted_hdi": row["predicted_hdi"],
            "hdi_category": row["hdi_category"],
            "created_at": datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S") if isinstance(row["created_at"], str) else row["created_at"]
        })
        
    conn.close()
    return history

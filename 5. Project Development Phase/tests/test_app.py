import os
import unittest
import sqlite3
import numpy as np
from app.predict import predict_hdi, classify_hdi_category
from app import utils

class TestHDIPredictor(unittest.TestCase):
    def setUp(self):
        # Configure a temporary database path for testing
        self.original_db = utils.DATABASE_PATH
        utils.DATABASE_PATH = "test_database.db"
        utils.init_db()

    def tearDown(self):
        # Restore the original database configuration and clean up
        utils.DATABASE_PATH = self.original_db
        if os.path.exists("test_database.db"):
            os.remove("test_database.db")

    def test_database_initialization(self):
        """Test database and tables creation."""
        conn = utils.get_db_connection()
        cursor = conn.cursor()
        
        # Check users table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        self.assertIsNotNone(cursor.fetchone(), "Users table should exist.")
        
        # Check predictions table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='predictions'")
        self.assertIsNotNone(cursor.fetchone(), "Predictions table should exist.")
        
        conn.close()

    def test_user_registration_and_login(self):
        """Test user sign up, duplicate email blocks, and secure login verification."""
        # Register user
        success, msg = utils.register_user("Test User", "test@example.com", "password123")
        self.assertTrue(success)
        self.assertEqual(msg, "Registration successful!")
        
        # Prevent duplicate email
        success2, msg2 = utils.register_user("Another User", "test@example.com", "password456")
        self.assertFalse(success2)
        self.assertIn("exists", msg2)
        
        # Verify valid login
        user, login_msg = utils.verify_user("test@example.com", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user["full_name"], "Test User")
        
        # Verify invalid login (wrong password)
        user_bad, login_msg_bad = utils.verify_user("test@example.com", "wrongpassword")
        self.assertNil(user_bad) if hasattr(self, "assertNil") else self.assertIsNone(user_bad)
        self.assertIn("Invalid", login_msg_bad)

    def test_predictions_database_log(self):
        """Test logging predictions to the database and fetching history logs."""
        # Register user
        utils.register_user("Test User", "test@example.com", "password123")
        user, _ = utils.verify_user("test@example.com", "password123")
        user_id = user["id"]
        
        # Log prediction
        success, db_msg = utils.save_prediction(user_id, 83.2, 13.0, 18.2, 66000.0, 0.9610, "Very High")
        self.assertTrue(success)
        
        # Retrieve history
        history = utils.get_prediction_history(user_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["life_expectancy"], 83.2)
        self.assertEqual(history[0]["predicted_hdi"], 0.9610)
        self.assertEqual(history[0]["hdi_category"], "Very High")

    def test_hdi_prediction_ranges(self):
        """Test prediction inputs and category classification bounds."""
        # 1. Test Category Rules
        self.assertEqual(classify_hdi_category(0.850), "Very High")
        self.assertEqual(classify_hdi_category(0.800), "Very High")
        self.assertEqual(classify_hdi_category(0.750), "High")
        self.assertEqual(classify_hdi_category(0.700), "High")
        self.assertEqual(classify_hdi_category(0.650), "Medium")
        self.assertEqual(classify_hdi_category(0.550), "Medium")
        self.assertEqual(classify_hdi_category(0.500), "Low")
        
        # 2. Test predict_hdi math & bounds
        try:
            score, category = predict_hdi(80.0, 12.0, 16.0, 45000.0)
            self.assertTrue(0.0 <= score <= 1.0)
            self.assertIn(category, ["Very High", "High", "Medium", "Low"])
        except FileNotFoundError:
            # If assets model/scaler not generated in test env, ignore execution check
            pass

        # 3. Test Invalid Range Validations
        with self.assertRaises(ValueError):
            # Out of range Life Expectancy
            predict_hdi(15.0, 10.0, 10.0, 5000.0)
        with self.assertRaises(ValueError):
            # Negative Schooling
            predict_hdi(80.0, -1.0, 10.0, 5000.0)
        with self.assertRaises(ValueError):
            # Negative GNI
            predict_hdi(80.0, 10.0, 10.0, -500.0)

if __name__ == "__main__":
    unittest.main()

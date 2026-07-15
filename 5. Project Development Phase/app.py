from app import create_app

# Instantiate the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the application on localhost with debug enabled for development
    app.run(debug=True, host="127.0.0.1", port=5000)

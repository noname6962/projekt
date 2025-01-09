from back import app as application  #  Import your Flask app instance from back.py


#  Optional: If you need a specific port, configure it here
if __name__ == "__main__":
    application.run(debug=False, port=8080)  # Set port if needed for AWS

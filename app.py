from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re  # For email validation
import smtplib # for sending emails
from email.mime.text import MIMEText #For email formatting
import os  # For accessing environment variables

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins (for development)

# Use environment variables for sensitive information
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    print("Error: Email credentials not found in environment variables.")
    # It's best to raise an exception and stop the app from running if these are missing in production
    # raise ValueError("Email credentials not found in environment variables.") #Uncomment for production

@app.route('/')
def index():
    return render_template('Emmanuel.html') #Changed to Emmanuel.html

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        message = data['message']

        # Basic input validation (you should enhance this)
        if not name or not email or not message:
            return jsonify({"success": False, "message": "All fields are required"})

        # Email validation (using the previous function)
        email_validation_result = validate_email_format(email)
        if not email_validation_result["valid"]:
            return jsonify({"success": False, "message": email_validation_result["error"]})

        # Create the email message
        msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage:\n{message}")
        msg['Subject'] = f"New Contact Form Submission from {name}"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS

        # Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: #Use a secure SMTP connection
            try:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            except smtplib.SMTPAuthenticationError as e:
                print(f"SMTP Authentication Error: {e}")
                return jsonify({"success": False, "message": "Email authentication failed. Check your credentials."})
            except Exception as e:
                print(f"Email Sending Error: {e}")
                return jsonify({"success": False, "message": "Failed to send email. Please try again later."})


        return jsonify({"success": True, "message": "Message sent successfully!"})

    except Exception as e:
        print(f"Error submitting form: {e}")  # Log the error
        return jsonify({"success": False, "message": "An error occurred while sending the message."})

def validate_email_format(email):
    """Validates the email format using regex."""
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"valid": False, "error": "Invalid email format"}
    return {"valid": True}


if __name__ == '__main__':
    app.run(debug=True) #Remove debug=True for production   
# Password Reset Flaw Application

This project is a simple Flask web application designed to demonstrate a security flaw related to password resets. The application allows users to reset their passwords without requiring email verification, highlighting the potential risks associated with this practice.

## Project Structure

```
password-reset-flaw-app
├── app.py                  # Main application file with Flask routes and logic
├── templates               # Directory containing HTML templates
│   ├── index.html         # Homepage with links to login and reset password
│   ├── login.html         # Login page with username and password form
│   ├── reset_password.html # Password reset page allowing users to change their password
│   ├── reset_success.html  # Success page displayed after password reset
│   └── user_dashboard.html  # User dashboard shown after successful login
├── requirements.txt        # List of dependencies for the project
└── README.md               # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd password-reset-flaw-app
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Start the Flask application by running:
   ```
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Usage

- Navigate to the homepage to access the login and password reset functionalities.
- Users can log in with their credentials or reset their password without email verification.
- After resetting the password, users will be redirected to a success page.

## Security Note

This application intentionally allows password resets without email verification to demonstrate the associated security risks. In a production environment, it is crucial to implement proper verification mechanisms to prevent unauthorized access and ensure user account security.
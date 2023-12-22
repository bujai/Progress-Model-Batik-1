import pyrebase
from pyrebase import initialize_app

# Firebase configuration
config = {
    "apiKey": "AIzaSyCGdmGLXFzJDC12wvfpBPshTEo-aoGj4P4",
    "authDomain": "data-yogjakarta-quest.firebaseapp.com",
    "databaseURL": "https://data-yogjakarta-quest-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "data-yogjakarta-quest",
    "storageBucket": "data-yogjakarta-quest.appspot.com",
    "messagingSenderId": "659590794174",
    "appId": "1:659590794174:web:c7150b97336cee808dc7ef",
    "measurementId": "G-0RP0LKBFVP"
}

# Initialize Firebase
firebase = initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Function to sign up a new user and add additional data to the database
def sign_up_user(name, phone, email, address, password):
    try:
        # Create the user using their email and password
        user = auth.create_user_with_email_and_password(email, password)
        # Add additional user data to the Firebase Realtime Database
        data = {"name": name, "phone": phone, "email": email, "address": address}
        db.child("users").child(user['localId']).set(data)
        return user['idToken']
    except Exception as e:
        # Handle the error (e.g., email already in use, weak password, etc.)
        print(e)
        return None


# Function to sign in an existing user
def sign_in_user(email, password):
    try:
        # Authenticate the user using their email and password
        user = auth.sign_in_with_email_and_password(email, password)
        # Return the user's ID token if the sign-in is successful
        return user['idToken'], user['localId']
    except Exception as e:
        # Handle the error (e.g., wrong password, user not found, etc.)
        print(e)
        return None, None
import mysql.connector
import hashlib

# Connect to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",  # Replace with your MySQL host
        user="root",       # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="career_counselling"  # Database name
    )

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a new user (signup)
def add_user(username, password):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Hash the password before storing it
        hashed_password = hash_password(password)

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        conn.close()
        return True, "Signup successful!"
    except mysql.connector.IntegrityError:
        return False, "Username already exists!"
    except Exception as e:
        return False, str(e)

# Function to validate user login
def validate_user(username, password):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Hash the password before checking
        hashed_password = hash_password(password)

        # Query to check if the username and password match
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, hashed_password))
        user = cursor.fetchone()
        conn.close()

        return user is not None  # Returns True if user exists, False otherwise
    except Exception as e:
        print("Error:", e)
        return False

# Example Usage
if __name__ == "__main__":
    # Example: Signup
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    success, message = add_user(username, password)
    print(message)

    # Example: Login
    username = input("Enter your username to login: ")
    password = input("Enter your password: ")
    if validate_user(username, password):
        print("Login successful!")
    else:
        print("Invalid username or password.")
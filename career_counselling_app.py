import streamlit as st
import joblib
import pandas as pd
import numpy as np
import hashlib
import mysql.connector
import matplotlib.pyplot as plt

# Connect to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",  # Replace with your MySQL host
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

# Load the pre-trained model
model = joblib.load('careermodel.pkl')

# Define the career categories for displaying the prediction
careerCategories = {
    0: "Architecture",
    1: "Arts",
    2: "Business",
    3: "Communications",
    4: "Education",
    5: "Engineering",
    6: "Healthcare",
    7: "Law",
    8: "Sales",
    9: "Government"
}

# Define a helper function to display additional information
def display_career_details(career):
    details = {

    "Architecture": """
    ### Career Details:
    Architects design buildings, spaces, and structures, requiring creativity and technical knowledge.

    ### Job Market Trends:
    The demand for sustainable and eco-friendly designs is increasing, with a focus on green architecture.

    ### Career Insights:
    Proficiency in CAD software and knowledge of building codes are essential for success.

    🎥 [Watch Career Video](https://www.youtube.com/watch?v=nymZ3dD-VWE)
    """,

    "Arts": """
    ### Career Details:
    Artists focus on creating visual, performing, or literary art and often engage in freelance or gallery work.

    ### Job Market Trends:
    Digital art and multimedia design are growing fields, with opportunities in gaming and animation.

    ### Career Insights:
    Building a strong portfolio and networking are key to gaining visibility and opportunities.

    🎥 [Watch Career Video](https://www.youtube.com/watch?v=OYF_LHeHLXA)
    """,

    "Business": """
    ### Career Details:
    Business professionals manage companies or organizations, focusing on strategy, finance, and operations.

    ### Job Market Trends:
    Data-driven decision-making and digital transformation are reshaping business roles.

    ### Career Insights:
    Skills in data analysis, project management, and leadership are highly valued.

    🎥 [Watch Career Video](https://www.youtube.com/watch?v=wVfhXYdTcdQ)
    """,

    "Communications": """
    ### Career Details:
    Professionals in communications manage media, public relations, marketing, and advertising.

    ### Job Market Trends:
    Social media marketing and content creation are in high demand, with a focus on digital platforms.

    ### Career Insights:
    Creativity, storytelling, and analytics skills are crucial for success in this field.

    🎥 [Watch Career Video](https://www.youtube.com/watch?v=joU9aYqDCQk)
    """,

    "Education": """
    ### Career Details:
    Educators teach and inspire others in schools, universities, or other learning environments.

    ### Job Market Trends:
    Online education and e-learning platforms are growing rapidly, creating new teaching opportunities.

    ### Career Insights:
    Adaptability to technology and strong interpersonal skills are essential.

    🎥 [Watch Career Video](https://www.youtube.com/watch?v=N6_cGS9yy7w)
    """,

    "Engineering": """
    ### Career Details:
    Engineers solve technical problems by applying scientific principles to design, develop, and improve systems.

    ### Job Market Trends:
    Renewable energy, AI, and robotics are driving demand for specialized engineering roles.

    ### Career Insights:
    Continuous learning and certifications in emerging technologies can boost career prospects.

    🎥 [Watch Career Video](https://www.youtube.com/watch?v=e5BWvz8_WyQ)
    """,

    "Healthcare": """
    ### Career Details:
    Healthcare professionals provide medical care, therapy, or counseling to individuals to improve health and wellness.

    ### Job Market Trends:
    Telemedicine and personalized healthcare are transforming the industry.

    ### Career Insights:
    Empathy, attention to detail, and staying updated with medical advancements are critical.

    🎥 [Watch Career Video](https://www.youtube.com/watch?v=i2pMEhEzbEs)
    """,

    "Law": """
    ### Career Details:
    Lawyers, judges, and paralegals practice law, providing legal advice, representation, and ensuring justice.

    ### Job Market Trends:
    Cybersecurity law and intellectual property law are emerging fields with growing demand.

    ### Career Insights:
    Strong research and analytical skills, along with specialization, can enhance career growth.

    🎥 [Watch Career Video](https://www.youtube.com/watch?v=aK2PVtgWLp8)
    """,

    "Sales": """
    ### Career Details:
    Salespeople focus on selling products or services, often working on commissions and building client relationships.

    ### Job Market Trends:
    E-commerce and digital sales are rapidly expanding, requiring tech-savvy professionals.

    ### Career Insights:
    Building relationships and understanding customer needs are key to success.

    🎥 [Watch Career Video](https://www.youtube.com/watch?v=E_ZIDu4u4WE)
    """
}


    
    return details.get(career, "No information available")

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.sidebar.title("Authentication")
    auth_option = st.sidebar.radio("Choose an option", ["Login", "Signup"])

    if auth_option == "Signup":
        st.title("Signup")
        username = st.text_input("Enter a username")
        password = st.text_input("Enter a password", type="password")
        if st.button("Signup"):
            success, message = add_user(username, password)
            if success:
                st.success(message)
            else:
                st.error(message)

    elif auth_option == "Login":
        st.title("Login")
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password", type="password")
        if st.button("Login"):
            if validate_user(username, password):
                st.success("Login successful!")
                st.session_state.authenticated = True
            else:
                st.error("Invalid username or password.")
else:
    # Sidebar: Introduction and Instructions
    st.sidebar.title("Career Counseling App")
    st.sidebar.markdown("""
    This app helps you determine the best career path based on your personality, thinking style, and score.
    Fill out the details below and get career recommendations that suit your profile.
    """)

    # Collecting User Inputs
    st.header("Step 1: Personality Details")
    personality = st.selectbox("Select your personality type", ['Introverted', 'Extroverted'])
    thinking = st.selectbox("Select your thinking type", ['Thinker', 'Feeler'])
    perception = st.selectbox("Select your perception type", ['Judger', 'Perceiver'])
    thought = st.selectbox("Select your thought process", ['Sensing', 'Intuition'])

    # LR Score input with validation
    LRscore = st.slider("Enter your LR Score (0 to 100)", 0, 100, 50)
    st.write(f"Your LR Score is: {LRscore}")

    # Predict Button
    if st.button("Predict Career Path"):
        # Mapping of input data to model features (encoding as per the trained model)
        personality_map = {'Introverted': 0, 'Extroverted': 1}
        thinking_map = {'Thinker': 0, 'Feeler': 1}
        perception_map = {'Judger': 0, 'Perceiver': 1}
        thought_map = {'Sensing': 0, 'Intuition': 1}
        
        # Creating a DataFrame with the user input
        user_data = pd.DataFrame({
            'personality': [personality_map[personality]],
            'thinking': [thinking_map[thinking]],
            'perception': [perception_map[perception]],
            'thought': [thought_map[thought]],
            'LRscore': [LRscore]
        })

        # Making the prediction using the model
        prediction = model.predict(user_data)
        predicted_career = careerCategories[prediction[0]]
        st.write(f"### Recommended Career Path: {predicted_career}")

        # Show career details
        career_info = display_career_details(predicted_career)
 
        st.markdown(career_info)

       
        # Display the probability (confidence level of the prediction)
        probability = model.predict_proba(user_data)[0]
        st.write("#### Prediction Confidence:")
        career_probs = {careerCategories[i]: prob for i, prob in enumerate(probability)}
        sorted_probs = sorted(career_probs.items(), key=lambda x: x[1], reverse=True)
        
        st.write("**Career Path Probabilities:**")
        for career, prob in sorted_probs:
            st.write(f"{career}: {prob * 100:.2f}%")
        
        # Bar chart of probabilities for all careers
        careers = [x[0] for x in sorted_probs]
        probs = [x[1] for x in sorted_probs]
        
        plt.figure(figsize=(10, 6))
        plt.barh(careers, probs, color='skyblue')
        plt.xlabel('Probability (%)')
        plt.title('Career Path Probabilities')
        plt.xlim(0, 1)
        st.pyplot(plt)

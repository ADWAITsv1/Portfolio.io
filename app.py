from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

# Database connection details - use environment variables in production
DATABASE_URL = os.getenv('DATABASE_URL')

# Initialize database
def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact_messages (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully")

# Call init_db at application startup - wrap in try/except to handle errors gracefully
try:
    init_db()
except Exception as e:
    print(f"Database initialization error: {e}")

# Sample project data - you'll replace this with your actual projects
projects = [
    {
        "title": "Predictive Analysis of Customer Churn",
        "description": "Used machine learning algorithms to predict customer churn in a telecom company.",
        "technologies": ["Python", "Scikit-learn", "Pandas", "Matplotlib"],
        "github_link": "https://github.com/yourusername/customer-churn",
        "image": "images/project1.jpg"
    },
    {
        "title": "Natural Language Processing for Sentiment Analysis",
        "description": "Developed a model to analyze sentiment in product reviews.",
        "technologies": ["Python", "NLTK", "TensorFlow", "Keras"],
        "github_link": "https://github.com/yourusername/sentiment-analysis",
        "image": "images/project2.jpg"
    }
]

# Sample research work - replace with your actual research
research = [
    {
        "title": "Novel Approach to Time Series Forecasting",
        "description": "Research on improving time series forecasting accuracy using hybrid models.",
        "link": "#",  # Link to your research paper or slides
        "date": "June 2023"
    },
    {
        "title": "Exploring Transfer Learning in Computer Vision",
        "description": "Investigation of transfer learning techniques for improved image classification.",
        "link": "#",  # Link to your research paper or slides
        "date": "January 2024"
    }
]

@app.route('/')
def home():
    return render_template('index.html', projects=projects, research=research)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/research')
def research_page():
    return render_template('research.html', research=research)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Store in database
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            timestamp = datetime.now()
            cursor.execute(
                "INSERT INTO contact_messages (name, email, message, timestamp) VALUES (%s, %s, %s, %s)",
                (name, email, message, timestamp)
            )
            conn.commit()
            conn.close()
            
            # Send an email notification (optional - add later)
            
            # Give feedback to user
            flash('Thank you for your message! I will get back to you soon.', 'success')
            print(f"Message from {name} saved successfully")
        except Exception as e:
            print(f"Error saving message: {e}")
            flash('There was an error sending your message. Please try again later.', 'error')
        
        # Redirect to avoid form resubmission
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

if __name__ == '__main__':
    # Use PORT environment variable for compatibility with Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
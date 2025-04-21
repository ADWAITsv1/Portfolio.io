from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

# Database connection details - hardcoded for reliability
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://adwait_portfolio_user:VD6UHceZqb63iGWI7ItyLkn82IRzcafi@dpg-d02p84qdbo4c73f1lpvg-a/adwait_portfolio')
print(f"Database URL: {DATABASE_URL}", file=sys.stderr)

# Helper function to get database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        return None

# Initialize database
def init_db():
    try:
        print(f"Attempting to connect to database...", file=sys.stderr)
        conn = get_db_connection()
        if not conn:
            print("Failed to get database connection", file=sys.stderr)
            return False
        
        cursor = conn.cursor()
        
        # Enable more verbose error reporting
        cursor.execute('SET client_min_messages TO NOTICE;')
        
        # Create the table with explicit schema
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
        
        # Verify the table exists
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'contact_messages');")
        table_exists = cursor.fetchone()[0]
        print(f"Table contact_messages exists: {table_exists}", file=sys.stderr)
        
        conn.close()
        print("Database initialized successfully", file=sys.stderr)
        return True
    except Exception as e:
        print(f"Database initialization error: {e}", file=sys.stderr)
        return False

# Call init_db at application startup
db_initialized = init_db()

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
        try:
            # Check if the request is JSON (from JavaScript fetch)
            if request.is_json:
                data = request.get_json()
                name = data.get('name')
                email = data.get('email')
                message = data.get('message')
                print(f"JSON data received - Name: {name}, Email: {email}", file=sys.stderr)
            else:
                # Regular form submission
                name = request.form.get('name')
                email = request.form.get('email')
                message = request.form.get('message')
                print(f"Form data received - Name: {name}, Email: {email}", file=sys.stderr)
            
            # Validate data
            if not all([name, email, message]):
                print("Missing required fields", file=sys.stderr)
                if request.is_json:
                    return jsonify({"status": "error", "message": "Missing required fields"}), 400
                else:
                    flash('All fields are required.', 'error')
                    return redirect(url_for('contact'))
            
            # Store in database
            print("Getting database connection...", file=sys.stderr)
            conn = get_db_connection()
            if not conn:
                print("Failed to connect to database", file=sys.stderr)
                if request.is_json:
                    return jsonify({"status": "error", "message": "Database connection error"}), 500
                else:
                    flash('Unable to connect to database. Please try again later.', 'error')
                    return redirect(url_for('contact'))
            
            print("Creating cursor...", file=sys.stderr)
            cursor = conn.cursor()
            timestamp = datetime.now()
            
            print("Executing SQL insert...", file=sys.stderr)
            cursor.execute(
                "INSERT INTO contact_messages (name, email, message, timestamp) VALUES (%s, %s, %s, %s) RETURNING id;",
                (name, email, message, timestamp)
            )
            
            # Get the ID of the inserted row
            inserted_id = cursor.fetchone()[0]
            print(f"Row inserted with ID: {inserted_id}", file=sys.stderr)
            
            # Commit the transaction
            conn.commit()
            conn.close()
            print(f"Message from {name} saved successfully with ID {inserted_id}", file=sys.stderr)
            
            # Return appropriate response
            if request.is_json:
                return jsonify({"status": "success", "message": "Message sent successfully", "id": inserted_id}), 200
            else:
                flash('Thank you for your message! I will get back to you soon.', 'success')
                return redirect(url_for('contact'))
                
        except Exception as e:
            print(f"Error processing form: {e}", file=sys.stderr)
            if request.is_json:
                return jsonify({"status": "error", "message": str(e)}), 500
            else:
                flash('There was an error sending your message. Please try again later.', 'error')
                return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/db-status')
def db_status():
    try:
        conn = get_db_connection()
        if not conn:
            return "Failed to connect to database."
        
        cursor = conn.cursor()
        
        # Check database version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        # List tables in the database
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()
        tables_list = [table[0] for table in tables]
        
        # Count messages
        cursor.execute("SELECT COUNT(*) FROM contact_messages;")
        count = cursor.fetchone()
        
        # Get most recent messages
        cursor.execute("""
            SELECT id, name, email, LEFT(message, 50) as message_preview, timestamp 
            FROM contact_messages 
            ORDER BY timestamp DESC 
            LIMIT 5;
        """)
        messages = cursor.fetchall()
        
        conn.close()
        
        html_response = f"""
        <h2>Database Connection Status</h2>
        <p>Database connected successfully.</p>
        <p>PostgreSQL version: {version[0]}</p>
        <p>Tables in database: {', '.join(tables_list)}</p>
        <p>Contact messages: {count[0]}</p>
        
        <h3>Recent Messages</h3>
        <table border="1" cellpadding="5">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Message Preview</th>
                <th>Timestamp</th>
            </tr>
        """
        
        if messages:
            for msg in messages:
                html_response += f"""
                <tr>
                    <td>{msg[0]}</td>
                    <td>{msg[1]}</td>
                    <td>{msg[2]}</td>
                    <td>{msg[3]}...</td>
                    <td>{msg[4]}</td>
                </tr>
                """
        else:
            html_response += """
            <tr>
                <td colspan="5" style="text-align: center;">No messages found in database</td>
            </tr>
            """
        
        html_response += """
        </table>
        <p><strong>Form Test:</strong> <a href="/contact">Go to contact form to submit a test message</a></p>
        """
        
        return html_response
    except Exception as e:
        return f"Database status check failed: {str(e)}"

if __name__ == '__main__':
    # Use PORT environment variable for compatibility with Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
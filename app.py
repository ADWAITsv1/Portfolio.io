from flask import Flask, render_template
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

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

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
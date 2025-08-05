from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from datetime import datetime

app = Flask(__name__)

# Data Science: Load and process projects data
def load_projects_data():
    # Sample data - in a real app, this would come from a database
    completed_projects = [
        {"name": "Residential Project 1", "location": "Udumalpet", "client": "Mr. Client 1", "year": "2022", "image": "project1.jpg"},
        {"name": "Commercial Project 1", "location": "Coimbatore", "client": "Mr. Client 2", "year": "2021", "image": "project2.jpg"},
        {"name": "Renovation Project 1", "location": "Karur", "client": "Mr. Client 3", "year": "2023", "image": "project3.jpg"}
    ]
    
    ongoing_projects = [
        {"name": "Udumalpet - Ravanapuram", "location": "Udumalpet", "client": "MR.Chandrakumar", "status": 65, "image": "ongoing1.jpg"},
        {"name": "Karur - Velayuthampalayam", "location": "Karur", "client": "MR.Vishagar", "status": 40, "image": "ongoing2.jpg"},
        {"name": "COIMBATORE - Annur", "location": "Coimbatore", "client": "MR. Gunaseelan", "status": 25, "image": "ongoing3.jpg"},
        {"name": "COIMBATORE - KAARAMADAI", "location": "Coimbatore", "client": "MR.KOSURI SIVA", "status": 80, "image": "ongoing4.jpg"},
        {"name": "DHARAPURAM - THILLAGOUNDANPUDHUR", "location": "Dharapuram", "client": "MR.JAYAPRAKASH", "status": 50, "image": "ongoing5.jpg"}
    ]
    
    return completed_projects, ongoing_projects

# Data Science: Generate project statistics chart
def generate_completion_chart():
    # Sample data for the chart
    data = {
        'Year': ['2020', '2021', '2022', '2023', '2024'],
        'Completed': [5, 8, 12, 15, 10],
        'Ongoing': [2, 3, 5, 7, 8]
    }
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(10, 6))
    plt.bar(df['Year'], df['Completed'], color='#e74c3c', label='Completed')
    plt.bar(df['Year'], df['Ongoing'], bottom=df['Completed'], color='#3498db', label='Ongoing')
    plt.title('Project Completion Over Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Projects')
    plt.legend()
    
    # Save the plot to a bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert to base64 for embedding in HTML
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return chart_image

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/projects')
def projects():
    completed_projects, ongoing_projects = load_projects_data()
    
    # Generate chart for project statistics
    chart_image = generate_completion_chart()
    
    # Save the chart image temporarily (in a real app, use a proper storage solution)
    chart_path = os.path.join('static', 'images', 'completion_chart.png')
    with open(chart_path, 'wb') as f:
        f.write(base64.b64decode(chart_image))
    
    return render_template('projects.html', 
                         completed_projects=completed_projects,
                         ongoing_projects=ongoing_projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']
        
        # Data Science: Log the contact form submission (in a real app, save to database)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp},{name},{email},{phone},{subject}\n"
        
        with open('contact_submissions.csv', 'a') as f:
            f.write(log_entry)
        
        # Data Science: Simple analysis - count submissions per day
        try:
            df = pd.read_csv('contact_submissions.csv', names=['timestamp', 'name', 'email', 'phone', 'subject'])
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            submissions_by_day = df.groupby('date').size().reset_index(name='count')
            print("\nContact form submissions by day:")
            print(submissions_by_day)
        except Exception as e:
            print(f"Error analyzing contact data: {e}")
        
        return redirect(url_for('contact_success'))
    
    return render_template('contact.html')

@app.route('/contact/success')
def contact_success():
    return render_template('contact.html', success=True)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(os.path.join('static', 'images'), exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True)
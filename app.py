from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
# Initialize the database
def init_db():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()

    # Table for storing contact form details
    cursor.execute('''CREATE TABLE IF NOT EXISTS portfolio (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        message TEXT NOT NULL
                    )''')

    # Table for storing certificates
    cursor.execute('''CREATE TABLE IF NOT EXISTS certificates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        certificate_name TEXT NOT NULL,
                        skills TEXT NOT NULL,
                        institution TEXT NOT NULL,
                        learnings TEXT NOT NULL
                    )''')

    # Table for storing projects
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        technologies TEXT NOT NULL,
                        link TEXT NOT NULL
                    )''')

    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/skills')
def skills():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT certificate_name, skills, institution, learnings FROM certificates')
    certificates = cursor.fetchall()
    conn.close()
    return render_template('skills.html', certificates=certificates)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO portfolio (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    return render_template('contact.html')

app.secret_key =os.environ.get("SECRET_CODE")  
# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Admin route
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin panel.", "danger")
        return redirect(url_for('login'))

    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()

    # Fetch data from both tables
    cursor.execute('SELECT * FROM portfolio')
    portfolio_data = cursor.fetchall()

    cursor.execute('SELECT * FROM certificates')
    certificates_data = cursor.fetchall()

    cursor.execute('SELECT * FROM projects')
    projects_data = cursor.fetchall()

    conn.close()

    return render_template('admin.html', portfolio_data=portfolio_data, certificates_data=certificates_data, projects_data=projects_data)


# Add Certificate Route
@app.route('/add_certificate', methods=['POST'])
def add_certificate():
    if request.method == 'POST':
        certificate_name = request.form['certificate_name']
        skills = request.form['skills']
        institution = request.form['institution']
        learnings = request.form['learnings']

        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO certificates (certificate_name, skills, institution, learnings) VALUES (?, ?, ?, ?)',
                       (certificate_name, skills, institution, learnings))
        conn.commit()
        conn.close()
        flash("Certificate added successfully!", "success")
        return redirect(url_for('admin'))

# Update Certificate Route
@app.route('/update_certificate/<int:id>', methods=['POST'])
def update_certificate(id):
    if request.method == 'POST':
        certificate_name = request.form['certificate_name']
        skills = request.form['skills']
        institution = request.form['institution']
        learnings = request.form['learnings']

        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE certificates
                          SET certificate_name = ?, skills = ?, institution = ?, learnings = ?
                          WHERE id = ?''', (certificate_name, skills, institution, learnings, id))
        conn.commit()
        conn.close()
        flash("Certificate updated successfully!", "success")
        return redirect(url_for('admin'))

# Delete Certificate Route
@app.route('/delete_certificate/<int:id>')
def delete_certificate(id):
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM certificates WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Certificate deleted successfully!", "success")
    return redirect(url_for('admin'))

# Edit Contact Message Route
@app.route('/edit_message/<int:message_id>', methods=['GET', 'POST'])
def edit_message(message_id):
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM portfolio WHERE id = ?', (message_id,))
    message_data = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE portfolio SET name = ?, email = ?, message = ? WHERE id = ?''', (name, email, message, message_id))
        conn.commit()
        conn.close()

        flash("Message updated successfully!", "success")
        return redirect(url_for('admin'))

    return render_template('edit_message.html', message=message_data)


# Delete Contact Message Route
@app.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))

    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM portfolio WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()
    flash("Message deleted successfully!", "success")
    return redirect(url_for('admin'))

# Logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin'))


@app.route('/edit_contact/<int:contact_id>', methods=['GET'])
def edit_contact(contact_id):
    # Fetch the contact details by ID from the database
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM portfolio WHERE id = ?', (contact_id,))
    contact_data = cursor.fetchone()
    conn.close()

    if contact_data:
        contact = {'id': contact_data[0], 'name': contact_data[1], 'email': contact_data[2], 'message': contact_data[3]}
        return render_template('edit_contact.html', contact=contact)
    else:
        return "Contact not found.", 404

@app.route('/update_contact/<int:contact_id>', methods=['POST'])
def update_contact(contact_id):
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Update the contact details in the database
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE portfolio
        SET name = ?, email = ?, message = ?
        WHERE id = ?
    ''', (name, email, message, contact_id))
    conn.commit()
    conn.close()

    return redirect(url_for('admin'))


@app.route('/projects')
def projects():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects')
    project_data = cursor.fetchall()
    conn.close()

    # Convert the fetched data into a list of dictionaries
    projects = []
    for row in project_data:
        projects.append({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'technologies': row[3],
            'link': row[4]
        })

    return render_template('project.html', projects=projects)

# Add Project Route
@app.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        technologies = request.form['technologies']
        link = request.form['link']

        # Save to the projects table
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO projects (project_name, description, technologies, link)
                          VALUES (?, ?, ?, ?)''', (project_name, description, technologies, link))
        conn.commit()
        conn.close()

        flash("Project added successfully!", "success")
        return redirect(url_for('admin'))


@app.route('/about')
def about():
    return render_template('about.html')

#Project routes
# Edit Project Route
@app.route('/update_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project_data = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        name = request.form['project_name']
        description = request.form['description']
        technologies = request.form['technologies']
        link = request.form['link']

        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE projects
                          SET project_name = ?, description = ?, technologies = ?, link = ?
                          WHERE id = ?''', (name, description, technologies, link, project_id))
        conn.commit()
        conn.close()

        flash("Project updated successfully!", "success")
        return redirect(url_for('admin'))

    


# Delete Project Route
@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))

    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()
    
    flash("Project deleted successfully!", "success")
    return redirect(url_for('admin'))


@app.route('/cv')
def cv():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()

    # Fetching certificates data
    cursor.execute('SELECT certificate_name, skills, institution, learnings FROM certificates')
    certificates = cursor.fetchall()

    # Fetching projects data
    cursor.execute('SELECT project_name, description, technologies, link FROM projects')
    projects = cursor.fetchall()

    conn.close()

    # Data to pass to template
    personal_info = {
        'name': 'Khelendra Rauniyar',  # Replace with dynamic data or hard-coded for testing
        'address': 'Mamunpur, Punjab',
        'contact_email': 'Khelendra71412@gmial.com',
        'contact_phone': '+91 7739933172'
    }

    return render_template('cv.html', name=personal_info['name'],
                           address=personal_info['address'],
                           contact_email=personal_info['contact_email'],
                           contact_phone=personal_info['contact_phone'],
                           certificates=certificates,
                           projects=projects)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

# Personal Portfolio Web Application

This is a dynamic personal portfolio web application built with [Flask](https://flask.palletsprojects.com/) and [SQLite](https://www.sqlite.org/), designed to showcase your skills, projects, certifications, and CV. The application features an admin panel for easy management of portfolio content, including projects, certificates, and contact messages.

## Features

- **Home Page:** Introduction and vision statement.
- **About Page:** Detailed background, education, skills, and achievements.
- **Skills Page:** List of certifications and key skills.
- **Projects Page:** Showcase of projects with descriptions and technologies used.
- **Contact Page:** Contact form for visitors to send messages.
- **CV Page:** Dynamic CV with print and PDF export options.
- **Admin Panel:** Secure admin interface to manage projects, certificates, and contact messages.

## Technologies Used

- Python 3
- Flask
- SQLite
- HTML5, CSS3 (custom styles)
- [dotenv](https://pypi.org/project/python-dotenv/) for environment variable management

## Getting Started

### Prerequisites

- Python 3.x
- [pip](https://pip.pypa.io/en/stable/)
- (Optional) [virtualenv](https://virtualenv.pypa.io/)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/your-portfolio-repo.git
    cd your-portfolio-repo
    ```

2. **Create and activate a virtual environment (optional but recommended):**
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    pip install flask python-dotenv
    ```

4. **Set up environment variables:**
    - Create a `.env` file in the project root:
      ```
      SECRET_CODE=your_secret_key_here
      ```
    - Replace `your_secret_key_here` with a secure random string.

5. **Initialize the database and run the app:**
    ```sh
    python app.py
    ```
    - The app will be available at `http://127.0.0.1:5000/`.

## Usage

- Visit `/admin` to access the admin panel (default credentials: [admin](http://_vscodecontentref_/0) / `password123`).
- Add, update, or delete projects, certificates, and contact messages from the admin panel.
- Visitors can view your portfolio, send messages, and download/print your CV.

## Folder Structure

- [app.py](http://_vscodecontentref_/1) - Main Flask application.
- [templates](http://_vscodecontentref_/2) - HTML templates for all pages.
- [css](http://_vscodecontentref_/3) - CSS stylesheets.
- [portfolio.db](http://_vscodecontentref_/4) - SQLite database file.
- [utils](http://_vscodecontentref_/5) - (Optional) Utility scripts or modules.
- [.env](http://_vscodecontentref_/6) - Environment variables (not to be committed to public repos).

## License

This project is open source and available under the MIT License.

---

**Author:**  
Khelendra Rauniyar  
[LinkedIn](https://www.linkedin.com/in/khelendra-rauniyar-4a0424257/) | [GitHub](https://github.com/Khelendrarauniyar)

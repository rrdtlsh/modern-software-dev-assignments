## Student Task Manager (Flask) – Version 2

**Student Task Manager** is a simple CRUD web application built as part of a university assignment to fulfill the requirement of using a non‑JavaScript backend language. It allows students to manage their tasks by creating, viewing, updating, and deleting task entries through a clean, browser-based interface.

### Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML, Tailwind CSS (via CDN)

### Features

- **Create**: Add new student tasks with title, description, and deadline.
- **Read**: View a table of all existing tasks with their current status.
- **Update**: Edit an existing task’s details and status (e.g., pending/completed).
- **Delete**: Remove tasks that are no longer needed.

### Prerequisites & Installation

1. **Install Python** (3.x) on your system if it is not already installed.
2. **Create and activate a virtual environment** (optional but recommended):
   - On Windows (PowerShell):
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
3. **Install Flask** using `pip`:
   ```bash
   pip install flask
   ```

### How to Run

1. Make sure you are in the `flask-task-app` directory (where `app.py` is located).
2. Start the Flask development server:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to:
   - `http://localhost:5000`

The application will be available at this URL, and you can immediately start creating and managing student tasks.

### Database Configuration

- This project uses **SQLite** as its database engine.
- The database file (typically named `database.db`) is **created automatically** when you run the application for the first time.
- No additional configuration or `.env` file is required for database setup; everything is self-contained and ready to use out of the box.

This README is intended to be clear and concise for use in a GitHub repository, making it easy for others to understand, set up, and run the Student Task Manager application.
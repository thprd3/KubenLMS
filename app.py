from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Table for modules
        cursor.execute('''CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )''')
        # Table for students
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )''')
        # Table linking students and module submissions
        cursor.execute('''CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            is_approved INTEGER DEFAULT 0,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (module_id) REFERENCES modules(id)
        )''')
        # Table for module dependencies
        cursor.execute('''CREATE TABLE IF NOT EXISTS module_dependencies (
            module_id INTEGER NOT NULL,
            required_module_id INTEGER NOT NULL,
            FOREIGN KEY (module_id) REFERENCES modules(id),
            FOREIGN KEY (required_module_id) REFERENCES modules(id),
            PRIMARY KEY (module_id, required_module_id)
        )''')
        
        # Insert dummy data for students
        cursor.execute('INSERT INTO students (name) VALUES (?)', ('Simen',))
        cursor.execute('INSERT INTO students (name) VALUES (?)', ('Thale',))
        cursor.execute('INSERT INTO students (name) VALUES (?)', ('Thomas',))

        # Insert dummy data for modules
        cursor.execute('INSERT INTO modules (title, description) VALUES (?, ?)', ('Introduction to Python', 'Learn the basics of Python programming.'))
        cursor.execute('INSERT INTO modules (title, description) VALUES (?, ?)', ('Database Fundamentals', 'Learn SQL and database design.'))
        cursor.execute('INSERT INTO modules (title, description) VALUES (?, ?)', ('Web Development Basics', 'Build your first website using HTML, CSS, and JavaScript.'))
    conn.close()
init_db()

@app.route('/reset_db', methods=['POST'])
def reset_database():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS submissions')
        cursor.execute('DROP TABLE IF EXISTS module_dependencies')
        cursor.execute('DROP TABLE IF EXISTS modules')
        cursor.execute('DROP TABLE IF EXISTS students')
        conn.commit()
        init_db()
    return redirect(url_for('index'))

@app.route('/') # lists all modules
def index():
    student_id = 1  # Example: hardcoded student ID for now
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        modules = cursor.execute('''
            SELECT m.id, m.title, m.description,
                   CASE WHEN EXISTS (
                       SELECT 1 FROM module_dependencies md
                       LEFT JOIN submissions s ON md.required_module_id = s.module_id
                       WHERE md.module_id = m.id AND (s.is_approved IS NULL OR s.is_approved = 0)
                   ) THEN 0 ELSE 1 END AS is_accessible,
                   CASE WHEN EXISTS (
                       SELECT 1 FROM submissions s
                       WHERE s.module_id = m.id AND s.student_id = ? AND s.is_approved = 1
                   ) THEN 1 ELSE 0 END AS is_completed
            FROM modules m
        ''', (student_id,)).fetchall()
    return render_template('index.html', modules=modules)

@app.route('/module/<int:module_id>') # module page
def module(module_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        module = cursor.execute('SELECT * FROM modules WHERE id = ?', (module_id,)).fetchone()
    return render_template('module.html', module=module)

# student adds finished module into submission queue
@app.route('/submit/<int:module_id>', methods=['POST']) 
def submit_module(module_id):
    student_id = 1  # Example: hardcoded student ID for now
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO submissions (student_id, module_id, is_approved) VALUES (?, ?, 0)', (student_id, module_id))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        submissions = cursor.execute('''
            SELECT s.id, s.student_id, st.name, m.title, s.is_approved
            FROM submissions s
            LEFT JOIN students st ON s.student_id = st.id
            LEFT JOIN modules m ON s.module_id = m.id
        ''').fetchall()
    return render_template('admin.html', submissions=submissions)

@app.route('/approve/<int:submission_id>', methods=['POST'])
def approve_submission(submission_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE submissions SET is_approved = 1 WHERE id = ?', (submission_id,))
        conn.commit()
    return redirect(url_for('admin'))

@app.route('/add', methods=['GET', 'POST']) # add new module
def add_module():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        required_modules = request.form.getlist('required_modules')
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO modules (title, description) VALUES (?, ?)', (title, description))
            new_module_id = cursor.lastrowid
            for req_module_id in required_modules:
                cursor.execute('INSERT INTO module_dependencies (module_id, required_module_id) VALUES (?, ?)', (new_module_id, req_module_id))
            conn.commit()
        return redirect(url_for('index'))
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        modules = cursor.execute('SELECT id, title FROM modules').fetchall()
    return render_template('add.html', modules=modules)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
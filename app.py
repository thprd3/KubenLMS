from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            is_completed INTEGER DEFAULT 0
        )''')
    conn.close()

init_db()

# Routes
@app.route('/')
def index():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        modules = cursor.execute('SELECT * FROM modules').fetchall()
    return render_template('index.html', modules=modules)

@app.route('/module/<int:module_id>')
def module(module_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        module = cursor.execute('SELECT * FROM modules WHERE id = ?', (module_id,)).fetchone()
    return render_template('module.html', module=module)

@app.route('/complete/<int:module_id>', methods=['POST'])
def complete_module(module_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE modules SET is_completed = 1 WHERE id = ?', (module_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_module():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO modules (title, description) VALUES (?, ?)', (title, description))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Initialize the database and create the books table if it does not exist
def init_db():
    with sqlite3.connect('books.db') as conn:
        c = conn.cursor()
        # Create a simple table with title, author, and year
        c.execute('''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER
        )''')
        conn.commit()

# Route to list all books and provide a search form
@app.route('/books', methods=['GET'])
def books():
    init_db()
    search = request.args.get('search')
    with sqlite3.connect('books.db') as conn:
        c = conn.cursor()
        if search:
            # Perform a search on title, author, or year fields
            query = "SELECT id, title, author, year FROM books WHERE title LIKE ? OR author LIKE ? OR CAST(year AS TEXT) LIKE ?"
            params = (f'%{search}%', f'%{search}%', f'%{search}%')
            c.execute(query, params)
        else:
            c.execute("SELECT id, title, author, year FROM books")
        rows = c.fetchall()
        # Convert rows to list of dictionaries for template
        books_list = []
        for row in rows:
            books_list.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'year': row[3]
            })
    return render_template('books.html', books=books_list, search=search)

# Route to add a new book
@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    init_db()
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')
        with sqlite3.connect('books.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
            conn.commit()
        return redirect(url_for('books'))
    # Render the form to add a new book
    return render_template('add_book.html')

# Main entry point when running this script directly
if __name__ == '__main__':
    app.run(debug=True)

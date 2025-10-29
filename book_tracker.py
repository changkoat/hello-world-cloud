from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)
# Initialize the database and create the books table if it does not exist
def init_db():
    with sqlite3.connect('books.db') as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, genre TEXT, summary TEXT)')
        conn.commit()
# Route to list all books and provide a search form
@app.route('/books', methods=['GET'])
def books():
    init_db()
    search = request.args.get('search')
    with sqlite3.connect('books.db') as conn:
        c = conn.cursor()
        if search:
            c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + search + '%', '%' + search + '%'))
        else:
            c.execute("SELECT * FROM books")
        books_list = c.fetchall()
    html = '<h1>Books</h1>'
    search_value = search or ''
    html += '<form action="/books" method="get">'
    html += '<input name="search" placeholder="Search by title or author" value="' + search_value + '">' 
    html += '<input type="submit" value="Search"></form>'
    html += '<a href="/books/add">Add Book</a>'
    html += '<ul>'
    for b in books_list:
        title = b[1] if b[1] else ''
        author = b[2] if b[2] else ''
        genre = b[3] if b[3] else ''
        summary = b[4] if b[4] else ''
        html += '<li><strong>' + title + '</strong> by ' + author + ' (' + genre + ') - ' + summary + '</li>'
    html += '</ul>'
    return html
# Route to add a new book to the database
@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    init_db()
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        summary = request.form.get('summary')
        with sqlite3.connect('books.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO books (title, author, genre, summary) VALUES (?, ?, ?, ?)", (title, author, genre, summary))
            conn.commit()
        return redirect(url_for('books'))
    return '''
        <h1>Add Book</h1>
        <form method="post">
            Title: <input name="title"><br>
            Author: <input name="author"><br>
            Genre: <input name="genre"><br>
            Summary: <textarea name="summary"></textarea><br>
            <input type="submit" value="Add">
        </form>
    '''
if __name__ == '__main__':
    app.run(debug=True)

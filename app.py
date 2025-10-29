from flask import Flask
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

@app.route('/')
def hello():
    init_db()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO visits DEFAULT VALUES')
    conn.commit()
    count = c.execute('SELECT COUNT(*) FROM visits').fetchone()[0]
    conn.close()
    return f'Hello World! You are visitor number {count}.'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

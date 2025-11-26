from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import random
from datetime import datetime
import os

app = Flask(__name__)
DATABASE = 'inspirational_board.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    count = conn.execute('SELECT COUNT(*) FROM quotes').fetchone()[0]
    if count == 0:
        default_quotes = [
            ("The only way to do great qwork is to love what you do.", "Steve Jobs"),
            ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
            ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
        ]
        conn.executemany('INSERT INTO quotes (text, author) VALUES (?, ?)', default_quotes)
        conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    quotes = conn.execute('SELECT * FROM quotes ORDER BY created_at DESC').fetchall()
    conn.close()
    
    # Get a random quote for display
    random_quote = random.choice(quotes) if quotes else None
    
    return render_template('index.html', quotes=quotes, random_quote=random_quote)

@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    conn = get_db_connection()
    quotes = conn.execute('SELECT * FROM quotes ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return jsonify([dict(quote) for quote in quotes])

@app.route('/api/quotes/random', methods=['GET'])
def get_random_quote():
    conn = get_db_connection()
    quotes = conn.execute('SELECT * FROM quotes').fetchall()
    conn.close()
    
    if quotes:
        random_quote = random.choice(quotes)
        return jsonify(dict(random_quote))
    return jsonify({"error": "No quotes available"}), 404

@app.route('/api/quotes', methods=['POST'])
def add_quote():
    data = request.get_json()
    
    if not data or 'text' not in data or 'author' not in data:
        return jsonify({"error": "Missing text or author"}), 400
    
    text = data['text'].strip()
    author = data['author'].strip()
    
    if not text or not author:
        return jsonify({"error": "Text and author cannot be empty"}), 400
    
    conn = get_db_connection()
    cursor = conn.execute('INSERT INTO quotes (text, author) VALUES (?, ?)', (text, author))
    quote_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({"id": quote_id, "text": text, "author": author}), 201

@app.route('/api/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM quotes WHERE id = ?', (quote_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Quote deleted successfully"}), 200

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)



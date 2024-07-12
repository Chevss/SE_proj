# server/server.py
from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), 'Trimark_construction_supply.db')

def connect_db():
    return sqlite3.connect(DATABASE)

@app.route('/query', methods=['POST'])
def query_db():
    query = request.json.get('query')
    params = request.json.get('params', ())
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.mongo_client import get_database

app = Flask(__name__)

db = get_database()
collection = db["articles"]

@app.route('/', methods=['GET'])
def results():
    # Fetch all articles from the database
    results = list(collection.find({}))  # Adjust query if needed
    return render_template("search.html", results=results)

if __name__ == '__main__':
    app.run(debug=True)
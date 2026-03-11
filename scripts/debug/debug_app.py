from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def debug_page():
    return send_from_directory('.', 'debug_upload.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
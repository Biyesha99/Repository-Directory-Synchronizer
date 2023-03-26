
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sync', methods=['POST'])
def sync():
    folder_path = request.form.get('folder_path')
    access_token = request.form.get('access_token')
    # Call the sync_dropbox.py script with the folder_path and access_token parameters
    return 'Sync complete!'

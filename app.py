from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from werkzeug.utils import secure_filename
import os

# Application setup
app = Flask(__name__)
app.secret_key = 'secret123'

# Upload folder
app.config['UPLOAD_FOLDER'] = 'uploads/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Variable route
@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}, welcome to our Flask app!'

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = username
        flash('Login successful')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    return render_template('dashboard.html', user=user)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out')
    return redirect(url_for('home'))

# Set cookie
@app.route('/set-cookie')
def set_cookie():
    response = make_response("Cookie has been set")
    response.set_cookie('course', 'Flask')
    return response

# Get cookie
@app.route('/get-cookie')
def get_cookie():
    course = request.cookies.get('course')
    return f'The course cookie value is: {course}'

# File upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash("No file selected", "error")
            return redirect(url_for("upload_file"))

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("File uploaded successfully", "success")
        return redirect(url_for('upload_file'))

    return render_template('upload.html')

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Run server
if __name__ == '__main__':
    app.run(debug=True)
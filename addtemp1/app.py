from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key.

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///templates.db'
db = SQLAlchemy(app)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    creator_name = db.Column(db.String(50))
    filename = db.Column(db.String(100))
    timestamp = db.Column(db.String(20))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    templates = Template.query.all()
    return render_template('home.html', templates=templates)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload-form', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        creator_name = request.form['creator_name']
        category = request.form['category']
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_template = Template(
                name=filename,
                category=category,
                creator_name=creator_name,
                filename=filename,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            db.session.add(new_template)
            db.session.commit()
            flash('Template uploaded successfully', 'success')
        else:
            flash('Invalid file format or no file uploaded', 'danger')

    return render_template('upload.html')

@app.route('/create-form', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Handle the form submission for creating a new template
        name = request.form['name']
        category = request.form['category']
        creator_name = request.form['creator_name']
        # You can add the data to the database here
        flash('Template created successfully', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)











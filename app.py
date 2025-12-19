import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Project, Client, ContactLead, Newsletter
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 1. Configuration
# Using SQLite locally; this creates a file named realestate.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///realestate.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'flipr_secret_key'
db.init_app(app)

# 2. BONUS: Image Cropping Logic (Requirement: 450x350)
def save_and_crop(file):
    filename = secure_filename(file.filename)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = Image.open(file)
    
    # Resize and crop to exactly 450x350 as per bonus task
    img = img.resize((450, 350), Image.Resampling.LANCZOS)
    img.save(path)
    return filename

# 3. ROUTES

@app.route('/')
def index():
    # Fetch data to display in "Our Project" and "Happy Clients" sections
    projects = Project.query.all()
    clients = Client.query.all()
    return render_template('index.html', projects=projects, clients=clients)

@app.route('/admin')
def admin_panel():
    # Fetch all data for the admin to view
    leads = ContactLead.query.all()
    subs = Newsletter.query.all()
    return render_template('admin.html', leads=leads, subs=subs)

@app.route('/admin')
def admin_panel():
    leads = ContactLead.query.all()
    subs = Newsletter.query.all()
    projects = Project.query.all()  # <--- CRUCIAL: Fetch the projects
    return render_template('admin.html', leads=leads, subs=subs, projects=projects)

@app.route('/admin/add-project', methods=['POST'])
def add_project():
    file = request.files.get('image')
    if file:
        filename = save_and_crop(file)
        new_project = Project(
            name=request.form.get('name'),
            description=request.form.get('desc'),
            image_path=filename
        )
        db.session.add(new_project)
        db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/add-client', methods=['POST'])
def add_client():
    file = request.files.get('image')
    if file:
        filename = save_and_crop(file)
        new_client = Client(
            name=request.form.get('name'),
            designation=request.form.get('designation'),
            description=request.form.get('desc'),
            image_path=filename
        )
        db.session.add(new_client)
        db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/contact', methods=['POST'])
def contact():
    # Save contact form details to backend
    new_lead = ContactLead(
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        mobile=request.form.get('mobile'),
        city=request.form.get('city')
    )
    db.session.add(new_lead)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Save newsletter email to backend
    email = request.form.get('email')
    if email:
        new_sub = Newsletter(email=email)
        db.session.add(new_sub)
        db.session.commit()
    return redirect(url_for('index'))

# 4. Initialization
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Creates the database tables
    app.run(debug=True)
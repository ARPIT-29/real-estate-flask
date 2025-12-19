from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1. Table for Projects
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))

# 2. Table for Clients (Happy Clients Section)
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_path = db.Column(db.String(255))

# 3. Table for Contact Form Leads
class ContactLead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    city = db.Column(db.String(50))

# 4. Table for Newsletter
class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
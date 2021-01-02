import os
import datetime, re

from flask import Flask, render_template, redirect, request 
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "contactdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

###################### Database - Table ##############################

def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now, 
        onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Contact: %s>' % self.id


###################### Routes & Views ##############################
@app.route('/', methods = ["GET", "POST"])
def index():
    if request.form:
        try:
            contact = Contact(fname=request.form.get("fname"), lname=request.form.get("lname"), age=request.form.get("age"), phone=request.form.get("phone"), email=request.form.get("email"))
            db.session.add(contact)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    contacts = Contact.query.all()
    return render_template("index.html", contacts=contacts)
    

@app.route('/edit')
def edit():
    return '<h1> Edit page is working </h1>'

@app.route('/show')
def show():
    return '<h1> Show page is working </h1>'






if __name__ == "__main__":
    app.run(debug = True)
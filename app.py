from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from chatbot import generate_response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job.db'
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    education = db.Column(db.String(100))
    work_experience = db.Column(db.Text)
    target_job = db.Column(db.String(50))
    skills_focus = db.Column(db.Text)

    def __repr__(self):
        return f"{self.id} - {self.name}"

class UserForm(FlaskForm):
    name = StringField('Name')
    education = StringField('Educational Background')
    work_experience = TextAreaField('Work Experience')
    target_job = StringField('Target Job/Industry')
    skills_focus = TextAreaField('Specific Skills or Technologies to Focus On')

# Create tables before running the app
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()

    if form.validate_on_submit():
        user = Job(
            name=form.name.data,
            education=form.education.data,
            work_experience=form.work_experience.data,
            target_job=form.target_job.data,
            skills_focus=form.skills_focus.data
        )

        db.session.add(user)
        db.session.commit()

        # Get the user input and generate a response using the chatbot
        user_input = form.name.data  # You can change this based on your requirements
        chatbot_response = generate_response(user_input)

        # Pass the response to the template or handle as needed
        return render_template('chatbot.html', response=chatbot_response)

    return render_template('index.html', form=form)

@app.route('/product')
def product():
    return 'This is feedback page'

if __name__ == "__main__":
    app.run(debug=True, port=8000)

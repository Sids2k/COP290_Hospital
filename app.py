from flask import Flask, render_template, url_for, redirect, request, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt
import sqlite3
import requests
import json

app = Flask(__name__)

# First database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_BINDS'] = {
    'forum': 'sqlite:///forum.db'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'antelope'
with app.app_context():
    db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# with app.app_context():
#     db.create_all()

# Your models for the first database

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"User(role={self.role}, username={self.username}, password={self.password}, " \
f"name={self.name}, age={self.age}, gender={self.gender})"

# Your models for the second database
class Question(db.Model):
    __bind_key__ = 'forum'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    flag = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"question = {self.question}, flag={self.flag}"

# Your forms and routes go here
# ...

class AskQuestionForm(FlaskForm):
    question=StringField('Question' , validators=[InputRequired(), Length(min=4,max=20)],render_kw={"placeholder":"Enter your question"})
    submit=SubmitField('Submit')

class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(), Length(min=4,max=20)])
    password=PasswordField(validators=[InputRequired(), Length(min=4,max=20)])
    submit=SubmitField("Login")

    def validate_usrnme(self,username):
        existing = User.query.filter_by(username=username.data).first()
        if (existing==None):
            raise ValidationError("This username does not exit. Please retry.")

class RegisterForm(FlaskForm):
    role = SelectField('Role', choices=[('Doctor', 'Doctor'), ('Patient', 'Patient'), ('Staff', 'Staff')],validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    #confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=50)])
    age = StringField('Age', validators=[InputRequired(), Length(min=1, max=3)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_username(self,username):
        existing = User.query.filter_by(username=username.data).first()
        if (existing!=None):
            raise ValidationError("This username already exists. Please choose again.")
            

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/doctor_home')
def doctor_home():
    return render_template('doctor_home.html')

@app.route('/login/patient_home')
def patient_home():
    return render_template('patient_home.html')

@app.route('/login/staff_home')
def staff_home():
    return render_template('staff_home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the username and password values from the form
        username = form.username.data
        password = form.password.data

        # Validate the username and password against a user database
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return render_template('aboutus.html')
        else:
            return render_template('index.html')

    return render_template('login.html',form=form)

@app.route('/login_submit', methods=['GET','POST'])
def login_submit():
    if request.method== 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            if(user.role=='Doctor'):
                return redirect(url_for('doctor_home'))
            elif(user.role=='Patient'):
                return redirect(url_for('patient_home'))
            else:
                return redirect(url_for('staff_home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html',form=request.form)
        

@app.route('/register',methods= ['GET','POST'])
def register():
    flag=1
    form = RegisterForm()
    if (form.validate_on_submit()):
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        #hashed_password2 = bcrypt.generate_password_hash(form.confirm_password.data)
        new_user = User(role=form.role.data,username=form.username.data,password=hashed_password,name=form.name.data,age=form.age.data,gender=form.gender.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form,flag=flag)

@app.route('/register_submit', methods=['POST'])
def register_submit():
    flag=1
    if request.method == 'POST':
        role = request.form["role"]
        username=request.form["username"]
        password=request.form["password"]
        name=request.form["name"]
        age=request.form["age"]
        gender=request.form["gender"]
        user = User.query.filter_by(username=username).first()
        if(user!=None):
            flag = 0
        else:
            new_user = User(role=role,username=username,password=password,name=name,age=age,gender=gender)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html',form=request.form, flag=flag)

@app.route('/reset')
def reset_flag():
    flag = 1  # set flag to a value that won't trigger the alert message
    return redirect(url_for('register'))

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/healthandinformation')
def healthinfo():
    return render_template('healthandinformation.html')

@app.route('/login/askdoctor', methods=['GET', 'POST'])
def askdoctor():
    form = AskQuestionForm()
    if form.validate_on_submit():
        question = form.question.data
        flag = form.flag.data
        new_question = Question(question=question,flag=flag)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('askdoctor'))
    url = 'http://127.0.0.1:5000/api/recommender' # this is the URL used for api recommender, change if needed
    response = requests.post(url)
    data = json.loads(response.content)['items']
    return render_template('forum.html',form=form, data=data)

@app.route('/login/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        question = request.form["qn"]
        flag = request.form["fl"]
        new_question = Question(question=question,flag=flag)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('askdoctor'))
    return redirect(url_for('askdoctor'))



@app.route('/login/forum', methods=['GET', 'POST'])
def doctorforum():
    url = 'http://127.0.0.1:5000/api/recommender' # this is the URL used for api recommender, change if needed
    response = requests.post(url)
    ranked_items = json.loads(response.content)['items']
    return render_template('doctor_forum.html', data=ranked_items)


@app.route('/api/recommender', methods=['POST'])
def apiRecommender():
    conn = sqlite3.connect('instance/forum.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM question')
    data = cur.fetchall()
    user = User.query.first()
    role = user.role
    if role == 'Doctor':
        data = sorted(data, key=lambda x: x[2], reverse=True) # make this x[2] for the actual recommender
    elif role == 'Patient':
        data = sorted(data, key=lambda x: x[2], reverse=False) # make this x[2] for the actual recommender
    else:
        data = data
    return jsonify({'items': data})


if __name__ == '__main__':
    app.run(debug=True)
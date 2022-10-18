from flask import Flask, render_template, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from unicodedata import category
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask import flash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
db = SQLAlchemy(app)  #creates database
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  #connects to database

app.config['SECRET_KEY'] = 'thisisasecretkey'
key = 'secret'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length
    (min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length
    (min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            flash("That username already exists. Please choose a different one.", category='error' )
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length
    (min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length
    (min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://localhost:5000/route?token=ackbkckjckvcsad
        # token = request.headers['token'] # it should be passed in headers token as key and value
        if not token:
            return jsonify({'message':'Token is missing!'}), 403
        try:
            data = jwt.decode(token, key, algorithms="HS256")
        except:
            return jsonify({'message':'Token is Invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        token = jwt.encode({'user':form.username.data, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5)}, key)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("successfully logged in!!", category = 'success')
                # return redirect(url_for('dashboard'))
                return jsonify({"Data":user})
            else:
                flash("Incorrect password!!", category = 'error')
    return render_template('login.html', form=form)




@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@token_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
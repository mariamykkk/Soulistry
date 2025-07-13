from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import Config
from forms import RegisterForm, LoginForm, BioForm
from models import db, User, Melody
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists.')
            return redirect(url_for('register'))
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data),
                    is_admin=False)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('form'))
        flash('Invalid credentials.')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    form = BioForm()
    if form.validate_on_submit():
        melody = Melody(
            blood_type=form.blood_type.data,
            eye_color=form.eye_color.data,
            origin=form.origin.data,
            mood=form.mood.data,
            user_id=current_user.id
        )
        db.session.add(melody)
        db.session.commit()
        return redirect(url_for('result', melody_id=melody.id))
    return render_template('form.html', form=form)

@app.route('/result/<int:melody_id>')
@login_required
def result(melody_id):
    melody = Melody.query.get_or_404(melody_id)
    mood = melody.mood.lower()
    if "happy" in mood:
        output = "Your melody is bright and energetic in C major."
    elif "sad" in mood:
        output = "Your melody is slow and soft in A minor."
    else:
        output = "Your melody is reflective and calm in D minor."
    return render_template('result.html', melody=melody, music_output=output)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash("Access denied.")
        return redirect(url_for('home'))
    melodies = Melody.query.all()
    return render_template('admin.html', melodies=melodies)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, redirect
from data import db_session, jobs, users
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat assword', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    
    submit = SubmitField('Войти')

app = Flask(__name__, template_folder="template/")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    global actions
    return render_template("works.html", actions=actions, enumerate=enumerate)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global session
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if session.query(User).filter(User.email == form.username.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = int(form.age.data)
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.username.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/register')
    return render_template('register.html', title='Регистрация', form=form)



def main():
    global actions, session, User
    try:
        db_session.global_init("db/blogs.sqlite")
    
        session = db_session.create_session()

        Jobs = jobs.Jobs
        User = users.User
        
        actions = []
        
        for job in session.query(Jobs).all():
            user = session.query(User).filter(User.id == job.team_leader).first()
            actions.append((job.job, ' '.join([user.name, user.surname]), job.work_size, job.collaborators, job.is_finished))
    
        app.run(debug=False)
    except Exception as s:
        input(s)


actions = None
session = None
User = None

if __name__ == '__main__':
    main()
from flask import Flask, flash, redirect, render_template, url_for
from flask_wtf.csrf import CSRFProtect

from registration_form_with_db.form import RegistrationForm
from registration_form_with_db.model import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = b'7bb2c87f65986c3843ea8c6d1750beee37bb0925e362df20034dc8757f1aae28'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/users.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data)
        # установку пароля делаем через отдельный метод класса User
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Успешная регистрация пользователя', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

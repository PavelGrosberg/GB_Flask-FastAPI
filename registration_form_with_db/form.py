from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from registration_form_with_db.model import User


# добавлена проверка наличия/отсутствия пользователя с одинаковым email в нашей базе данных
# поля с подтверждением пароля по условиям задачи нет, поэтому поле для сравнения пароля мы добавлять не будем
class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Отправка данных')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Пользователь с таким email уже существует')

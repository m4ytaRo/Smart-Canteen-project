from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    login = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField(
        'Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class EnterForm(FlaskForm):
    login = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class AboutUser(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('Изменить данные')
    button_out = SubmitField('Выход')


class BasketForm(FlaskForm):
    mark = SelectField('Оценка', choices=[('1', 'Отвратительно'), ('2', 'Плохо'),
                                              ('3', 'Удовлетворительно'), ('4', 'Хоршо'),
                                              ('5', 'Прекрасно')])
    evaluate = SubmitField('Оценить')
    pay = SubmitField('Оплатить')
    button_delete = SubmitField('Отменить заказ')

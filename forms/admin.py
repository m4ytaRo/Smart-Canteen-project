from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class AboutAdmin(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Изменить данные') 
    button_out = SubmitField('Выход')


class AddMealLibrary(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    type = SelectField('Тип', choices=[('1', 'Напиток'), ('2', 'Завтрак'),
                                        ('3', 'Обед'), ('4', 'Ужин')])
    submit = SubmitField('Добавить')


class MealChangeForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    type = SelectField('Тип', choices=[('1', 'Напиток'), ('2', 'Завтрак'),
                                        ('3', 'Обед'), ('4', 'Ужин')])
    submit = SubmitField('Изменить')
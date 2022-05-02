import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'UsersId'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    image = sqlalchemy.Column(sqlalchemy.String, default='img/system/standart.png')
    address = sqlalchemy.Column(sqlalchemy.String, default='')

    meal = orm.relation('MealsLibrary', back_populates='canteen')
    menu = orm.relation('EverydayMenu', back_populates='canteen')
    statistic = orm.relation('Statistic', back_populates='canteen')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


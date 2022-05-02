import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import datetime


class EverydayMenu(SqlAlchemyBase):
    __tablename__ = 'EverydayMenu'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now().date())
    meal_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('MealsLibrary.id'))
    count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    canteen_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey('UsersId.id'))
    
    meal = orm.relation('MealsLibrary')
    canteen = orm.relation('User')


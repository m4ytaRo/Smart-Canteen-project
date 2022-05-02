import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class MealsLibrary(SqlAlchemyBase):
    __tablename__ = 'MealsLibrary'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    type_id = sqlalchemy.Column(sqlalchemy.Integer)
    canteen_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey('UsersId.id'))

    canteen = orm.relation('User')
    menu = orm.relation('EverydayMenu', back_populates='meal')

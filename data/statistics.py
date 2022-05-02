import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Statistic(SqlAlchemyBase):
    __tablename__ = 'Statistics'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    mark = sqlalchemy.Column(sqlalchemy.Integer, default=5)
    canteen_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('UsersId.id'))
    
    canteen = orm.relation('User')

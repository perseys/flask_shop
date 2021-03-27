import datetime

import sqlalchemy
from flask import url_for
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Good(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'goods'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    article = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<Товар> {self.title} [{self.article}]'

    def getImage(self, app):
        img = None
        if not self.__good['image']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/good.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найдено изображение по умолчанию: " + str(e))
        else:
            img = self.__good['image']

        return img

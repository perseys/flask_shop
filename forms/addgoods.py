from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, FloatField, TextAreaField
from wtforms.validators import DataRequired


class AddGoodsForm(FlaskForm):
    title = StringField('Наименование', validators=[DataRequired()])
    article = StringField('Артикул', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    # image = StringField('Описание', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired()])
    is_active = BooleanField('Активный', validators=[DataRequired()])
    # created_date = DateField('Дата создания', validators=[DataRequired()])
    # modified_date = DateField('Дата изменения', validators=[DataRequired()])

    submit = SubmitField('Добавить')

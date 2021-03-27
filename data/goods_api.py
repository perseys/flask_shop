import flask
from flask import jsonify, make_response

from . import db_session
from .goods import Good

blueprint = flask.Blueprint(
    'goods_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/goods')
def get_goods():
    db_sess = db_session.create_session()
    goods = db_sess.query(Good).all()
    return jsonify(
        {
            'goods':
                [item.to_dict(only=('title', 'article', 'description', 'price'))
                 for item in goods]
        }
    )

@blueprint.route('/api/goods/<int:goods_id>', methods=['GET'])
def get_one_news(goods_id):
    db_sess = db_session.create_session()
    goods = db_sess.query(Good).get(goods_id)
    if not goods:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'goods': goods.to_dict(only=(
                'title', 'article', 'description', 'price', 'is_active', 'created_date', 'modified_date'))
        }
    )

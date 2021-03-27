import parser

from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.goods import Good


def abort_if_goods_not_found(goods_id):
    session = db_session.create_session()
    goods = session.query(Good).get(goods_id)
    if not goods:
        abort(404, message=f"Goods {goods_id} not found")


class GoodsResource(Resource):
    def get(self, goods_id):
        abort_if_goods_not_found(goods_id)
        session = db_session.create_session()
        goods = session.query(Good).get(goods_id)
        return jsonify(
            {'goods': goods.to_dict(
                only=('title',
                      'article',
                      'description',
                      'price',
                      'is_active',
                      'created_date',
                      'modified_date'
                      )
            )
            }
        )

    def delete(self, goods_id):
        abort_if_goods_not_found(goods_id)
        session = db_session.create_session()
        goods = session.query(Good).get(goods_id)
        session.delete(goods)
        session.commit()
        return jsonify({'success': 'OK'})


class GoodsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        goods = session.query(Good).all()
        return jsonify({'goods': [item.to_dict(
            only=('title', 'article', 'description', 'price', 'is_active', 'created_date','modified_date'
                  )) for item in goods]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        goods = Good(
            title=args['title'],
            article=args['article'],
            description=args['description'],
            price=args['price'],
            created_date=args['created_date'],
            modified_date=args['modified_date'],
            is_active=args['is_active']
        )
        session.add(goods)
        session.commit()
        return jsonify({'success': 'OK'})

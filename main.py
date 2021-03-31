from datetime import datetime

from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_login import login_user, logout_user, LoginManager, login_required
from flask_restful import abort, Api

from data import db_session, goods_api, goods_resources
from data.goods import Good
from data.users import User
# from forms.user import RegisterForm
from forms.addgoods import AddGoodsForm
from forms.loginform import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
# app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'kjOsqhCsNKtAfaQ8ODrTerh5LWqMkfkNZ1QxyCV5f1TKwTGaKl'

login_manager = LoginManager()
login_manager.init_app(app)

# Flask-RESTful
api = Api(app)
# для списка объектов
api.add_resource(goods_resources.GoodsListResource, '/api/v2/goods')

# для одного объекта
api.add_resource(goods_resources.GoodsResource, '/api/v2/goods/<int:goods_id>')


def main():
    # breakpoint()
    db_session.global_init("db/shop.db")
    app.register_blueprint(goods_api.blueprint)

    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    goods = db_sess.query(Good).filter(Good.is_active == True)
    # goods = db_sess.query(Good).all()

    return render_template("index.html", goods=goods, title='Товары')


@app.route("/add_good", methods=['GET', 'POST'])
def add_good():
    form_add = AddGoodsForm()
    if form_add.validate_on_submit():
        db_sess = db_session.create_session()
        goods = Good(
            title=form_add.title.data,
            article=form_add.article.data,
            description=form_add.description.data,
            price=form_add.price.data,
            is_active=form_add.is_active.data
        )
        db_sess.add(goods)
        db_sess.commit()
        return redirect('/')
    return render_template('add_good.html', title='Добавление товара', bt_title='Добавить товар', form=form_add)


@app.route('/goods/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_goods(id):
    form = AddGoodsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        goods = db_sess.query(Good).filter(Good.id == id).first()
        if goods:
            form.title.data = goods.title
            form.article.data = goods.article
            form.description.data = goods.description
            form.price.data = goods.price
            form.is_active.data = goods.is_active
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Good).filter(Good.id == id).first()
        if goods:
            goods.title = form.title.data
            goods.article = form.article.data
            goods.description = form.description.data
            goods.price = form.price.data
            goods.is_active = form.is_active.data
            goods.modified_date = datetime.now()
            db_sess.merge(goods)
            return redirect('/')
        else:
            abort(404)
    return render_template('add_good.html', title='Редактирование товара', bt_title='Изменить товар', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Вход', message="Неправильный email или пароль", form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация нового покупателя', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация нового покупателя', form=form,
                                   message="Такой логин/email уже есть")
        user = User(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация нового покупателя', form=form)


if __name__ == '__main__':
    main()

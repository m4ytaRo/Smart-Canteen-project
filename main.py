from flask import Flask, render_template, request, send_from_directory, url_for, session, make_response
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.utils import redirect, secure_filename
import os
import math

from data import db_session
from data.users import User
from data.statistics import Statistic
from data.meals import MealsLibrary
from data.menu import EverydayMenu

from forms.user import EnterForm, AboutUser, BasketForm
from forms.admin import AboutAdmin, AddMealLibrary, MealChangeForm


UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'static/img/')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("database.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/delete-from-basket/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_from_basket(id):
    basket = request.cookies.get('basket', 0)
    res = make_response(
        '<script>document.location.href = document.referrer</script>')
    if basket:
        db_sess = db_session.create_session()
        menu = db_sess.query(EverydayMenu).filter(EverydayMenu.meal_id == id).first()
        menu.count -= 1
        db_sess.commit()

        basket = list(map(int, basket.split()))
        basket.pop(basket.index(id))
        if basket:
            basket = ' '.join(list(map(str, basket)))
            res.set_cookie('basket', basket,
                           max_age=60 * 60 * 24 * 365 * 2)
        else:
            res.set_cookie('basket', '1', max_age=0)
    return res


@app.route('/basket', methods=['GET', 'POST'])
@login_required
def basket_prof():
    form = BasketForm()
    db_sess = db_session.create_session()
    indexes = request.cookies.get('basket', 0)

    if indexes:
        indexes = indexes.split()
        meals = db_sess.query(MealsLibrary).filter(
            MealsLibrary.id.in_(indexes))
        canteen = meals[0].canteen_id
        if form.validate_on_submit():
            if form.evaluate.data:
                stat = db_sess.query(Statistic).filter(
                    Statistic.canteen_id == canteen).first()
                if not stat:
                    stat = Statistic()
                    stat.canteen_id = canteen
                    stat.mark = form.mark.data
                    db_sess.add(stat)
                    db_sess.commit()
                else:
                    stat.mark = math.floor((stat.mark + int(form.mark.data)) / 2)
                    db_sess.commit()
            res = make_response(redirect('/'))
            res.set_cookie('basket', '1', max_age=0)
            for meal in meals:
                menu = db_sess.query(EverydayMenu).filter(
                    EverydayMenu.meal_id == meal.id).first()
                menu.count -= 1
                db_sess.commit()
            return res
        return render_template('basket.html', title='Заказ',
                               file='css/basket.css', meals=meals, form=form)
    return render_template('basket.html', title='Заказ',
                           file='css/basket.css', form=form)


@app.route('/add-to-basket/<int:id>', methods=['GET', 'POST'])
@login_required
def add_to_basket(id):
    basket = request.cookies.get('basket', 0)
    db_sess = db_session.create_session()
    res = make_response(
        '<script>document.location.href = document.referrer</script>')
    if basket and str(id) not in basket:
        basket += f' {id}'
        res.set_cookie("basket", basket,
                       max_age=60 * 60 * 24 * 365 * 2)

        menu = db_sess.query(EverydayMenu).filter(
            EverydayMenu.meal_id == id).first()
        menu.count += 1
        db_sess.commit()
    elif not basket:
        res.set_cookie("basket", str(id),
                       max_age=60 * 60 * 24 * 365 * 2)

        menu = db_sess.query(EverydayMenu).filter(
            EverydayMenu.meal_id == id).first()
        menu.count += 1
        db_sess.commit()
    return res


@app.route('/info/<int:id>')
@login_required
def info(id):
    db_sess = db_session.create_session()
    meal = db_sess.query(MealsLibrary).filter(MealsLibrary.id == id).first()
    if meal:
        return render_template('info_meal.html', file='css/info_meal.css',
                               title='Информация о блюде', meal=meal)
    else:
        abort(404)


@app.route('/delete-meal-menu/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_meal_menu(id):
    db_sess = db_session.create_session()
    menu_meal = db_sess.query(EverydayMenu).filter(
        EverydayMenu.meal_id == id).first()
    db_sess.delete(menu_meal)
    db_sess.commit()
    return redirect('/')


@app.route('/add-fast-menu/<int:id>', methods=['GET', 'POST'])
@login_required
def add_meal_to_fastmenu(id):
    db_sess = db_session.create_session()
    # meal = db_sess.query(MealsLibrary).filter(MealsLibrary.id == id).first()
    check_count = db_sess.query(EverydayMenu).filter(
        EverydayMenu.meal_id == id).first()
    if check_count:
        return redirect('/')

    else:
        meal_to_menu = EverydayMenu()
        meal_to_menu.meal_id = id
        meal_to_menu.canteen_id = current_user.id
        db_sess.add(meal_to_menu)
        db_sess.commit()
        return redirect('/')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def meal_delete(id):
    db_sess = db_session.create_session()
    meal = db_sess.query(MealsLibrary).filter(MealsLibrary.id == id,
                                              MealsLibrary.canteen_id == current_user.id
                                              ).first()
    if meal:
        db_sess.delete(meal)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def meal_change(id):
    form = MealChangeForm()
    db_sess = db_session.create_session()
    meal = db_sess.query(MealsLibrary).filter(MealsLibrary.id == id,
                                              MealsLibrary.canteen_id == current_user.id
                                              ).first()
    if form.validate_on_submit():
        meal.name = form.name.data
        meal.description = form.description.data
        meal.price = form.price.data
        meal.type_id = form.type.data

        image = request.files.get('image')
        if image:
            path = os.path.join(os.path.dirname(__file__), f'static/{meal.image}')
            os.remove(path)
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_PATH, filename))
            file = f'img/{filename}'
            meal.image = file

        db_sess.commit()
        return render_template('change_meal.html', title='Изменение блюда',
                               form=form, file='css/change_meal.css',
                               meal=meal, message='Данные изменены')

    if meal:
        form.description.data = meal.description
        return render_template('change_meal.html', title='Изменение блюда',
                               form=form, file='css/change_meal.css',
                               meal=meal)
    else:
        abort(404)
    return redirect('/')


@login_required
@app.route('/add-meal-lib', methods=['GET', 'POST'])
def add_meal():
    form = AddMealLibrary()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        meal = MealsLibrary()
        meal.name = form.name.data
        meal.description = form.description.data
        meal.price = form.price.data
        meal.type_id = form.type.data
        meal.canteen_id = current_user.id

        image = request.files.get('image')
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_PATH, filename))
            file = f'img/{filename}'
            meal.image = file

            db_sess.add(meal)
            db_sess.commit()
            return render_template('add_meal_lib.html', form=form,
                                   title='Добавление блюда в меню',
                                   file='css/add_meal_lib.css',
                                   message='Блюдо добавлено')
        else:
            return render_template('add_meal_lib.html', form=form,
                                   title='Добавление блюда в меню',
                                   file='css/add_meal_lib.css',
                                   message='Выберите изображение!')

    return render_template('add_meal_lib.html', form=form,
                           file='css/add_meal_lib.css',
                           title='Добавление блюда в меню')


@app.route('/canteens/<int:id>', methods=['GET', 'POST'])
@login_required
def canteen(id):
    db_sess = db_session.create_session()
    canteen = db_sess.query(User).filter(User.id == id).first()
    meals = db_sess.query(MealsLibrary).filter(
        MealsLibrary.canteen_id == id)
    menu = db_sess.query(EverydayMenu).filter(EverydayMenu.canteen_id == id)
    basket = request.cookies.get("basket", [])
    if basket:
        basket = list(map(int, basket.split()))
    return render_template('menu.html', title='Выбор блюд',
                           file='css/menu.css',
                           meals=meals, menu=menu, canteen=canteen,
                           basket=basket, count=len(basket))


@app.route('/', methods=['GET', 'POST'])
def main():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if current_user.type == 0:
            marks = db_sess.query(Statistic)
            canteens = db_sess.query(User).filter(User.type == 1)
            basket = request.cookies.get('basket', 0)
            return render_template('main_user.html', title='Умная столовая',
                                   file='css/main_user.css', canteens=canteens,
                                   basket=basket, marks=marks)
        else:
            meals = db_sess.query(MealsLibrary).filter(
                MealsLibrary.canteen_id == current_user.id)
            menu = db_sess.query(EverydayMenu).filter(
                EverydayMenu.canteen_id == current_user.id)
            mark = db_sess.query(Statistic).filter(Statistic.canteen_id == current_user.id).first()
            return render_template('main_admin.html', title='Умная столовая',
                                   file='css/main_admin.css', meals=meals,
                                   menu=menu, mark=mark)
    return render_template('main.html', title='Умная столовая',
                           file='css/main.css')


@app.route('/about_admin', methods=['GET', 'POST'])
@login_required
def about_admin():
    form = AboutAdmin()
    if form.validate_on_submit():
        if form.button_out.data:
            return redirect('/logout')
        else:
            db_sess = db_session.create_session()
            check = db_sess.query(User).filter(
                User.login == form.login.data, User.id != current_user.id).first()
            if check:
                return render_template('about_admin.html', title='О пользователе',
                                       file='css/about_admin.css', form=form,
                                       message='Такой пользователь уже есть')
            admin = db_sess.query(User).filter(
                User.login == current_user.login).first()
            admin.name = form.name.data
            admin.login = form.login.data
            admin.address = form.address.data

            image = request.files.get('image')
            if image:
                path = os.path.join(os.path.dirname(__file__), f'static/{current_user.image}')
                os.remove(path)
                filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_PATH, filename))
                file = f'img/{filename}'
                admin.image = file

            db_sess.commit()
            login_user(admin, remember=True)
            return render_template('about_admin.html', title='О пользователе',
                                   file='css/about_admin.css', form=form,
                                   message='Данные изменены')
    return render_template('about_admin.html', title='О пользователе',
                           file='css/about_admin.css', form=form)


@app.route('/about_user', methods=['GET', 'POST'])
@login_required
def about_user():
    form = AboutUser()
    if form.validate_on_submit():
        if form.button_out.data:
            return redirect('/logout')
        else:
            db_sess = db_session.create_session()
            check = db_sess.query(User).filter(
                User.login == form.login.data, User.id != current_user.id).first()
            if check:
                return render_template('about_user.html', title='О пользователе',
                                       file='css/about_user.css', form=form,
                                       message='Такой пользователь уже есть')
            user = db_sess.query(User).filter(
                User.login == current_user.login).first()
            user.name = form.name.data
            user.surname = form.surname.data
            user.login = form.login.data
            db_sess.commit()
            login_user(user, remember=True)
            return render_template('about_user.html', title='О пользователе',
                                   file='css/about_user.css', form=form,
                                   message='Данные изменены')

    return render_template('about_user.html', title='О пользователе',
                           file='css/about_user.css', form=form)


@app.route('/enter', methods=['GET', 'POST'])
def enter():
    form = EnterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect('/')
        return render_template('enter.html', title='Вход',
                               file='css/enter.css',
                               form=form,
                               message='Неправильный логин или пароль!')
    return render_template('enter.html', title='Вход',
                           file='css/enter.css', form=form)


# @app.route('/')

# app.run()

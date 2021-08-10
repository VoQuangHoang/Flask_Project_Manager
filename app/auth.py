"""Auth controller"""
from flask import (Blueprint, render_template, url_for, redirect,request, flash,
                    session, abort, current_app)
from flask_login import login_required, logout_user, current_user, login_user
from flask_wtf import csrf
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import SignupForm, LoginForm, ChangePassword
from . import db, login_manager
from .models import User, Role, Group, Device, User_device_history
import ast

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """Login the user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password,password=form.password.data):
            if user.role_id == 1:
                login_user(user)
                session.permanent = True # set timeout
                return redirect(url_for('main.index'))
            flash('Accept denied! Check the permissions for your role')
            return redirect(url_for('auth.login'))
        flash('「アカウント名」または「パスワード」は不正です。')
        return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))


@auth.route("/logout")
@login_required
def logout():
    """User log-out"""
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/create-user', methods=['GET'])
@login_required
def create():
    """Redirect to signup page"""
    form = SignupForm(request.form)
    devices = Device.query.all()

    return render_template('add.html', form=form,devices=devices)


@auth.route('/confirm', methods=['POST', 'GET'])
@login_required
def confirm():
    """Confirm the user to add new or update"""
    form = SignupForm(request.form)
    devices = Device.query.all()
    group_by_id = Group.query.get(form.group.data)

    device_his_id = request.form.getlist('dev_his_id')
    devicess = []
    start_date = []
    end_date = []
    row_device = []

    for i in request.form:
        devicess.append(request.form[i]) if 'device' in i else None
        start_date.append(request.form[i]) if 'date_start' in i else None
        end_date.append(request.form[i]) if 'date_end' in i else None

    if devicess != ['']:
        for i in range(len(devicess)):
            device_by_id = Device.query.get(devicess[i])
            device_name = device_by_id.device_name
            row_device.append([devicess[i],device_name,start_date[i],end_date[i],device_his_id[i]])

    id_user = form.id.data
    user = db.session.query(User,User.user_id, Group.group_name, Role.role_id, Role.role_name).join(
                    Group).join(Role).filter(User.user_id == id_user).first()

    if id_user != '':
        form.email.data = user.User.email
        form.password.data = 'default'
        form.confirm.data = 'default'

    if form.validate_on_submit():
        if id_user != '':
            return render_template('confirm.html',form=form,row_device=row_device,
                                    action="update/"+id_user, group_by_id=group_by_id)
        else:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                return render_template('confirm.html',form=form,row_device=row_device,
                                    action="add", group_by_id=group_by_id)
            flash('「アカウント名」は既に存在しています。')
            return render_template('add.html', form=form, user=user, devices=devices)
    return render_template('add.html', form=form, user=user,devices=devices)

@auth.route('/add', methods=['POST'])
@login_required
def add():
    """Add a user"""
    try:
        if request.method == 'POST':
            user_add = User(
                group_id = request.form['group'],
                role_id = request.form['role'],
                email = request.form['email'],
                password = generate_password_hash(request.form['password'],method='sha256'),
                persional_email = request.form['persional_email'],
                full_name = request.form['full_name'],
                full_name_kana = request.form['full_name_kana'],
                gender = request.form['gender'],
                tel = request.form['tel'],
                birthday = request.form['birthday'],
                onboard_date = db.func.now(),
            )
            db.session.add(user_add)
            db.session.flush()
            list_device = ast.literal_eval(request.form['device'])
            if list_device != []:
                for device in list_device:
                    device_add = User_device_history(
                        user_id = user_add.user_id,
                        device_id = device[0],
                        is_deleted = 0,
                        start_date = device[2],
                        end_date = device[3]
                    )
                    db.session.add(device_add)
            db.session.commit()
            db.session.close()
            flash('ユーザの登録が完了しました', 'success')
            return redirect(url_for('main.notification'))
        return redirect(url_for('auth.confirm'))
    except:
        flash('システムエラーが発生しました。', 'danger')
        return redirect(url_for('main.notification'))


@auth.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Redirect to the edit page"""
    user = db.session.query(User,User.user_id, Group.group_name, Role.role_id, Role.role_name).join(
                    Group).join(Role).filter(User.user_id == id).first()
    if user is None:
        flash('検該当するユーザは存在していません。', 'danger')
        return redirect(url_for('main.notification'))

    form = SignupForm(object=user)

    devices = Device.query.all()

    devices_by_id = (db.session.query(User_device_history, Device.device_name, Device.device_id)
                .join(Device).filter(User_device_history.user_id == id).all())

    form.email.data = user.User.email
    form.full_name.data = user.User.full_name
    form.full_name_kana.data = user.User.full_name_kana
    form.role.data = str(user.User.role_id)
    form.group.data = str(user.User.group_id)
    form.gender.data = user.User.gender
    form.birthday.data = user.User.birthday
    form.persional_email.data = user.User.persional_email
    form.tel.data = user.User.tel
    form.id.data = user.User.user_id
    return render_template('add.html', user=user, form=form,
                        devices=devices, devices_by_id=devices_by_id)


@auth.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    """Update a user"""
    user = User.query.get(id)
    if user is None:
        flash('該当するユーザは存在していません。', 'danger')
        return redirect(url_for('main.notification'))
    try:
        if request.method == 'POST':
            user.group_id = request.form['group']
            user.role_id = request.form['role']
            user.persional_email = request.form['persional_email']
            user.full_name = request.form['full_name']
            user.full_name_kana = request.form['full_name_kana']
            user.gender = request.form['gender']
            user.tel = request.form['tel']
            user.birthday = request.form['birthday']
            list_device = ast.literal_eval(request.form['device'])
            for device in list_device:
                if device[4] == '':
                    device_add = User_device_history(
                        user_id = id,
                        device_id = device[0],
                        is_deleted = 0,
                        start_date = device[2],
                        end_date = device[3]
                    )
                    db.session.add(device_add)
                else:
                    device_his = User_device_history.query.get(device[4])
                    device_his.device_id = device[0]
                    device_his.start_date = device[2]
                    device_his.end_date = device[3]
            db.session.commit()
            db.session.close()
            flash('ユーザの更新が完了しました。', 'success')
            return redirect(url_for('main.notification'))
        return redirect(url_for('auth.confirm'))
    except:
        flash('システムエラーが発生しました。', 'danger')
        return redirect(url_for('main.notification'))

@auth.route('/editpassword/<int:id>', methods=['GET'])
@login_required
def editpassword(id):
    user = User.query.get(id)
    form = ChangePassword(request.form)
    if user is None:
        flash('該当するユーザは存在していません。', 'danger')
        return redirect(url_for('main.notification'))
    try:
        return render_template('change_password.html', form=form, id=id)
    except:
        flash('システムエラーが発生しました。', 'danger')
        return redirect(url_for('main.notification'))

@auth.route('/updatepassword/<int:id>', methods=['POST'])
@login_required
def updatepassword(id):
    form = ChangePassword(request.form)
    user = User.query.get(id)
    if user is None:
        flash('該当するユーザは存在していません。', 'danger')
        return redirect(url_for('main.notification'))
    try:
        if form.validate_on_submit():
            user.password = generate_password_hash(form.password.data, method="sha256")
            db.session.commit()
            db.session.close()
            flash('ユーザの更新が完了しました。', 'success')
            return redirect(url_for('main.notification'))
        return render_template('change_password.html', form=form, id=id)
    except:
        flash('システムエラーが発生しました。', 'danger')
        return redirect(url_for('main.notification'))


@auth.route('/delete/<int:id>', methods=['GET','DELETE'])
@login_required
def delete(id):
    """Delete a user"""
    user_to_delete = User.query.get(id)
    if user_to_delete is None:
        flash('該当するユーザは存在していません。', 'danger')
        return render_template('notification.html')
    try:
        if user_to_delete.role_id == 1:
            flash("Can't delete user with role Super User", 'danger')
            return redirect(url_for('main.notification'))
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('ユーザの更新が完了しました。', 'success')
        return redirect(url_for('main.notification'))
    except:
        flash('システムエラーが発生しました。', 'danger')
        return redirect(url_for('main.notification'))

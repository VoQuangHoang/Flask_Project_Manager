from flask import Blueprint, render_template, url_for, redirect,request, flash, session
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import SignupForm, LoginForm
from . import db, login_manager
from .models import User, Role, Group, Device, User_device_history
import ast

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password,password=form.password.data):
            if user.role_id == 1:
                login_user(user)
                session.permanent = True
                return redirect(url_for('main.index'))
            flash('Accept denied for your role')
            return redirect(url_for('auth.login'))
        flash('Invalid username/password combination')
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
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
@login_required
def signup():
    form = SignupForm(request.form)
    
    form.group.choices = [("", "選択してください")]+[(str(g.group_id), g.group_name) for g in Group.query.all()]
    form.role.choices = [("", "選択してください")]+[(str(r.role_id), r.role_name) for r in Role.query.all()]
    form.gender.choices = [(1,"Male"), (0,"Female")]
    devices = Device.query.all()

    return render_template('add.html', form=form,devices=devices)


@auth.route('/confirm', methods=['POST', 'GET'])
@login_required
def confirm():
    form = SignupForm(request.form)
    form.group.choices = [("", "選択してください")]+[(str(g.group_id), g.group_name) for g in Group.query.all()]
    form.role.choices = [("", "選択してください")]+[(str(r.role_id), r.role_name) for r in Role.query.all()]
    form.gender.choices = [(1,"Male"), (0,"Female")]
    devices = Device.query.all()

    group_by_id = Group.query.get_or_404(form.group.data)

    device = request.form.getlist('device')
    date_start = request.form.getlist('date_start')
    date_end = request.form.getlist('date_end')
    device_his_id = request.form.getlist('device_his_id')

    row_device = []
    if device != ['']:
        for i in range(len(device)):
            device_by_id = Device.query.get_or_404(device[i])
            device_name = device_by_id.device_name
            row_device.append([device[i],device_name,date_start[i],date_end[i],device_his_id[i]])  
    print (row_device)

    idUser = form.id.data

    user = db.session.query(User,User.user_id, Group.group_name, Role.role_id, Role.role_name).join(
                    Group).join(Role).filter(User.user_id == idUser).first()

    if idUser != '':
        form.email.data = user.User.email
    
    if form.validate_on_submit():
        if idUser != '':
            return render_template('confirm.html',form=form,row_device=row_device, action="update/"+idUser, group_by_id=group_by_id)
        else:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                return render_template('confirm.html',form=form,row_device=row_device, action="add", group_by_id=group_by_id)
            flash('A user already exists with that email address.')
            return render_template('add.html', form=form, user=user, devices=devices)
    return render_template('add.html', form=form, user=user,devices=devices)


@auth.route('/add', methods=['POST'])
@login_required
def add():
    if request.method == 'POST':
        userAdd = User(
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
            onboard_date = db.func.now()
        )
        db.session.add(userAdd)
        db.session.flush()
        list_device = ast.literal_eval(request.form['device'])
        print (list_device)
        if list_device != []:
            for device in list_device:
                deviceAdd = User_device_history(
                    user_id = userAdd.user_id,
                    device_id = device[0],
                    is_deleted = 0,
                    start_date = device[2],
                    end_date = device[3]
                )
                db.session.add(deviceAdd)
        db.session.commit()
        db.session.close()
        flash('MSG001: ユーザの登録が完了しました')
        return redirect(url_for('main.notification'))
    return redirect(url_for('auth.confirm'))          
   

@auth.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = db.session.query(User,User.user_id, Group.group_name, Role.role_id, Role.role_name).join(
                    Group).join(Role).filter(User.user_id == id).first()
    form = SignupForm(object=user)

    form.group.choices = [("", "選択してください")]+[(str(g.group_id), g.group_name) for g in Group.query.all()]
    form.role.choices = [("", "選択してください")]+[(str(r.role_id), r.role_name) for r in Role.query.all()]
    form.gender.choices = [(1,"Male"), (0,"Female")]
    devices = Device.query.all()
    devices_by_id = (db.session.query(User_device_history, Device.device_name, Device.device_id)
                .join(Device).filter(User_device_history.user_id == id).all())

    form.email.data = user.User.email
    form.full_name.data = user.User.full_name
    form.full_name_kana.data = user.User.full_name_kana
    form.role.data = str(user.User.role_id)
    print(form.role.data)
    form.group.data = str(user.User.group_id)
    print(form.group.data)
    form.gender.data = user.User.gender
    form.birthday.data = user.User.birthday
    form.persional_email.data = user.User.persional_email
    form.tel.data = user.User.tel
    form.id.data = user.User.user_id
    return render_template('add.html', user=user, form=form, devices=devices, devices_by_id=devices_by_id)    


@auth.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.group_id = request.form['group']
        user.role_id = request.form['role']
        user.password = generate_password_hash(request.form['password'],method='sha256')
        user.persional_email = request.form['persional_email']
        user.full_name = request.form['full_name']
        user.full_name_kana = request.form['full_name_kana']
        user.gender = request.form['gender']
        user.tel = request.form['tel']
        user.birthday = request.form['birthday']
        list_device = ast.literal_eval(request.form['device'])
        for device in list_device:
            if device[4] == '':
                deviceAdd = User_device_history(
                    user_id = id,
                    device_id = device[0],
                    is_deleted = 0,
                    start_date = device[2],
                    end_date = device[3]
                )
                db.session.add(deviceAdd)
            else:
                device_his = User_device_history.query.get_or_404(device[4])
                device_his.device_id = device[0]
                device_his.start_date = device[2]
                device_his.end_date = device[3]
        db.session.commit()
        db.session.close()
        flash('MSG002: ユーザの更新が完了しました。')
        return redirect(url_for('main.notification'))
    return redirect(url_for('auth.confirm')) 


@auth.route('/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash('MSG003: ユーザの更新が完了しました。')
    return redirect(url_for('main.notification'))


@auth.route('/abc')
def abc():
    form = SignupForm(request.form)
    form.device.choices = [(d.device_id, d.device_name) for d in Device.query.all()]
    return render_template('testload.html', form=form)  


 
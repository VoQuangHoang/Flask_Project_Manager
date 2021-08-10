"""Main controller"""
import csv
import ast
from io import StringIO
from math import ceil
from flask import (Blueprint, g, flash, url_for, request, redirect, render_template,
    current_app, make_response, jsonify, json)
from flask_login import current_user, login_required
from . import db
from .models import User, Role, Group, User_device_history, Device
from datetime import datetime


main = Blueprint('main', __name__)

ROWS_PER_PAGE = 5

@main.route('/', methods=['GET'])
@login_required
def index():
    """Redirect to manager page"""
    groups = Group.query.all()
    page = request.args.get('page', 1, type=int)

    a = User.full_name.asc()
    b = Role.role_name.asc()
    c = User.onboard_date.asc()

    g.name = request.args.get('name','asc', type=str)
    g.role = request.args.get('role','asc', type=str)
    g.date = request.args.get('date','desc', type=str)

    if g.name == "desc":
        a = User.full_name.desc()
    if g.role == "desc":
        b = Role.role_name.desc()
    if g.date == "desc":
        c = User.onboard_date.desc()

    text = request.args.get('text', default="", type=str)
    groupname = request.args.get('groupname', default="", type=str)

    desc = '△▼'
    asc = '▲▽'

    # Export data to CSV
    query = db.session.query(User.user_id, User.full_name,Group.group_id, Group.group_name,
        Role.role_id,Role.role_name,User.email, User.tel, User.birthday, User.onboard_date
        ).join(Group).join(Role).filter(User.full_name.contains(text,autoescape=True)).filter(
        Group.group_name.like(f'%{groupname}%')).order_by(a,b,c).all()

    list_user2 = []
    for user in query:
        list_user2.append(User.to_json(user))

    # User to show
    querys = db.session.query(User, Group.group_name, Role.role_name).join(Group).join(
                        Role).filter(User.full_name.contains(text,autoescape=True)).filter(
                        Group.group_name.like(f'%{groupname}%')).order_by(a,b,c)
    users = querys.paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)

    return render_template('manager.html',current_user=current_user,asc=asc,desc=desc, users=users,
                        groups=groups, text = text,groupname = groupname,list_user = list_user2 ,
                        pagegroup = (ceil(users.page/3)-1), pagesgroup = (ceil(users.pages/3)-1))


@main.route('/download', methods=['POST'])
@login_required
def post():
    si = StringIO()
    field_names = ['user_id','full_name','group_id','group_name','role_id','role_name','email',
                'tel','birthday','onboard_date']
    cw = csv.DictWriter(si, fieldnames = field_names)
    list_user = ast.literal_eval(request.form['userquery'])
    cw.writeheader()
    cw.writerows(list_user)
    output = make_response(si.getvalue())
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    output.headers["Content-Disposition"] = "attachment; filename=user_export_"+time+".csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output

@main.route('/detail/<int:id>')
@login_required
def detail(id):
    """Redirect to the detail user page"""
    user = db.session.query(User, Group.group_name).join(Group).filter(User.user_id == id).first()
    devices_his = db.session.query(User_device_history, Device.device_name).join(
        Device).filter(User_device_history.user_id == id).all()
    if user:
        return render_template('detail.html', user=user, user_id = id, devices_his=devices_his)
    flash('検索条件に該当するユーザが見つかりません。', 'danger')
    return redirect(url_for('main.notification'))

@main.route('/notification')
def notification():
    """Redirect to the notification page"""
    return render_template('notification.html')

@main.route('/listdevice/<int:id>')
@login_required
def listdevice(id):
    """Redirect to the notification page"""
    devices_his = db.session.query(User_device_history, Device.device_name).join(
        Device).filter(User_device_history.user_id == id).all()
    return render_template('listdevice.html',devices_his=devices_his)
 
from flask import Blueprint, g
from flask.templating import render_template
from flask import request, redirect, render_template
from . import db
from math import ceil
from .models import User, Role, Group, User_device_history, Device
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

ROWS_PER_PAGE = 5


@main.route('/', methods=['GET'])
@login_required
def index():
    groups = Group.query.all()
    page = request.args.get('page', 1, type=int)

    a = User.full_name
    b = Role.role_name
    c = User.onboard_date

    g.name = request.args.get('name','asc', type=str)
    g.role = request.args.get('role','asc', type=str)
    g.date = request.args.get('date','desc', type=str)

    if g.name == "desc":
        a = User.full_name.desc()
    elif g.role == "desc":
        b = Role.role_name.desc()
    elif g.date == "desc":
        c = User.onboard_date.desc()

    text = request.args.get('text', default="", type=str)
    groupname = request.args.get('groupname', default="", type=str)

    desc = '△▼'
    asc = '▲▽'

    users = db.session.query(User, Group.group_name, Role.role_name).join(
                Group).join(Role).filter(User.full_name.contains(text,autoescape=True)).filter(
                Group.group_name.like(f'%{groupname}%')).order_by(a,b,c).paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
    return render_template('manager.html',current_user=current_user,asc=asc,desc=desc, users=users, groups=groups, text = text,groupname = groupname,
                            pagegroup = (ceil(users.page/3)-1), pagesgroup = (ceil(users.pages/3)-1))          


@main.route('/detail/<int:id>')
@login_required
def detail(id):
    user = db.session.query(User, Group.group_name).join(Group).filter(User.user_id == id).first()
    devices_his = db.session.query(User_device_history, Device.device_name).join(Device).filter(User_device_history.user_id == id).all()
    return render_template('detail.html', user=user, user_id = id, devices_his=devices_his)

@main.route('/notification')
@login_required
def notification():
    return render_template('notification.html')

  

"""Model data"""
from sqlalchemy import text
from flask_login import UserMixin
from datetime import datetime
from . import db

class Role(db.Model):
    __tablename__ = 'tbl_role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())
    create_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    update_at = db.Column(db.TIMESTAMP,server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False)

class Group(db.Model):
    __tablename__ = 'mst_group'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())
    create_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    update_at = db.Column(db.TIMESTAMP,server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False)

class Device(db.Model):
    __tablename__ = 'mst_devices'

    device_id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String(255), nullable=False)
    device_name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text())
    device_status = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    update_at = db.Column(db.TIMESTAMP,server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False)

class User(UserMixin,db.Model):
    __tablename__ = 'tbl_user'

    user_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('mst_group.group_id'), nullable=False)
    mst_group = db.relationship("Group")
    role_id = db.Column(db.Integer, db.ForeignKey('tbl_role.role_id'), nullable=False)
    tbl_role = db.relationship("Role")
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    persional_email = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    full_name_kana = db.Column(db.String(255))
    gender = db.Column(db.Integer, nullable=False)
    tel = db.Column(db.String(15), nullable=False)
    skype = db.Column(db.String(20))
    birthday = db.Column(db.Date, nullable=False)
    onboard_date = db.Column(db.Date, nullable=False)
    avatar = db.Column(db.String(15))
    tbl_user_device_history = db.relationship("User_device_history",
        back_populates="tbl_user",cascade="all, delete",passive_deletes=True)
    create_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    update_at = db.Column(db.TIMESTAMP,server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False)

    def to_json(self):
        return {
            'user_id': self.user_id,
            'group_id': self.group_id,
            'group_name': self.group_name,
            'role_id': self.role_id,
            'role_name': self.role_name,
            'email': self.email,
            'full_name': self.full_name,
            'tel': self.tel,
            'birthday': self.birthday.strftime("%Y-%m-%d"),
            'onboard_date': self.onboard_date.strftime("%Y-%m-%d"),
        }

class User_device_history(db.Model):
    __tablename__ = 'tbl_user_device_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_user.user_id', ondelete="CASCADE"), nullable=False)
    tbl_user = db.relationship("User", back_populates="tbl_user_device_history")
    device_id = db.Column(db.Integer, db.ForeignKey('mst_devices.device_id'), nullable=False)
    mst_devices = db.relationship("Device")
    is_deleted = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    create_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    update_at = db.Column(db.TIMESTAMP,server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False)

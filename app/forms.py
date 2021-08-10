"""Sign-up & log-in forms."""
import regex
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, DateField, HiddenField,
    SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from .models import Group, Role

class SignupForm(FlaskForm):
    """User Sign-up Form."""
    email = StringField(
        'アカウント名:',
        validators=[
            Length(max=50, message="50桁以内の「アカウント名」を入力してください"),
            Email(message="「アカウント名」をyouremail@example.com形式で入力してください"),
            DataRequired(message="「アカウント名」を入力してください")
        ])

    id = HiddenField('id')

    GROUP_CHOICES = [("", "選択してください")]+[
        (str(g.group_id), g.group_name) for g in Group.query.all()]
    ROLE_CHOICES = [("", "選択してください")]+[
        (str(r.role_id), r.role_name) for r in Role.query.all()]
    GENDER_CHOICES = [(1,"Male"), (0,"Female")]

    role = SelectField('ロール: ',choices=ROLE_CHOICES,
        validators=[DataRequired(message="「ロール」を入力してください")])
    group = SelectField('グループ:', choices=GROUP_CHOICES,
        validators=[DataRequired(message="「グループ」を入力してください")]
    )
    gender = SelectField('Gender: ', choices=GENDER_CHOICES, coerce=int)
    full_name = StringField('氏名:',
        validators=[
            DataRequired(message="「氏名」を入力してください"),
            Length(max=255, message=" 255桁以内の「氏名」を入力してください")]
    )
    full_name_kana = StringField('カタカナ氏名:',
        validators=[
            Length(max=255, message=" 255桁以内の「カタカナ氏名」を入力してください"),
            # Regexp(regex="([ｧ-ﾝﾞﾟ])", message="ER009: 「カタカナ氏名」をカタカナで入力してください")
        ]
    )
    birthday = DateField('生年月日:', format='%Y-%m-%d',
        validators=[DataRequired(message="「生年月日」を入力してください")]
    )
    persional_email = StringField('メールアドレス:',
        validators=[
            Length(max=50, message="50桁以内の「メールアドレス」を入力してください")
        ]
    )
    tel = StringField('電話番号:',
        validators=[
            DataRequired(message="「電話番号」を入力してください"),
            Regexp(regex="^[0-9]{1,4}\\-[0-9]{1,4}\\-[0-9]{1,4}$", flags=0,
                message="「電話番号」を1234-5678-9999形式で入力してください"),
            Length(max=14, message="14桁以内の「電話番号」を入力してください")
        ]
    )
    password = PasswordField('パスワード:',
        validators=[
            DataRequired(message='「パスワード」を入力してください'),
            Length(min=5, max=15, message='「パスワード」を5＜＝桁数、＜＝15桁で入力してください'),
            Regexp(regex='[\\w -/:-@\\[-~]', message="「パスワード」に半角英数を入力してください")
        ]
    )
    confirm = PasswordField('パスワード（確認）:',
        validators=[
            DataRequired(message='「パスワード（確認）」を入力してください'),
            EqualTo('password', message="「パスワード（確認)」が不正です。")
        ]
    )
    submit = SubmitField('確認')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'アカウント名:',
        validators=[
            DataRequired(message='「アカウント名」を入力してください'),
            Email(message='「アカウント名」をyouremail@example.com形式で入力してください')
        ]
    )
    password = PasswordField('パスワード:', validators=[DataRequired(message='ER001:「パスワード」を入力してください')])
    submit = SubmitField('ログイン')

class ChangePassword(FlaskForm):
    """User Change-Password Form"""
    password = PasswordField('パスワード:',
        validators=[
            DataRequired(message='「パスワード」を入力してください'),
            Length(min=5, max=15, message='「パスワード」を5＜＝桁数、＜＝15桁で入力してください'),
            Regexp(regex='[\\w -/:-@\\[-~]', message=" 「パスワード」に半角英数を入力してください")
        ]
    )
    confirm = PasswordField('パスワード（確認）:',
        validators=[
            DataRequired(message='「パスワード（確認）」を入力してください'),
            EqualTo('password', message="「パスワード（確認)」が不正です。")
        ]
    )
    submit = SubmitField('確認')

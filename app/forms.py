"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, HiddenField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

class SignupForm(FlaskForm):
    """User Sign-up Form."""
    email = StringField(
        'アカウント名:',
        validators=[
            Length(max=50, message="ER006: 50桁以内の「アカウント名」を入力してください"),
            Email(message="ER005:「アカウント名」をyouremail@example.com形式で入力してください"),
            DataRequired(message="ER001:「アカウント名」を入力してください")
        ])

    id = HiddenField('id')

    role = SelectField('ロール: ',choices=[],
        validators=[DataRequired(message="ER002:「ロール」を入力してください")])

    group = SelectField('グループ:', choices=[],
        validators=[DataRequired(message="ER002:「グループ」を入力してください")]
    )
    gender = SelectField('Gender: ', choices=[], coerce=int)
    full_name = StringField('氏名:',
        validators=[
            DataRequired(message="ER001:「氏名」を入力してください"),
            Length(max=255, message="ER006: 255桁以内の「氏名」を入力してください")]
    )
    full_name_kana = StringField('カタカナ氏名:',
        validators=[
            Length(max=255, message="ER006: 255桁以内の「カタカナ氏名」を入力してください"),
            # Regexp(regex="([ｧ-ﾝﾞﾟ])", message="ER009: 「カタカナ氏名」をカタカナで入力してください")
        ]    
    )
    birthday = DateField('生年月日:', format='%Y-%m-%d',
        validators=[DataRequired(message="ER001:「生年月日」を入力してください")]
    )
    persional_email = StringField('メールアドレス:',
        validators=[
            Length(max=50, message="ER006: 50桁以内の「メールアドレス」を入力してください")
        ]
    )
    tel = StringField('電話番号:',
        validators=[
            DataRequired(message="ER001:「電話番号」を入力してください"),
            Regexp(regex="^[0-9]{1,4}\-[0-9]{1,4}\-[0-9]{1,4}$", flags=0, message="ER005:「電話番号」を1234-5678-9999形式で入力してください"),
            Length(max=14, message="ER006: 14桁以内の「電話番号」を入力してください")
        ]
    )
    password = PasswordField('パスワード:',
        validators=[
            DataRequired(message='ER001:「パスワード」を入力してください'),
            Length(min=5, max=15, message='ER007:「パスワード」を5＜＝桁数、＜＝15桁で入力してください'),
            Regexp(regex='[\w -/:-@\[-~]', message="ER008: 「パスワード」に半角英数を入力してください")
        ]
    )
    confirm = PasswordField('パスワード（確認）:',
        validators=[
            DataRequired(),
            EqualTo('password', message="ER017:「パスワード（確認)」が不正です。")
        ]
    )

    submit = SubmitField('確認')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'アカウント名:',
        validators=[
            DataRequired(message='ER001:「アカウント名」を入力してください'),
            Email(message='ER005:「アカウント名」をyouremail@example.com形式で入力してください')
        ]
    )
    password = PasswordField('パスワード:', validators=[DataRequired(message='ER001:「パスワード」を入力してください')])
    submit = SubmitField('ログイン')
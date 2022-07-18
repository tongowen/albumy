# -*- coding: utf-8 -*-

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp

from app.models import User


class EditProfileForm(FlaskForm):
    name = StringField('昵称', validators=[DataRequired(), Length(1, 30)])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message='The username should contain only a-z, A-Z and 0-9.')])
    website = StringField('网页', validators=[Optional(), Length(0, 255)])
    location = StringField('城市', validators=[Optional(), Length(0, 50)])
    bio = TextAreaField('个性签名', validators=[Optional(), Length(0, 120)])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')


class UploadAvatarForm(FlaskForm):
    image = FileField('上传', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], '上传的文件格式必须为jpg或png')
    ])
    submit = SubmitField('提交')


class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('裁剪并更新')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('这个邮箱已被占用！')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class NotificationSettingForm(FlaskForm):
    receive_comment_notification = BooleanField('新的评论')
    receive_follow_notification = BooleanField('新的粉丝')
    receive_collect_notification = BooleanField('新的点赞')
    submit = SubmitField('提交')


class PrivacySettingForm(FlaskForm):
    public_collections = BooleanField('公开我的点赞')
    submit = SubmitField('提交')


class DeleteAccountForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('用户名不匹配！')

# -*- coding: utf-8 -*-

from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email

from app.forms.user import EditProfileForm
from app.models import User, Role


class EditProfileAdminForm(EditProfileForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    role = SelectField('角色', coerce=int)
    active = BooleanField('活跃的')
    confirmed = BooleanField('已确认')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被占用！')

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('该邮箱已被占用！')

# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


class DescriptionForm(FlaskForm):
    description = TextAreaField('描述', validators=[Optional(), Length(0, 500)])
    submit = SubmitField('提交')


class TagForm(FlaskForm):
    tag = StringField('添加标签（使用空格键来分割标签）', validators=[Optional(), Length(0, 64)])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('提交')

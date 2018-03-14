#!/usr/bin/python
#-*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField,IntegerField,FloatField
from wtforms.validators import DataRequired, Length



class TodoListForm(FlaskForm):
    title = StringField('家务内容', validators=[DataRequired(), Length(1, 64)])
    bz = RadioField(validators=[DataRequired()],choices=[("0", '标准分'),("1",'额外')] ,default=0)
    #status = RadioField('是否完成', validators=[DataRequired()],  choices=[("1", '是'),("0",'否')])
    score = FloatField('分数', validators=[DataRequired()],default=1)
    status = RadioField(validators=[DataRequired()],choices=[("1", '启用'),("2",'不启用')] ,default=1)
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('登录')
    
class FeedbackForm(FlaskForm):
    username = StringField('email*', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('内容*', validators=[DataRequired(), Length(1, 255)])
    submit = SubmitField('提交')

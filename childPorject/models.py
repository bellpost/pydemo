#!/usr/bin/python
#-*- coding: UTF-8 -*-
import time

from ext import db
from flask_login import UserMixin
'''
create table business1(
id int not null,
number float,
savetime datetime)

'''

class TodoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float,nullable=False)
    bz = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, title, status,score,bz):
        self.user_id = user_id
        self.title = title
        self.status = status
        self.score = score
        self.bz = bz
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S")

class Business(db.Model):
    __tablename__ = 'business'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Float, nullable=True)
    savetime = db.Column(db.Integer, nullable=False)

    def __init__(self, id, number):
        self.id = id
        self.number = number
        self.savetime = time.strftime("%Y-%m-%d %H:%M:%S")

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
class Feedback():
    __tablename__="feedback"
    id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(24), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    
    def __init__(self, id,email, content):
        self.id=id
        self.email=email
        self.content=content
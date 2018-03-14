#!/usr/bin/python
#-*- coding: UTF-8 -*-
from __future__ import unicode_literals

from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user

from forms import TodoListForm, LoginForm ,FeedbackForm
from ext import db, login_manager
from models import TodoList, User ,Business

from datetime import datetime ,timedelta
from sqlalchemy.sql import func
import json

SECRET_KEY = 'ab454322d1b418ebc27938b7160e4821'

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://original:original@115.159.225.68/todo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/', methods=['GET', 'POST'])
@login_required
def show_todo_list():
    #form = TodoListForm()
    if request.method == 'GET':
        #Businesslist = Business.query.filter_by(id=id).first_or_404()
        Businesslists = db.session.query(TodoList,TodoList.id,TodoList.user_id,TodoList.title,TodoList.score, Business.savetime, func.sum(Business.number).label('number') )\
        .filter_by(user_id=current_user.id)\
        .join(Business, TodoList.id == Business.id).filter(Business.savetime < datetime.today(),Business.savetime > (datetime.today() + timedelta(days = -1)))\
        .group_by(TodoList.title).all()
        BusinessSum = db.session.query(TodoList, TodoList.user_id,func.sum(Business.number).label('sum'))\
        .filter_by(user_id=current_user.id)\
        .join(Business, TodoList.id == Business.id).filter(Business.savetime < datetime.today(),Business.savetime > (datetime.today() + timedelta(days = -1))).all()
        if len(Businesslists) < 1 :
            flash("没有家务日志,请添加")
        return render_template('index.html',todolists=Businesslists,todosum = BusinessSum)

@app.route('/add/', methods=['GET', 'POST'])
@login_required
def add_todo_list():
    form = TodoListForm()
    if request.method == 'GET':
        todolists = TodoList.query.filter_by(user_id=current_user.id).filter(TodoList.status>=1).all()
        if len(todolists) < 1 :
            flash("没有家务日志,请添加")
        return render_template('newadd.html', todolists=todolists, form=form)
    else:
        if form.validate_on_submit():
            if form.bz.data == '1':
                todolist = TodoList(current_user.id, form.title.data+" (额外)", form.status.data, form.score.data, form.bz.data)
            else:
                todolist = TodoList(current_user.id, form.title.data, form.status.data, form.score.data, form.bz.data)
            db.session.add(todolist)
            db.session.commit()
            flash('新增了一个家务')
        else:
            flash(form.errors)
        return redirect(url_for('add_todo_list'))

@app.route('/feedback/', methods=['POST'])
@login_required
def feedback():
    pass
    
    


@app.route('/save/', methods=['GET', 'POST'])
@login_required
def save_todo_list():
    if request.method == 'GET':
        todolists = TodoList.query.filter_by(user_id=current_user.id).filter(TodoList.status>=1).all()
        if len(todolists) < 1 : 
            return redirect(url_for('add_todo_list'))  
        return render_template('savecore.html',todolists=todolists)
    elif request.method == 'POST':
        data =  request.json
        for con in data['option']:
            id,number = con
            todolist = Business(id,number)
            db.session.add(todolist)
        db.session.commit()
# flash('保存了家务')
    return redirect(url_for('save_todo_list'))
 
@app.route('/me/', methods=['GET', 'POST'])
@login_required
def by_me():
    if request.method == 'GET':
        
        return render_template('byme.html')
 
 
@app.route('/return/', methods=['GET', 'POST'])
@login_required
def return_todo_list():
    if request.method == 'GET':
        flash('保存了家务')
        return redirect(url_for('save_todo_list'))
    
    
@app.route('/delete/<int:id>')
@login_required
def delete_todo_list(id):
     todolist = TodoList.query.filter_by(id=id).first_or_404()
     #db.session.delete(todolist)
     #db.session.update(todolist,status='0')
     todolist.status = '0'
     db.session.commit()
     flash('删除成功')
     return redirect(url_for('add_todo_list'))


@app.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change_todo_list(id):
    if request.method == 'GET':
        todolist = TodoList.query.filter(TodoList.status>=1).filter_by(id=id).first_or_404()
        form = TodoListForm()
        form.title.data = todolist.title
        form.score.data = todolist.score
        form.status.data = str(todolist.status)
        return render_template('modify.html', form=form)
    else:
        form = TodoListForm()
        if form.validate_on_submit():
            todolist = TodoList.query.filter(TodoList.status>=1).filter_by(id=id).first_or_404()
            todolist.title = form.title.data
            todolist.score = form.score.data
            todolist.status = form.status.data
            db.session.commit()
            flash('家务如下')
        else:
            flash(form.errors)
        return redirect(url_for('add_todo_list'))




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash('登录成功')
            return redirect(url_for('show_todo_list'))
        else:
            flash('用户名或密码错误')
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功!')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,threaded=True, debug=True)

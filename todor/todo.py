from flask import Blueprint, render_template, request, redirect, url_for, g

bp = Blueprint('todo', __name__, url_prefix='/todo')

from todor.auth import loging_required
from.models import Todo,User
from todor import db

@bp.route('/list')
@loging_required 
def index():
    todos = Todo.query.all()
    return render_template('todo/index.html', todos = todos)

@bp.route('/create', methods = ('GET','POST'))
@loging_required #para entrar aqui se necesita haber iniciado session 
def create():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(g.user.id, title, desc)

        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo.index'))
    return render_template('todo/create.html')

def get_todo(id):
    todo = Todo.query.get_or_404(id) #hace una busqueda y si la encuentra el id nos devuelve todo 
    return todo

@bp.route('/update/<int:id>', methods = ('GET', 'POST'))
@loging_required #para entrar aqui se necesita haber iniciado session 
def update(id):
    todo = get_todo(id)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.state = True if request.form.get('state') == 'on' else False

        db.session.commit()

        return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo = todo)

@bp.route('/delete/<int:id>')
@loging_required #para entrar aqui se necesita haber iniciado session
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))

#project/views.py

import sqlite3;
from functools import wraps;
from flask import Flask, flash, redirect , render_template, \
	request, session, url_for,g
from forms import AddTaskForm;
#config

app=Flask(__name__);
app.config.from_object('_config');

#helper functions

def connect_db():
	return sqlite3.connect(app.config['DATABASE_PATH']);

#auth guard

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs);
		else:
			flash('you need to login first');
			return redirect(url_for('login'));
	return wrap;

#route handlers

@app.route('/logout/')
def logout():
	session.pop('logged_in',None);
	flash('Bye Bye !!');
	return redirect(url_for('login'));

@app.route('/',methods=['GET','POST'])
def login():
	if request.method=='POST':
		if request.form['username']!=app.config['USERNAME'] \
			or request.form['password']!=app.config['PASSWORD']:
			error='Invalid credentials. PLease try again';
			return render_template('login.html',error=error);
		else:
			session['logged_in']=True;
			flash('Welcome!');
			return redirect(url_for('tasks'));
	return render_template('login.html');	

@app.route('/tasks/')
@login_required
def tasks():
	g.db=connect_db();
	cursor=g.db.execute(
		'select name, due_date, priority, task_id from Tasks where status=1'
		);

	open_tasks=[
		dict(name=row[0],due_date=row[1],
			priority=row[2],task_id=row[3]) for row in cursor.fetchall()
	];

	cursor=g.db.execute('select name,due_date,priority,task_id from Tasks where status=0');

	closed_tasks=[
		dict(name=row[0],due_date=row[1],
			priority=row[2],task_id=row[3]) for row in cursor.fetchall()
	];

	g.db.close();

	return render_template(
		'tasks.html',
		form=AddTaskForm(request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks
		);

#add new tasks
@app.route('/add/',methods=['POST'])
@login_required
def new_task():
	g.db=connect_db();
	name=request.form['name'];
	date=request.form['due_date'];
	priority=request.form['priority'];

	if not name or not date or not priority:
		flash("all fields are required. Please try again");
		return redirect(url_for('tasks'))
		g.db.close();
	else:
		g.db.execute('insert into tasks (name,due_date,priority,status) \
			values(?,?,?,?)',[
			request.form['name'],
			request.form['due_date'],
			request.form['priority'],
			'1'
			]);
		g.db.commit();
		g.db.close();
		flash("new entry was successfully posted");
		return redirect(url_for('tasks'));

#mark tasks as completed
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	g.db=connect_db();
	g.db.execute('update Tasks set status=0 where task_id='+str(task_id));
	g.db.commit();
	g.db.close();
	flash('The task was marked as complete');
	return redirect(url_for('tasks'));

# Delete tasks
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	g.db=connect_db();
	g.db.execute('delete from tasks where task_id='+str(task_id));
	g.db.commit();
	g.db.close();
	flash('THe task has been deleted');
	return redirect(url_for('tasks'))

















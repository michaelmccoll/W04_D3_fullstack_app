from flask import Flask, render_template, request, redirect
from flask import Blueprint
from repositories import task_repository, user_repository
from models.task import Task

# This allows Flask to understand task routes
tasks_blueprint = Blueprint("tasks",__name__)

# Return an HTML view listing all the tasks
@tasks_blueprint.route('/tasks')
def tasks():
    tasks = task_repository.select_all()                            # Gets all the tasks
    return render_template("tasks/index.html",all_tasks=tasks)      # Renders tasks/index HTML and passes in, tasks as all_tasks     

@tasks_blueprint.route('/tasks/new')
def new_task():
    users = user_repository.select_all()                            # Gets all the users
    return render_template("tasks/new.html",all_users=users)        # Renders tasks/index HTML and passes in, users as all_users

@tasks_blueprint.route('/tasks', methods=['POST'])
def create_task():
    description = request.form["description"]                       # Grab all parts of form and assign to variables
    user_id = request.form["user"]
    duration = request.form["duration"]
    completed = request.form["completed"]
    user = user_repository.select(user_id)                          # Find the right user from the dB, based on the user.id from the form
    task = Task(description,user,duration,completed)                # Create a new Task object based on that form data
    task_repository.save(task)                                      # Save it to the database
    return redirect("/tasks")                                       # Redirect back to all tasks view

@tasks_blueprint.route('/tasks/<id>')
def show_task(id):                                                  # Capture the id parameter from the URL
    task = task_repository.select(id)                               # Find the right task in the db by the id
    return render_template('/tasks/show.html', selected_task=task)  # Render an HTML view with the task


@tasks_blueprint.route('/tasks/<id>/delete', methods=['POST'])
def delete_task(id):
    task_repository.delete(id)
    return redirect('/tasks')

@tasks_blueprint.route('/tasks/<id>/edit', methods=['GET'])
def edit_task(id):
    task = task_repository.select(id)
    users = user_repository.select_all()
    return render_template('tasks/edit.html', task = task, all_users = users)

@tasks_blueprint.route('/tasks/<id>', methods=['POST'])
def update_task(id):
    description = request.form['description']
    user_id     = request.form['user_id']
    duration    = request.form['duration']
    completed   = request.form['completed']
    user        = user_repository.select(user_id)
    task        = Task(description, user, duration, completed, id)
    task_repository.update(task)
    return redirect('/tasks')
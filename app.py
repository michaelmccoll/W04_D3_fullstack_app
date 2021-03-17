from flask import Flask, render_template, redirect
from controllers.tasks_controller import tasks_blueprint

app = Flask(__name__)

app.register_blueprint(tasks_blueprint)                     # This allows the startpoint to use the task controller and routes

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

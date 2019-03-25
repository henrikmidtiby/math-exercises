# from app import app
from helper.exerciseconverterfunctions import get_exercises, render_exercises

from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', converted_exercise="")

@app.route('/name/<name>')
def hello_world_named(name):
    return 'Welcome %s' % name

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        converted_exercise = request.form['exercise_input']
        exercises = list(get_exercises(change_part_of_markup(converted_exercise)))
        rendered_exercises = render_exercises(exercises)
        return render_template('index.html',
                converted_exercise=rendered_exercises)
    else:
        return render_template('index.html')
        


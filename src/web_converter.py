# from app import app
from .exercise_converter.helper.exerciseconverterfunctions import get_exercises, render_exercises, change_part_of_markup

from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', 
            converted_exercise="",
            original_input="")

@app.route('/name/<name>')
def hello_world_named(name):
    return 'Welcome %s' % name

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        converted_exercise = request.form['exercise_input']
        rendered_exercises = converted_exercise
        exercises = list(get_exercises(change_part_of_markup(converted_exercise.split('\n'))))
        rendered_exercises = render_exercises(exercises)
        print(str(rendered_exercises))
        my_bytes = str(rendered_exercises).encode("utf-8")
        simplified = my_bytes.decode("unicode-escape")
        print(simplified)
        return render_template('index.html',
                converted_exercise=simplified, 
                original_input=converted_exercise)
    else:
        return render_template('index.html')
        


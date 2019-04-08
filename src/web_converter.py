# from app import app
from .exercise_converter.helper.exerciseconverterfunctions import get_exercises, render_exercises, change_part_of_markup, get_exercise_meta_information_from_string, write_exercises_to_file 
from io import StringIO

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
        outfile = StringIO()
        converted_exercise = request.form['exercise_input']
        rendered_exercises = converted_exercise
        exercise_meta_information = get_exercise_meta_information_from_string(converted_exercise.split('\n'))
        exercises = list(get_exercises(change_part_of_markup(converted_exercise.split('\n'))))
        rendered_exercises = render_exercises(exercises)
        write_exercises_to_file(outfile, exercise_meta_information,
                rendered_exercises)
        outfile.seek(0)
        simplified=outfile.read()
        return render_template('index.html',
                converted_exercise=simplified.replace("\r", "\\n"), 
                original_input=converted_exercise)
    else:
        return render_template('index.html')
        


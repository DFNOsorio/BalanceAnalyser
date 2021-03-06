from flask import Flask
from flask import render_template, jsonify, request, Response, redirect, url_for
import os
from processing_code import *
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.model import *
import json
app = Flask(__name__)

default_path = '../BalanceAnalyser/data'
global folder

global s1
global s2
global s3
global s4

global emg_smoother_window
global filter_frequency


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/graph")
def graphs():
    return render_template("graphs.html")

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result = a + b)

@app.route('/_display_folders')
def get_folder_name(default_path=default_path):
    # ALTERAR PARA ESCOLHER OUTROS PATHS
    return jsonify(os.listdir(default_path))

@app.route('/_set_folder_name')
def set_folder_name():
    global folder
    folder = request.args.get('folder_name')
    return jsonify(folder)

@app.route('/_load_data')
def load_data():
    global folder
    if folder == 'Andreia':
        return Response(process_patient(default_path+'/', folder, multiple=True), mimetype= 'text/event-stream')
    else:
        return Response(process_patient(default_path+'/', folder), mimetype= 'text/event-stream')

@app.route('/_cache_data')
def cache_data():
    global s1
    global s2
    global s3
    global s4

    global emg_smoother_window
    global filter_frequency

    [[s1, s2, s3, s4], filter_frequency, emg_smoother_window]= get_val()
    print filter_frequency
    return 'done'

@app.route('/_get_cache_data')
def get_cache_data():
    global filter_frequency
    global emg_smoother_window
    return jsonify([filter_frequency, emg_smoother_window])

@app.route('/_make_graph')
def make_graph():
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)

    show(p)

    plot = figure()
    plot.circle([1,2], [3,4])


    script, div = components(plot, wrap_script=False)

    data = {'script'  : script, 'div' : div, 'jsons': plot.to_json(True)}
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)

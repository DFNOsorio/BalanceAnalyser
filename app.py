from flask import Flask
from flask import render_template, jsonify, render_template, request
import os


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sara")
def sara():
    return render_template("sara.html")

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result = a + b)

if __name__ == "__main__":
    print os.listdir('../BalanceAnalyser/data')
    app.run(host='0.0.0.0',port=5000,debug=True)

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
    return "MhMining Method <br><a href='Onshore'>Onshore</a><br><a href='Offshore'>Offshore</a><br><a href='Subsea'>Subsea</a>"

@app.route("/Onshore")
def onshorecal():
    return render_template('Onshore.html')

from flask import render_template

@app.route('/Offshore')
def offshorecal():
    return render_template('Offshore.html')

@app.route('/Subsea')
def subseacal():
    return render_template('Subsea.html')

if __name__ == "__main__":
    app.run()

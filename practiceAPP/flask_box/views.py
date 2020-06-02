from flask_box import app

@app.route("/")
def index():
    return "MhMining Method"
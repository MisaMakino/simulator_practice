from flask import Flask, render_template, request, jsonify, json, make_response
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import pandas.plotting as plotting
import numpy as np


app = Flask(__name__)

@app.route("/")
def hello():
    return "MhMining Method <br><a href='Simulation'>Simulation</a><br>"

@app.route('/Simulation')
def Simulation():

    return render_template('calc.html')

# @app.route('/simulate1')
# def simulate1():
#     # This function read two parameters from web request
#     # Returns the sum of two parameters.
#     button1 = request.args.get('input1')
#     button2 = request.args.get('input2')
#     #button3 = request.args.get('input3')

#     output1=5
#     # output1 = int(button1)+ int(button2)
#     output2 = 9 / 8
#     # replace the next line with your simulator

#     json_str = '{"output1":' + str(output1) + ',"output2":' + str(output2) + '}'
#     json_data = json.loads(json_str)

#     # write your output to a file

#     with open('./data/output.json', 'w') as f:
#         json.dump(json_data["output1"], f, indent=4)
#         json.dump(json_data["output2"], f, indent=4)
#     return  json_str

#graphについてかく
@app.route('/graph1.png', methods=["GET" , "POST"])
def graph1():

    button1 = request.args.get('input1')
    button2 = request.args.get('input2') 

    # X = []
    # Y = []
    # for i in range(12):
    #     key = "input"+str(i+7)
    #     X.append(int(request.args.get(key)))
    #     key = "input"+str(i+9)
    #     Y.append(int(request.args.get(key)))

    # 昨日の
    x = [1,2,3,4,5,6,7,8,9,10]
    y = [1,2,3,4,5,6,7,8,9,10]
    
    fig, ax = plt.subplots(2,1,figsize=(5,5))
    ax[0].scatter(x, y, s=80, c='g')
    ax[0].set_title(button1)

# 色変えたよおおおおおおおおおおお
    i = 9
    if button1 == "Onshore" :
        if button2 == "Pipeline" :
            i = 0

    ax[0].scatter(x[i],y[i], s=100, c='r')

    df = pd.DataFrame(np.array([['$'+str(20),'$'+str(20),'$'+str(30),'$'+str(20),'$'+str(20),'$'+str(30),'$'+str(20),'$'+str(20),'$'+str(30)],[str(9)+'/TRL',str(4)+'/TRL',str(6)+'/TRL',str(9)+'/TRL',str(4)+'/TRL',str(6)+'/TRL',str(9)+'/TRL',str(4)+'/TRL',str(6)+'/TRL',]]))
    plotting.table(ax[1], df, loc='center', rowLabels=['Cost','Risk'], colLabels=['Phase1','Phase2','Sum','Phase1','Phase2','Sum','Phase1','Phase2','Sum'])
    ax[1].axis('off')
    
# canvasにプロットした画像を出力
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
# HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response   

if __name__ == "__main__":
    app.run(debug=True)


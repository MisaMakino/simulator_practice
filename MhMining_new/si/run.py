from flask import Flask, render_template, request, jsonify, json, make_response
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import pandas.plotting as plotting
import numpy as np
import csv
import os
import os.path
import sys

app = Flask(__name__)

@app.route("/")
def hello():
    return "MhMining Method <br><a href='Simulation'>Simulation</a><br>"

@app.route('/Simulation')
def Simulation():

    return render_template('mhcalc.html')

@app.route('/simulate1')
def simulate1():
    print('run simulate1')
    global Location_Trans
    # This function read two parameters from web request
    # Returns the sum of two parameters.
    button1 = request.args.get('input1')
    button2 = request.args.get('input2')

    output1 = int(button1)
    output2 = int(button2)
    Location_Trans = [output1, output2]
    # replace the next line with your simulator

    json_str = '{"output1":' + str(output1) + ',"output2":' + str(output2) + '}'
    json_data = json.loads(json_str)

    # write your output to a file

    with open('./data/output.json', 'w') as f:
        json.dump(json_data["output1"], f, indent=4)
        json.dump(json_data["output2"], f, indent=4)
    return  json_str

#graphについてかく
@app.route('/graph1.png')
def graph1():
    print('run grraph1')
    global Location_Trans
 
    print('Location_Trans = ' + str(Location_Trans))

# サンプルデータ（左からOnshore*Pipeline, Onshore*via Plants, ..., Subsea*Ship）
    x = [2.0,2.1,2.5,2.8,4.0,5.0,5.2,6.6,8.8]
    y = [8.0,7.1,4.4,5.8,2.5,5.0,2.2,2.0,1.7]
    # 9通りのプロット描画
    fig, ax = plt.subplots(2,1,figsize=(5,5))
    ax[0].scatter(x, y, s=80, c='g')
    ax[0].set_title('Cost and Risk')
    ax[0].set_xlabel('Cost')
    ax[0].set_ylabel('Risk')
    ax[0].set_xlim(0,10)
    ax[0].set_ylim(0,10)

# ラジオボタンの選択結果の点を強調
    i = -1 #デフォルト
    print(Location_Trans)
    if Location_Trans[0] == 1:
        if Location_Trans[1] == 4:
            i = 0
        elif Location_Trans[1] == 5:
            i = 1
        elif Location_Trans[1] == 6:
            i = 2
    elif Location_Trans[0] == 2:
        if Location_Trans[1] == 4:
            i = 3
        elif Location_Trans[1] == 5:
            i = 4
        elif Location_Trans[1] == 6:
            i = 5
    elif Location_Trans[1] == 3:
        if Location_Trans[1] == 4:
            i = 6
        elif Location_Trans[1] == 5:
            i = 7
        elif Location_Trans[1] == 6:
            i = 8
    else:
        print('else')

    ax[0].scatter(x[i],y[i], s=80, c='r')
    if i == -1:
        ax[0].scatter(x, y, s=80, c='w')

# ラジオボタンの選択結果の表を描画
    selected = str(Location_Trans[0]) + '_' + str(Location_Trans[1])
    csvname = 'data/' + selected + '/' + selected + '.csv'
    with open(csvname) as f:
        # print(f.read())
        reader = csv.reader(f)
        l = [row for row in reader]
    print(l)

# 概数に
    for i in range(9):
        l[0][i] = int(float(l[0][i])/1E+12)

# 表の中身
    df = pd.DataFrame(np.array([['$ '+str(l[0][0]),'$ '+str(l[0][1]),'$ '+str(l[0][2]),'$ '+str(l[0][3]),'$ '+str(l[0][4]),'$ '+str(l[0][5]),'$ '+str(l[0][6]),'$ '+str(l[0][7]),'$ '+str(l[0][8])],[str(l[1][0])+' TRL',str(l[1][1])+' TRL',str(l[1][2])+' TRL',str(l[1][3])+' TRL',str(l[1][4])+' TRL',str(l[1][5])+' TRL',str(l[1][6])+' TRL',str(l[1][7])+' TRL',str(round(float(l[1][8]),1))+' TRL',]]))
    plotting.table(ax[1], df, loc='center', rowLabels=['Cost','Risk'], colLabels=['Phase1','Phase2','Phase3','Phase4','Phase5','Phase6','Phase7','Phase8','Sum'])
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
    Location_Trans = [9, 9]
    app.run(debug=True)
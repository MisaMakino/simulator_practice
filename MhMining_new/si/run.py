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
    x = [2.12E+11,3.43E+10,4.47E+11,3.65E+11,1.33E+11,1.58E+11,3.65E+12,1.33E+12,1.58E+12]
    y = [4.95,3.57,2.88,4.97,3.69,4.29,1.56,1.42,1.41]
# 9通りのプロット描画
    fig, ax = plt.subplots(2,1,figsize=(5,5))
    #ax[0].scatter(x, y, s=80, marker="o", c='c')

    #凡例や各プロットの形
    ax[0].scatter(2.12E+11, 4.95, s=60, marker="o", c='c', alpha=0.5, label = "$Onshore_Pipeline$")
    ax[0].scatter(3.43E+10, 3.57, s=60, marker="*", c='c', alpha=0.5, label = "$Onshore_via Plant$")
    ax[0].scatter(4.47E+11, 2.88, s=60, marker="D", c='c', alpha=0.5, label = "$Onshore_Ship$")
    ax[0].scatter(3.65E+11, 4.97, s=60, marker="x", c='y', alpha=0.5, label = "$Offshore_Pipeline$")
    ax[0].scatter(1.33E+11, 3.69, s=60, marker="+", c='y', alpha=0.5, label = "$Offshore_via Plant$")
    ax[0].scatter(1.58E+11, 4.29, s=60, marker="s", c='y', alpha=0.5, label = "$Offshore_Ship$")
    ax[0].scatter(3.65E+12, 1.56, s=60, marker="^", c='m', alpha=0.5, label = "$Subsea_Pipeline$")
    ax[0].scatter(1.33E+12, 1.42, s=60, marker="p", c='m', alpha=0.5, label = "$Subsea_via Plant$")
    ax[0].scatter(1.58E+12, 1.41, s=60, marker="h", c='m', alpha=0.5, label = "$Subsea_Ship$")
    ax[0].legend(bbox_to_anchor=(0., -0.35, 1., .102), loc='upper left', borderaxespad=0, ncol=3, mode="expand", fontsize=6)

    ax[0].set_title('Cost and Risk')
    ax[0].set_xlabel('Cost')
    ax[0].set_ylabel('Risk')
    #ax[0].set_xlim(0,10)
    #ax[0].set_ylim(0,10)

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

    ax[0].scatter(x[i],y[i], s=100, c='r', alpha=1.0), 

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
        l[0][i] = int(float(l[0][i])/1E+8)
    
# 表の中身
    df = pd.DataFrame(np.array([['$ '+str(l[0][0]),'$ '+str(l[0][1]),'$ '+str(l[0][2]),'$ '+str(l[0][3]),'$ '+str(l[0][4]),'$ '+str(l[0][5]),'$ '+str(l[0][6]),'$ '+str(l[0][7]),'$ '+str(l[0][8])],[str(round(float(l[1][0]),2)),str(round(float(l[1][1]),2)),str(round(float(l[1][2]),2)),str(round(float(l[1][3]),2)),str(round(float(l[1][4]),2)),str(round(float(l[1][5]),2)),str(round(float(l[1][6]),2)),str(round(float(l[1][7]),2)),str(round(float(l[1][8]),2))]]))
    plotting.table(ax[1], df, loc='center', rowLabels=['Cost*','Risk'], colLabels=['Phase1','Phase2','Phase3','Phase4','Phase5','Phase6','Phase7','Phase8','Sum'])
    ax[1].axis('off')

    # plt.savefig('graph_default.png')

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
from flask import Flask, render_template, request, jsonify, json, make_response
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/")
def hello():
    return "MhMining Method <br><a href='Simulation'>Simulation</a><br>"

@app.route('/Simulation')
def Simulation():

    return render_template('calc.html')

@app.route('/simulate1')
def simulate1():
# This function read two parameters from web request
# Returns the sum of two parameters.
    param1 = request.args.get('input1')
    param2 = request.args.get('input2')
    param3 = request.args.get('input3')
    param4 = request.args.get('input4')
    param5 = request.args.get('input5')
    param6 = request.args.get('input6')
    param7 = request.args.get('input7')
    param8 = request.args.get('input8')
    param9 = request.args.get('input9')

    output1 = int(param1)+ int(param2)
    output2 = 9 / 8
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
    # 本当はoutput1とoutput2を縦軸と横軸に使いたい
    # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    x = np.random.rand(10)*2E+12 + 2E+12
    y = np.random.rand(10) 
    #y = [5.5E+12, 2E+12, 3E+12, 6E+12,8E+12,2E+12, 2E+12, 2E+12, 2E+12, 2E+12]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.clear()

    plt.title('Cost and Risk')
    plt.grid(which='both')
    plt.legend()
    plt.scatter(x, y)
    #ここまでよくわからん

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

#下には各フェーズのお金の合計金額

#df = pd.read_csv('.csv', encording='utf-8')

if __name__ == "__main__":
    app.run(debug=True)


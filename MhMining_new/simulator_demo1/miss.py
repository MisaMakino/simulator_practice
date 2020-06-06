from flask import Flask, render_template, request, jsonify, json
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def hello():
    return "MhMining Method <br><a href='Onshore'>Onshore</a><br><a href='Offshore'>Offshore</a><br><a href='Subsea'>Subsea</a>"

@app.route("/json")
def jsonreturn():
    # read JSON file and send them to the web client
    with open("./data/input.json", 'r') as f:
        json_data = json.load(f)
    json_str = json.dumps(json_data)
    return json_str

@app.route('/hello')
@app.route('/hello/<name>')
def hello2(name=None):
# /hello will reply basic html
# /hello/<name> will reply with username specified in <name>
    return render_template('hello.html', name=name)

@app.route('/Onshore')
def Onshore():

    return render_template('Onshore.html')

@app.route('/simulate1')
def simulate1():
# This function read two parameters from web request
# Returns the sum of two parameters.
    param1 = request.args.get('input1')
    param2 = request.args.get('input2')
    param3 = request.args.get('input3')
    param4 = request.args.get('input4')

    output1 = int(param1) + int(param2)
    output2 = int(param3) + int(param4)
    output3 = int(param3) + int(param4)
    # replace the next line with your simulator
    
    # output1は下のように範囲絞って文字を返したい
    #output1 = 

            #if 0 < int(param2) < 100 or 0 < int(param3) < 1000
                #return "Pipeline"
            #else:
                #return "Ship"
    
    #output2は以下のような計算式をしたい
    #output2 = 

            #CAPEX * Financial Uncertinty + OPEX * Technical Uncertinty

    #putput3は以下のような計算式をしたい
    #output3 = 
    # 
    #          technical risk * environment risk
    #          9/TRL(n) * ????????

    json_str = '{"output1":' + str(output1) + ',"output2":' + str(output2) + ',"output3":' + str(output3) +'}'
    json_data = json.loads(json_str)

    # write your output to a file

    with open('./data/output.json', 'w') as f:
        json.dump(json_data["output1"], f, indent=4)
        json.dump(json_data["output2"], f, indent=4)
        json.dump(json_data["output3"], f, indent=4)
    return  json_str

#graphについてかく

@app.route('/graph1.png')
def graph1():

    # 本当はoutput2とoutput3を縦軸と横軸に使いたい
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.cleas()

    plt.title('Cost and Risk')
    plt.grid(which='both')
    plt.legend()
    plt.plot(x, y)
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

@app.route('/Offshore')
def Offshore():

    return render_template('Offshore.html')

@app.route('/simulate2')
def simulate2():
# This function read two parameters from web request
# Returns the sum of two parameters.
    param1 = request.args.get('input1')
    param2 = request.args.get('input2')
    param3 = request.args.get('input3')
    param4 = request.args.get('input4')

    # replace the next line with your simulator

    output1 = int(param1) * int(param2)
    output2 = int(param1) * int(param4) 
    output3 = int(param3) * int(param4)
    json_str = '{"output1":' + str(output1) + ',"output2":' + str(output2) + ',"output3":' + str(output3) +'}'
    json_data = json.loads(json_str)

    # write your output to a file

    with open('./data/output.json', 'w') as f:
        json.dump(json_data["output1"], f, indent=4)
        json.dump(json_data["output2"], f, indent=4)
        json.dump(json_data["output3"], f, indent=4)
    return  json_str

@app.route('/Subsea')
def Subsea():

    return render_template('Subsea.html')

@app.route('/simulate3')
def simulate3():
# This function read two parameters from web request
# Returns the sum of two parameters.
    param1 = request.args.get('input1')
    param2 = request.args.get('input2')
    param3 = request.args.get('input3')
    param4 = request.args.get('input4')

    # replace the next line with your simulator

    output1 = int(param1) + int(param2)
    output2 = int(param3) + int(param4)
    output3 = int(param3) + int(param4)
    json_str = '{"output1":' + str(output1) + ',"output2":' + str(output2) + ',"output3":' + str(output3) +'}'
    json_data = json.loads(json_str)

    # write your output to a file

    with open('./data/output.json', 'w') as f:
        json.dump(json_data["output1"], f, indent=4)
        json.dump(json_data["output2"], f, indent=4)
        json.dump(json_data["output3"], f, indent=4)
    return  json_str


if __name__ == "__main__":
    app.run(debug=True)

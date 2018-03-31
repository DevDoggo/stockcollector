from flask import Flask, render_template, session, request, flash #rt, renders html
from graphObject import GraphObject
import datetime
from bokeh.resources import CDN

app=Flask(__name__)

graphList =[]
graph1 = GraphObject("MU", datetime.datetime(2016, 3, 1), datetime.datetime(2016,3,10))
graphList.append(graph1)
#graph2 = GraphObject("NVDA", datetime.datetime(2016, 3, 1), datetime.datetime(2016,3,10))
#graphList.append(graph2)

cdn_css=CDN.css_files[0]
cdn_js=CDN.js_files[0]

currentDate = (datetime.datetime.now()).date()

def plotrenderer(g):
    return render_template("home.html",
    cdn_css=cdn_css,
    cdn_js=cdn_js,
    currentDate=currentDate,
    graphs=graphList)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        try:
            symbol=request.form['companySymbol']
            start=(request.form['startTime']).split("-")
            end=(request.form['endTime']).split("-")
            #symbol="AMD"
            #start=[2016, 3, 1]
            #end=[2016, 3, 10]
            for i in range(len(start)):
                start[i] = int(start[i])
                end[i] = int(end[i])
            print(start)
            print(end)
            newGraph=GraphObject(str(symbol), datetime.datetime(start[0], start[1], start[2]), datetime.datetime(end[0], end[1], end[2]))
            graphList.append(newGraph)
        except:
            print("Woa there buddy")
            flash('Incorrect Input!')

    return(plotrenderer(graphList))

#@app.route('/home') #home page\\
#def home():
#    return render_template("home.html")

if __name__=="__main__":
    app.secret_key = "nabbaboye"
    app.run(debug=True)

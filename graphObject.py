from datetime import datetime
from pandas_datareader import data
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components


class GraphObject:
    script =""
    div = ""
    companyTag = ""
    startTime = ""
    endTime = ""
    dataSource = "yahoo"
    highOpenClose = [0, 0]
    daysIncreased, daysDecreased = [0, 0]
    averageGain = 0
    highestValue = 0
    lowestValue = 0
    firstRow = ""
    lastRow = ""
    firstValue = 0
    lastValue = 0
    totalGain = 0
    totalIncrease = 0


    df = ""
    graphPlot = ""

    def __init__(self, companyTag, startTime, endTime):
        self.update(companyTag, startTime, endTime)

    def update(self, companyTag, startTime, endTime):
        self.df = data.DataReader(name=companyTag, data_source=self.dataSource, start=startTime, end=endTime)
        self.df["Status"]= [self.iterateTable(c, o, h, l) for c, o, h, l in zip(self.df.Close, self.df.Open, self.df.High, self.df.Low)]
        self.daysIncreased, self.daysDecreased = self.highestByClosedOrOpen(self.highOpenClose)
        self.rowCalculations()
        self.df["Middle"]=(self.df.Open+self.df.Close)/2
        self.df["Height"]=abs(self.df.Close-self.df.Open)
        self.graphPlot = self.plotGraph(self.df, companyTag)
        self.setVariables(self.graphPlot, companyTag, startTime, endTime)

    #Checks for values of close- and opening-time to decide
    #if the value increased or lowered.
    def iterateTable(self, closed, open, highest, lowest):
        if self.lowestValue == 0:
            self.lowestValue = lowest
        if lowest < self.lowestValue:
            self.lowestValue = lowest
        if highest > self.highestValue:
            self.highestValue = highest

        if closed > open:
            value="Increase"
            self.highOpenClose[1] = self.highOpenClose[1] + 1
        elif closed < open:
            value="Decrease"
            self.highOpenClose[0] = self.highOpenClose[0] + 1
        else:
            value="Equal"
        return value

    def highestByClosedOrOpen(self, xArr):
        xSum = (xArr[0] + xArr[1])/100
        openPerc = round((xArr[0])/xSum, 2)
        closedPerc = round((xArr[1])/xSum, 2)
        return(closedPerc, openPerc)

    def rowCalculations(self):
        self.firstRow = self.df[:1]
        self.lastRow = self.df[len(self.df)-1:]
        self.firstValue = round(float(self.firstRow.Open), 2)
        self.lastValue = round(float(self.lastRow.Close), 2)
        self.totalGain = round(self.lastValue-self.firstValue, 2)
        self.totalIncrease = round(self.lastValue/(self.firstValue/100), 2)

    def calcAverageGain():
        pass

    def plotGraph(self, df, companyTag):
        p=figure(x_axis_type='datetime',width=500, height=185, responsive=True) #responsive makes it scale according to browser
        p.title.text=companyTag
        p.grid.grid_line_alpha=0.3 # transparent grid

        hours_12=12*60*60*1000

        #Anything added on p becomes a new layer on top of the old one.
        p.segment(df.index, df.High, df.index, df.Low, color="Black") #Shows the line in the candles

        p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"],
               hours_12, df.Height[df.Status=="Increase"], fill_color="green", line_color="black") #x, y, width, height

        p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"],
               hours_12, df.Height[df.Status=="Decrease"], fill_color="orange", line_color="black") #x, y, width, height
        return p

    def setVariables(self, p, companyTag, startTime, endTime):
        self.script, self.div, = components(p)
        self.companyTag=companyTag
        self.startTime=startTime.date()
        self.endTime=endTime.date()

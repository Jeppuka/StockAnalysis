from tkinter import *
import tkinter as tk
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import pandas as pd
import mplfinance as mpf
from datetime import date
from tkintertable import TableCanvas, TableModel


from yahoo_fin import stock_info as si
import time

root = Tk()
root.geometry("1675x1000")
root.configure(bg='black')

tickerEntry2 = Entry(root, width=15)
tickerEntry2.insert(0,"PLTR")
tickerEntry2.configure(fg="black")
tickerEntry2.place(x=1260,y=30)

def clearAllGraphs():
    try:#for canvas

        for item in canvas.get_tk_widget().find_all():
            canvas.get_tk_widget().delete(item)
        canvas.get_tk_widget().configure(bg="black")
    except:
        pass

    try:#for canvas2
        for item in canvas2.get_tk_widget().find_all():
            canvas2.get_tk_widget().delete(item)
        canvas2.get_tk_widget().configure(bg="black")
    except:
        pass

    try:#for canvas3
        for item in canvas3.get_tk_widget().find_all():
            canvas3.get_tk_widget().delete(item)
        canvas3.get_tk_widget().configure(bg="black")
    except:
        pass

    try:#for canvas4
        for item in canvas4.get_tk_widget().find_all():
            canvas4.get_tk_widget().delete(item)
        canvas4.get_tk_widget().configure(bg="black")
    except:
        pass


def showCurrentPortfolio():
    #print(tickerEntry1.get())

    clearAllGraphs()

    readAllTradesFile = open("allTimeTrades.txt","r")
    readAllTrades = readAllTradesFile.read()
    allTradesList = readAllTrades.split("\n")#get the previous current holdings and make it into a list
    allTradesLabel = Label(root, text="All Trades",width=10, bg="black", fg="#39FF14").place(x=120,y=75)

    allTradesListBox = Listbox(root, width = 25, height= 50, bg="black", fg="#39FF14", selectbackground="black")
    for x in range(len(allTradesList)):
        allTradesListBox.insert(x+1,allTradesList[x])
    allTradesListBox.place(x=50,y=125)

    readCurrentPortfolioFile = open("currentPositions.txt","r")
    readCurrentPortfolio = readCurrentPortfolioFile.read()
    currentPortfolioList = readCurrentPortfolio.split("\n")#get the previous current holdings and make it into a list
    currentPortfolioLabel = Label(root, text="Current Portfolio",width=20, bg="black", fg="#39FF14").place(x=275,y=75)

    currentPortfolioListBox = Listbox(root, width = 25, height= 50, bg="black", fg="#39FF14", selectbackground="black")
    for x in range(len(currentPortfolioList)):
        currentPortfolioListBox.insert(x+1,currentPortfolioList[x])
    currentPortfolioListBox.place(x=290,y=125)

def updateCurrentPortfolioPrices():
    readCurrentPortfolioFile = open("currentPositions.txt","r")
    readCurrentPortfolio = readCurrentPortfolioFile.read()
    currentPortfolioList = readCurrentPortfolio.split("\n")#get the previous current holdings and make it into a list

    writeCurrentPortfolio = open("currentPositions.txt","w")

    for x in range(len(currentPortfolioList)-1):
        currentPrice = si.get_live_price(currentPortfolioList[x].split()[0])
        withoutPrice = currentPortfolioList[x].split()[0]+" "+currentPortfolioList[x].split()[1]+" "+currentPortfolioList[x].split()[2]+" "
        writeCurrentPortfolio.writelines(withoutPrice+" "+str(round(currentPrice, 2))+"\n")

    writeCurrentPortfolio.close()


def addNewHolding():#adding new holdings to my holdings
    addTicker = addHoldingEntryTicker.get()
    addHoldingEntryTicker.delete(0, "end")
    addHoldingEntryTicker.insert(0, "")

    addPrice = addHoldingEntryPrice.get()
    addHoldingEntryPrice.delete(0, "end")
    addHoldingEntryPrice.insert(0, "")

    addShares = addHoldingEntryShares.get()
    addHoldingEntryShares.delete(0, "end")
    addHoldingEntryShares.insert(0, "")

    if addHoldingEntryDate.get() == "":
        today = date.today()
        addDate = today.strftime("%d/%m/%Y")
    else:
        addDate = addHoldingEntryDate.get()
    addHoldingEntryDate.delete(0, "end")
    addHoldingEntryDate.insert(0, "")

    addTarget = addHoldingEntryTarget.get()
    addHoldingEntryTarget.delete(0, "end")
    addHoldingEntryTarget.insert(0, "")

    stockValue = si.get_live_price(addTicker)

    print(stockValue)

    originalStockValue = float(addShares)*float(addPrice)

    currentStockValue = float(addShares)*float(stockValue)

    profitLossValue = float(currentStockValue)-float(originalStockValue)

    profitLossPercentage = float(currentStockValue)/float(originalStockValue)

    addStatus = addHoldingStatusClicked.get()

    readAllTradesFile = open("allTimeTrades.txt","r")
    readAllTrades = readAllTradesFile.read()
    allTradesList = readAllTrades.split("\n")#get the previous current holdings and make it into a list
    #print(allTradesList[0].split())

    if addHoldingStatusClicked.get() == "BUY":
        writeAllTrades = open("allTimeTrades.txt","w")
        writeAllTrades.writelines(addStatus+" "+addTicker+" "+addPrice+" "+addShares+" "+addDate+" "+addTarget+" "+str(round(originalStockValue, 2))+" "+str(round(currentStockValue, 2))+" "+str(round(profitLossValue, 2))+" "+str(round(profitLossPercentage, 2)) +"\n")#add the new holding to the txt file
        for x in range(len(allTradesList)-1):#this prevents that there are no empty lines in the txt file
            writeAllTrades.writelines(allTradesList[x]+"\n")#add the previous holdings to the txt file
        writeAllTrades.writelines(allTradesList[len(allTradesList)-1])
        writeAllTrades.close()

        readCurrentPortfolioFile = open("currentPositions.txt","r")
        readCurrentPortfolio = readCurrentPortfolioFile.read()
        currentPortfolioList = readCurrentPortfolio.split("\n")

        tickerFound = False
        for x in range(len(currentPortfolioList)-1):#find if the ticker being added as been added before or not
            if addTicker == currentPortfolioList[x].split()[0]:
                tickerFound = True

        if tickerFound == True:#if a ticker is being added which has previous owned shares, dca is needed
            global dollarCostAverage, totalNumberShares, totalNumberShares
            dollarCostAverage = 0
            totalNumberShares = 0
            newPositions = []

            for x in range(len(currentPortfolioList)-1):#find if the ticker being added as been added before or not
                print(currentPortfolioList[x])
                if addTicker == currentPortfolioList[x].split()[0]:
                    totalNumberShares = int(addShares) + int(currentPortfolioList[x].split()[2])
                    dollarCostAverage = ((float(addShares)*float(addPrice))+(float(currentPortfolioList[x].split()[2])*float(currentPortfolioList[x].split()[1])))/totalNumberShares
                    newPositions.append(addTicker+" "+str(round(dollarCostAverage, 2))+" "+str(int(totalNumberShares)))
                else:
                    newPositions.append(currentPortfolioList[x])
            writeCurrentPortfolio = open("currentPositions.txt","w")

            for x in range(len(newPositions)-1):
                writeCurrentPortfolio.writelines(newPositions[x]+"\n")
            writeCurrentPortfolio.writelines(newPositions[len(newPositions)-1])
            writeCurrentPortfolio.close()

        elif tickerFound == False:#if a new ticker is being added to the portfolio, no dollar cost averaging is needed
            writeCurrentPortfolio = open("currentPositions.txt","w")
            writeCurrentPortfolio.writelines(addTicker+" "+addPrice+" "+addShares+"\n")#add the new holding to the txt file
            for x in range(len(currentPortfolioList)-1):#this prevents that there are no empty lines in the txt file
                writeCurrentPortfolio.writelines(currentPortfolioList[x]+"\n")#add the previous holdings to the txt file
            writeCurrentPortfolio.writelines(currentPortfolioList[len(currentPortfolioList)-1])
            writeCurrentPortfolio.close()

    elif addHoldingStatusClicked.get() == "SELL":
        #print(currentHoldingsContent)
        totalShareCount = 0

        for x in range(len(allTradesList)-1):
            if allTradesList[x].split()[1] == addTicker:
                if allTradesList[x].split()[0] == "BUY":
                    totalShareCount = totalShareCount + int(allTradesList[x].split()[3])
                if allTradesList[x].split()[0] == "SELL":
                    totalShareCount = totalShareCount - int(allTradesList[x].split()[3])
        print(totalShareCount)

        if int(addShares) <= totalShareCount:#if there are enough shares to be sold

            writeAllTrades = open("allTimeTrades.txt","w")
            writeAllTrades.writelines(addStatus+" "+addTicker+" "+addPrice+" "+addShares+" "+addDate+" "+addTarget+" "+str(round(dollarCostAverage*float(addShares), 2))+" "+str(round(addPrice, 2))+" "+str(round((dollarCostAverage*float(addShares))-float(addPrice), 2))+" "+str(round((dollarCostAverage*float(addShares))/float(addPrice), 2)) +"\n")#add the new holding to the txt file
            for x in range(len(allTradesList)-1):#this prevents that there are no empty lines in the txt file
                writeAllTrades.writelines(allTradesList[x]+"\n")#add the previous holdings to the txt file
            writeAllTrades.writelines(allTradesList[len(allTradesList)-1])
            writeAllTrades.close()

            readCurrentPortfolioFile = open("currentPositions.txt","r")
            readCurrentPortfolio = readCurrentPortfolioFile.read()
            currentPortfolioList = readCurrentPortfolio.split("\n")

            tickerFound = False
            for x in range(len(currentPortfolioList)-1):#find if the ticker being added as been added before or not
                if addTicker == currentPortfolioList[x].split()[0]:
                    tickerFound = True

            if tickerFound == True:#if a ticker is being added which has previous owned shares, dca is needed

                dollarCostAverage = 0
                totalNumberShares = 0
                newPositions = []

                for x in range(len(currentPortfolioList)-1):#find if the ticker being added as been added before or not
                    print(currentPortfolioList[x])
                    if addTicker == currentPortfolioList[x].split()[0]:
                        totalNumberShares = int(currentPortfolioList[x].split()[2]) - int(addShares)
                        if totalNumberShares == 0:
                            pass
                        else:
                            dollarCostAverage = float(currentPortfolioList[x].split()[1])
                            newPositions.append(addTicker+" "+str(round(dollarCostAverage , 2))+" "+str(int(totalNumberShares)))
                    else:
                        newPositions.append(currentPortfolioList[x])
                writeCurrentPortfolio = open("currentPositions.txt","w")

                for x in range(len(newPositions)):
                    writeCurrentPortfolio.writelines(newPositions[x]+"\n")
                writeCurrentPortfolio.close()

            elif tickerFound == False:#make allert message that you are trying to sell a stock which you dont own
                print("Not enough Shares to be sold")

        else:#show an error message that there are not enough shares to be sold
            print("ERROR NOT ENOUGH SHARES")
    updateCurrentPortfolioPrices()





def tickerSearch2():
    #print(tickerEntry2.get())
    plotGraphTwo(str(tickerEntry2.get()))
    #print(graph2CheckButton5Var.get())


tickerButton2 = Button(root, text="Search",bg="black", fg="#39FF14", command = tickerSearch2)
tickerButton2.place(x=1410, y=33)

addHoldingBTN = Button(root, text="Add New Holding",bg="black", fg="#39FF14", command = addNewHolding, width = 16)
addHoldingBTN.place(x=640, y=33)

showPortfolioBTN = Button(root, text="Show Current Portfolio",bg="black", fg="#39FF14", command = showCurrentPortfolio, width = 16)
showPortfolioBTN.place(x=640, y=60)

addHoldingEntryTicker = Entry(root, width=10)
addHoldingEntryTicker.insert(0,"")
addHoldingEntryTicker.configure(fg="black")
addHoldingEntryTicker.place(x=10,y=30)
addHoldingEntryTickerLabel = Label(root, text="Ticker",width=10, bg="black", fg="#39FF14").place(x=10,y=3)

addHoldingEntryPrice = Entry(root, width=10)
addHoldingEntryPrice.insert(0,"")
addHoldingEntryPrice.configure(fg="black")
addHoldingEntryPrice.place(x=120,y=30)
addHoldingEntryPricelabel = Label(root, text="Price",width=10, bg="black", fg="#39FF14").place(x=120,y=3)

addHoldingEntryShares = Entry(root, width=10)
addHoldingEntryShares.insert(0,"")
addHoldingEntryShares.configure(fg="black")
addHoldingEntryShares.place(x=230,y=30)
addHoldingEntrySharesShares = Label(root, text="# of Shares",width=10, bg="black", fg="#39FF14").place(x=230,y=3)

addHoldingEntryDate = Entry(root, width=10)
addHoldingEntryDate.insert(0,"")
addHoldingEntryDate.configure(fg="black")
addHoldingEntryDate.place(x=340,y=30)
addHoldingEntryDateLabel = Label(root, text="Purchase Date",width=10, bg="black", fg="#39FF14").place(x=340,y=3)

addHoldingEntryTarget = Entry(root, width=10)
addHoldingEntryTarget.insert(0,"")
addHoldingEntryTarget.configure(fg="black")
addHoldingEntryTarget.place(x=450,y=30)
addHoldingEntryTargetLabel = Label(root, text="Target Price",width=10, bg="black", fg="#39FF14").place(x=450,y=3)

addHoldingStatusOptions = [
    "BUY",
    "SELL"
]

addHoldingStatusClicked = StringVar()
addHoldingStatusClicked.set( "BUY" )

addHoldingStatus = OptionMenu( root , addHoldingStatusClicked , *addHoldingStatusOptions )
addHoldingStatus.configure(width=5, bg="black", fg="#39FF14")
addHoldingStatus.place(x=560, y=30)


graphOptions = [
    "Close Prices",
    "Candle Stick",
    "Graph 3",
    "Graph 4",
    "Graph 5",
    "Graph 6",
    "Graph 7"
]

graphIntervals = [
    "1 Minute",
    "5 Minute",
    "30 Minute",
    "1 Hour",
    "1 Day",
    "7 Days",
    "30 days",
    "1 Month"
]

graphTimeFrame = [
    "1 Day",
    "1 Week",
    "2 Weeks",
    "1 Month",
    "3 Months",
    "6 Months",
    "1 Year",
    "2 Years",
    "5 Years"
]



graphMenu2Clicked = StringVar()
graphMenu2Clicked.set( "Close Prices" )

graphInterval2Clicked = StringVar()
graphInterval2Clicked.set( "1 Day" )

graphTimeFrame2Clicked = StringVar()
graphTimeFrame2Clicked.set( "1 Year" )

graph2Menu = OptionMenu( root , graphMenu2Clicked , *graphOptions)
graph2Menu.configure(width=8, bg="black", fg="#39FF14")
graph2Menu.place(x=1240, y=60)

graph2Interval = OptionMenu( root , graphInterval2Clicked , *graphIntervals )
graph2Interval.configure(width=8, bg="black", fg="#39FF14")
graph2Interval.place(x=1365, y=60)

graph2TimeFrame = OptionMenu( root , graphTimeFrame2Clicked , *graphTimeFrame )
graph2TimeFrame.configure(width=8, bg="black", fg="#39FF14")
graph2TimeFrame.place(x=1470, y=60)

graph2CheckButton1 = Checkbutton(root, text="Trend Lines")
graph2CheckButton1.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton1.place(x=800, y=33)

graph2CheckButton2 = Checkbutton(root, text="Res. Lines")
graph2CheckButton2.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton2.place(x=800,y=60)

graph2CheckButton3Var = IntVar()
graph2CheckButton3 = Checkbutton(root, text="200 Day MA", variable=graph2CheckButton3Var)
graph2CheckButton3.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton3.place(x=910,y=33)

graph2CheckButton4Var = IntVar()
graph2CheckButton4 = Checkbutton(root, text="50 Day MA", variable=graph2CheckButton4Var)
graph2CheckButton4.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton4.place(x=910,y=60)

graph2CheckButton5Var = IntVar()
graph2CheckButton5 = Checkbutton(root, text="RSI", variable=graph2CheckButton5Var)
graph2CheckButton5.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton5.place(x=1020,y=33)

graph2CheckButton6Var = IntVar()
graph2CheckButton6 = Checkbutton(root, text="OBV", variable=graph2CheckButton6Var)
graph2CheckButton6.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton6.place(x=1020,y=60)

graph2CheckButton7 = Checkbutton(root, text="Fib. Res.")
graph2CheckButton7.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton7.place(x=1130,y=33)

graph2CheckButton8Var = IntVar()
graph2CheckButton8 = Checkbutton(root, text="Boll. Bands", variable=graph2CheckButton8Var)
graph2CheckButton8.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton8.place(x=1130,y=60)

graph2CheckButton9Var = IntVar()
graph2CheckButton9 = Checkbutton(root, text="12 Day EMA", variable=graph2CheckButton9Var)
graph2CheckButton9.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton9.place(x=800,y=6)

graph2CheckButton10Var = IntVar()
graph2CheckButton10 = Checkbutton(root, text="26 Day EMA", variable=graph2CheckButton10Var)
graph2CheckButton10.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton10.place(x=910,y=6)

graph2CheckButton11Var = IntVar()
graph2CheckButton11 = Checkbutton(root, text="MACD", variable=graph2CheckButton11Var)
graph2CheckButton11.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton11.place(x=1020,y=6)

graph2CheckButton12Var = IntVar()
graph2CheckButton12 = Checkbutton(root, text="ADX", variable=graph2CheckButton12Var)
graph2CheckButton12.configure(width=11, bg="black", fg="#39FF14")
graph2CheckButton12.place(x=1130,y=6)

figureCount = 0

def plotGraphTwo(stockTicker):
    clearAllGraphs()

    global figureCount
    figureCount = figureCount + 1
    #print(graphTimeFrame2Clicked.get())
    plotTwoTimeFrame = 0
    plotTwoInterval = 0



    if graphTimeFrame2Clicked.get() == "1 Day":
        pass
    if graphTimeFrame2Clicked.get() == "1 Week":
        pass
    if graphTimeFrame2Clicked.get() == "2 Weeks":
        pass
    if graphTimeFrame2Clicked.get() == "1 Month":
        plotTwoTimeFrame = 31
    if graphTimeFrame2Clicked.get() == "3 Months":
        plotTwoTimeFrame = 63
        if len(si.get_data(stockTicker)) > 63:

            try:
                plotTwoMaxTimeFrame = 263
            except:
                plotTwoMaxTimeFrame = 63
        else:
            plotTwoMaxTimeFrame = len(si.get_data(stockTicker))
            plotTwoTimeFrame = len(si.get_data(stockTicker))
    if graphTimeFrame2Clicked.get() == "6 Months":
        if len(si.get_data(stockTicker)) > 126:
            plotTwoTimeFrame = 126
            if len(si.get_data(stockTicker)) > 326:
                plotTwoMaxTimeFrame = 326
            else:
                plotTwoMaxTimeFrame = len(si.get_data(stockTicker))

        else:
            plotTwoMaxTimeFrame = len(si.get_data(stockTicker))
            plotTwoTimeFrame = len(si.get_data(stockTicker))

        print(plotTwoMaxTimeFrame)
        print(plotTwoTimeFrame)

    if graphTimeFrame2Clicked.get() == "1 Year":
        if len(si.get_data(stockTicker)) > 253:
            plotTwoTimeFrame = 253
            try:
                plotTwoMaxTimeFrame = 453
            except:
                plotTwoMaxTimeFrame = 253
        else:
            plotTwoMaxTimeFrame = len(si.get_data(stockTicker))
            plotTwoTimeFrame = len(si.get_data(stockTicker))
        #print(plotTwoMaxTimeFrame)
        #print(plotTwoTimeFrame)

    if graphTimeFrame2Clicked.get() == "2 Years":

        if len(si.get_data(stockTicker)) > 506:
            plotTwoTimeFrame = 506
            try:
                plotTwoMaxTimeFrame = 706
            except:
                plotTwoMaxTimeFrame = 506
        else:
            plotTwoMaxTimeFrame = len(si.get_data(stockTicker))
            plotTwoTimeFrame = len(si.get_data(stockTicker))

    if graphTimeFrame2Clicked.get() == "5 Years":
        if len(si.get_data(stockTicker)) > 1265:
            plotTwoTimeFrame = 1265
        else:
            plotTwoMaxTimeFrame = len(si.get_data(stockTicker))
            plotTwoTimeFrame = len(si.get_data(stockTicker))



    #plotTwoMaxTimeFrame = len(si.get_data(stockTicker)) #sets the max timeframe to the absolute max available data



    #print(plotTwoMaxTimeFrame)

    # the figure that will contain the plot
    if figureCount == 0:
        pass
    else:
        try:
            fig.clf()#
        except:
            pass

    if graph2CheckButton5Var.get() == 0:
        fig = Figure(figsize = (16.5, 6), dpi = 100)
        #figCandle = mpf.figure(figsize = (19, 9), dpi = 100) #add the grid to the graph background
    if graph2CheckButton5Var.get() == 1 and graph2CheckButton6Var.get() == 0: #if RSI is checked and OBV not checked

        fig = Figure(figsize = (16.5, 6), dpi = 100)
        fig2 = Figure(figsize = (16.5, 3), dpi = 100)

    if graph2CheckButton6Var.get() == 1 and graph2CheckButton5Var.get() == 0: #if RSI not checked and OBV is checked
        fig = Figure(figsize = (16.5, 6), dpi = 100)
        fig3 = Figure(figsize = (16.5, 3), dpi = 100)

    if graph2CheckButton6Var.get() == 1 and graph2CheckButton5Var.get() == 1:
        fig = Figure(figsize = (16.5, 3), dpi = 100)
        fig2 = Figure(figsize = (16.5, 3), dpi = 100)
        fig3 = Figure(figsize = (16.5, 3), dpi = 100)

    if graph2CheckButton11Var.get() == 1:
        fig = Figure(figsize = (19, 6), dpi = 100)

        fig4 = Figure(figsize = (19, 3), dpi = 100)
        plot4 = fig4.add_subplot(111)

    if graph2CheckButton12Var.get() == 1:
        fig = Figure(figsize = (19, 6), dpi = 100)
        fig5 = Figure(figsize = (19, 3), dpi = 100)
        plot5 = fig5.add_subplot(111)


    stock = si.get_data(stockTicker)

    #print(stock.values[0][5])
    #print(stock.axes[0][0])

    openPrices = []
    closePrices = []
    highPrices = []
    lowPrices = []
    stockDates = []
    volumeRange = []

    rangeCandleData = []


    allTimeOpenPrices = []
    allTimeClosePrices = []
    allTimeHighPrices = []
    allTimeLowPrices = []
    allTimeStockDates = []
    allTimeVolume = []

    allTimeCandleData = []


    for x in range(len(si.get_data(stockTicker))-plotTwoTimeFrame, len(si.get_data(stockTicker))): #find the prices of open for the dates for specified time frame
        openPrices.append(stock.get("open")[x])
        closePrices.append(stock.get("close")[x])
        highPrices.append(stock.get("high")[x])
        lowPrices.append(stock.get("low")[x])
        stockDates.append(stock.axes[0][x])
        volumeRange.append(stock.values[x][5])


    for x in range(len(si.get_data(stockTicker))-plotTwoMaxTimeFrame, len(si.get_data(stockTicker))):#find the prices of open for the dates for all time
        allTimeOpenPrices.append(stock.get("open")[x])
        allTimeClosePrices.append(stock.get("close")[x])
        allTimeHighPrices.append(stock.get("high")[x])
        allTimeLowPrices.append(stock.get("low")[x])
        allTimeStockDates.append(stock.axes[0][x])
        allTimeVolume.append(stock.values[x][5])

    #print(volumeRange)


    # adding the subplot of open pricees
    plot1 = fig.add_subplot(111)
    #fig.close()
    #plotCandle = figCandle.add_subplot(111)

    #________________________________________________
#finding the RSI Value for the correct time period
    def findRSI():
        priceChange = []

        positiveChange = []
        negativeChange = []

        rsData = []
        rsiData = []

        totalGain = 0
        totalLoss = 0

        previousGain = 0
        previousLoss = 0
        averageGain = 0
        averageLoss = 0

        rsValue = 0
        rsiValue = 0

        for x in range(1, 15):#find the RSI for the first 14 days

            priceChangeVal = allTimeClosePrices[x]-allTimeClosePrices[x-1]

            if priceChangeVal > 0: #add to the positive oruce change list
                        #positiveChange.append(priceChangeVal)
                totalGain = totalGain + priceChangeVal

            if priceChangeVal < 0:#add to the negative oruce change list
                        #negativeChange.append(priceChangeVal)
                totalLoss = totalLoss + (priceChangeVal*-1)

            if priceChangeVal == 0:
                pass

        positiveChange.append(totalGain/14)
        negativeChange.append(totalLoss/14)

        previousGain = positiveChange[0]
        previousLoss = negativeChange[0]

        #for x in range(15):
        #    rsiData.append((100-(100/(1+((totalGain/14)/(totalLoss/14))))))

        for x in range(14, len(allTimeClosePrices)-1):#find the rsi for the rest of the days
            totalGain = 0
            totalLoss = 0

            priceChangeVal = allTimeClosePrices[x]-allTimeClosePrices[x-1]

            if priceChangeVal > 0: #add to the positive price change list
                        #positiveChange.append(priceChangeVal)
                totalGain = (previousGain*13) + priceChangeVal
                totalLoss = (previousLoss*13)

            if priceChangeVal < 0:#add to the negative price change list
                        #negativeChange.append(priceChangeVal)
                totalLoss = (previousLoss*13) + (priceChangeVal*-1)
                totalGain = (previousGain*13)

            if priceChangeVal == 0:
                totalLoss = (previousLoss*13)
                totalGain = (previousGain*13)

            averageGain = totalGain/14
            averageLoss = totalLoss/14

            rsValue = averageGain/averageLoss
            rsiValue = (100-(100/(1+rsValue)))

            rsiData.append(rsiValue)

            previousGain = averageGain
            previousLoss = averageLoss

        plot2 = fig2.add_subplot(111)

        rsiUpperLimit = []
        rsiLowerLimit = []

        rsiDataRange = []
        rsiDataRangeDates = []


        if len(rsiData) > len(closePrices):
            for x in range(len(closePrices)):
                rsiDataRange.append(rsiData[len(rsiData)-len(closePrices)+x])

            plot2.plot(stockDates, rsiDataRange, linewidth=1)

        elif len(rsiData) < len(closePrices):
            for x in range(len(rsiData)):
                rsiDataRange.append(rsiData[x])
                rsiDataRangeDates.append(stockDates[len(stockDates)-len(rsiData)+x])
                #print(rsiData[x])
            plot2.plot(rsiDataRangeDates, rsiDataRange, linewidth=1)

        elif len(rsiData) == len(closePrices):
            pass


        for x in range(len(stockDates)):
            rsiUpperLimit.append(70)
            rsiLowerLimit.append(30)



        plot2.plot(stockDates, rsiUpperLimit, linewidth=1)
        plot2.plot(stockDates, rsiLowerLimit, linewidth=1)



        fig2.suptitle("Relative Strength Index", color="#39FF14")
        fig2.tight_layout()
        fig2.set_facecolor("black")

        plot2.set_facecolor("black")
        plot2.tick_params(axis='x', colors='#39FF14')
        plot2.tick_params(axis='y', colors='#39FF14')




        global canvas2
        canvas2 = FigureCanvasTkAgg(fig2, master = root)
        canvas2.draw()
        canvas2.get_tk_widget().place(x=10, y=700) #normally 960 not 600
#________________________________________________
#find the data for the OBV chart
    def findOBV():
        plot3 = fig3.add_subplot(111)

        obvDataAllTime = []

        obvDataRange = []

        previousObv = 0
        currentObv = allTimeVolume[0]

        for x in range(len(allTimeVolume)):
            #print(str(allTimeVolume[x])+"   "+str(allTimeClosePrices[x]))
            if allTimeClosePrices[x] > allTimeClosePrices[x-1]:
                currentObv = previousObv + allTimeVolume[x]

            if allTimeClosePrices[x] < allTimeClosePrices[x-1]:
                currentObv = previousObv - allTimeVolume[x]

            if allTimeClosePrices[x] == allTimeClosePrices[x-1]:
                currentObv = previousObv

            obvDataAllTime.append(currentObv)
            previousObv = currentObv

        obvZeroRange = []

        for x in range(len(closePrices)):
            obvDataRange.append(obvDataAllTime[len(obvDataAllTime)-len(closePrices)+x])
            obvZeroRange.append(0)


        plot3.plot(allTimeStockDates, obvDataAllTime, linewidth=1)
        plot3.plot(stockDates, obvZeroRange)


        fig3.tight_layout()
        fig3.suptitle("On Balance Volume", color="#39FF14")

        plot3.set_facecolor("black")
        plot3.tick_params(axis='x', colors='#39FF14')
        plot3.tick_params(axis='y', colors='#39FF14')

        fig3.set_facecolor("black")

        global canvas3
        canvas3 = FigureCanvasTkAgg(fig3, master = root)
        canvas3.draw()
        canvas3.get_tk_widget().place(x=10, y=700)

#________________________________________________
    #finding 200 day moving average
    def find200MA():
        MA200AllTime = []
        MA200Range = []
        MA200RangeDates = []

        MA200Total = 0

        for x in range(200, len(allTimeClosePrices)):
            MA200Total = 0
            for y in range(200):
                MA200Total = MA200Total + allTimeClosePrices[x-200+y]


            #print(MA50Total/50)
            MA200AllTime.append(MA200Total/200)
        if len(closePrices) < len(MA200AllTime): #make the 50 day MA if there are enough dates
            for x in range(len(closePrices)):
                MA200Range.append(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                #print(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                #MA50RangeDates.append(stockDates[len(MA50AllTime)-len(closePrices)+x])

                #print(stockDates[len(MA50AllTime)-len(closePrices)+x])
            plot1.plot(stockDates, MA200Range, color="green", linewidth=1, label="200 MA")

        elif len(closePrices) > len(MA200AllTime): #make the 50 day MA if there arent enough dates
            for x in range(len(MA200AllTime)):

                MA200Range.append(MA200AllTime[x])
                #print(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                MA200RangeDates.append(stockDates[len(stockDates)-len(MA200AllTime)+x])

                #print(stockDates[len(MA50AllTime)-len(closePrices)+x])
            plot1.plot(MA200RangeDates, MA200Range, color="green", linewidth=1, label="200 MA")

        elif len(closePrices) == len(MA200AllTime):
            for x in range(len(closePrices)):
                MA200Range.append(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                #print(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                #MA50RangeDates.append(stockDates[len(MA50AllTime)-len(closePrices)+x])

                #print(stockDates[len(MA50AllTime)-len(closePrices)+x])
            plot1.plot(stockDates, MA200Range, color="green", linewidth=1)

        #print(MA200AllTime)

        #print(len(stockDates))
        #print(len(MA200Range))
        #print(len(MA200AllTime))
#________________________________________________
#finding 50 day moving average
    def find50MA():
        MA50AllTime = []
        MA50Range = []
        MA50RangeDates = []

        MA50Total = 0

        for x in range(50, len(allTimeClosePrices)):
            MA50Total = 0
            for y in range(50):
                MA50Total = MA50Total + allTimeClosePrices[x-50+y]


            #print(MA50Total/50)
            MA50AllTime.append(MA50Total/50)

        if len(closePrices) < len(MA50AllTime): #make the 50 day MA if there are enough dates
            for x in range(len(closePrices)):
                MA50Range.append(MA50AllTime[len(MA50AllTime)-len(closePrices)+x])
                #print(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                #MA50RangeDates.append(stockDates[len(MA50AllTime)-len(closePrices)+x])

                #print(stockDates[len(MA50AllTime)-len(closePrices)+x])
            plot1.plot(stockDates, MA50Range, color="red", linewidth=1, label="50 MA")

        elif len(closePrices) > len(MA50AllTime): #make the 50 day MA if there arent enough dates
            for x in range(len(MA50AllTime)):

                MA50Range.append(MA50AllTime[x])
                #print(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                MA50RangeDates.append(stockDates[len(stockDates)-len(MA50AllTime)+x])

                #print(stockDates[len(MA50AllTime)-len(closePrices)+x])
            plot1.plot(MA50RangeDates, MA50Range, color="red", linewidth=1, label="50 MA")

        elif len(closePrices) == len(MA50AllTime):
            pass
#________________________________________________

    #finding the Bollinger bands values and data
    #we need to use a 20 day MA
    #find the standard deviation of the 20 MA
    #Upper Band = 20DayMA + (20DayMASD*2)
    #Lower Band = 20DayMA - (20DayMASD*2)
    def findBolBands():
        MA20AllTime = []
        MA20Range = []
        MA20RangeDates = []

        MA20Total = 0

        for x in range(20, len(allTimeClosePrices)):
            MA20Total = 0
            for y in range(20):
                MA20Total = MA20Total + allTimeClosePrices[x-20+y]

            MA20AllTime.append(MA20Total/20)
            #print(MA20Total/20)

        if len(closePrices) < len(MA20AllTime): #make the 20 day MA if there are enough dates
            for x in range(len(closePrices)):
                MA20Range.append(MA20AllTime[len(MA20AllTime)-len(closePrices)+x])
                #print(MA20AllTime[len(closePrices)-len(MA20AllTime)+x])
                MA20RangeDates.append(stockDates[x])


            plot1.plot(MA20RangeDates, MA20Range, color="green", linewidth=1)

        elif len(closePrices) > len(MA20AllTime): #make the 20 day MA if there arent enough dates
            for x in range(len(MA20AllTime)):

                MA20Range.append(MA20AllTime[x])
                MA20RangeDates.append(stockDates[len(stockDates)-len(MA20AllTime)+x])

            plot1.plot(MA20RangeDates, MA20Range, color="green", linewidth=1)

        elif len(closePrices) == len(MA20AllTime):
            pass


        #finding the standard deviation of the 20 Day MA

        SDFinal = []
        UpperBollingerBand = []
        LowerBollingerBand = []

        UpperBollingerBandRange = []
        LowerBollingerBandRange = []

        for x in range(len(allTimeClosePrices)-20):
            SDFirstStep = []
            SDFirstStepTotal = 0
            SDFirstStepMean = 0
            for y in range(20):
                SDFirstStep.append((allTimeClosePrices[x+y]-MA20AllTime[x])*(allTimeClosePrices[x+y]-MA20AllTime[x]))

            for y in range(len(SDFirstStep)):
                SDFirstStepTotal = SDFirstStepTotal + SDFirstStep[y]

            SDFirstStepMean = SDFirstStepTotal/20
            SDFinal.append(math.sqrt(SDFirstStepMean))

        for x in range(len(SDFinal)):
            UpperBollingerBand.append(MA20AllTime[x]+(SDFinal[x]*2))
            LowerBollingerBand.append(MA20AllTime[x]-(SDFinal[x]*2))

        for x in range(len(MA20RangeDates)):
            UpperBollingerBandRange.append(UpperBollingerBand[len(UpperBollingerBand)-len(MA20RangeDates)+x])
            LowerBollingerBandRange.append(LowerBollingerBand[len(LowerBollingerBand)-len(MA20RangeDates)+x])

        #print("")
        #print(len(allTimeClosePrices))
        #print(len(MA20Range))
        #print(len(MA20RangeDates))
        #print(len(UpperBollingerBandRange))

        plot1.plot(MA20RangeDates, UpperBollingerBandRange, color="#39FF14", linewidth=1, alpha=0.1)
        plot1.plot(MA20RangeDates, LowerBollingerBandRange, color="#39FF14", linewidth=1, alpha=0.1)



        plot1.fill_between(MA20RangeDates, UpperBollingerBandRange, LowerBollingerBandRange, color="#39FF14", alpha=0.1, label="Boll. Band.")


    #________________________________________________
        #finding the 12 day EMA
    def find12EMA(ema12Var):
        MA12AllTime = []
        MA12Range = []
        MA12RangeDates = []

        MA12Total = 0

        for x in range(12, len(allTimeClosePrices)):
            MA12Total = 0
            for y in range(12):
                MA12Total = MA12Total + allTimeClosePrices[x-12+y]

            MA12AllTime.append(MA12Total/12)
            #print(MA12Total/12)

        if len(closePrices) < len(MA12AllTime): #make the 12 day MA if there are enough dates
            for x in range(len(closePrices)):
                MA12Range.append(MA12AllTime[len(MA12AllTime)-len(closePrices)+x])
                #print(MA14AllTime[len(closePrices)-len(MA14AllTime)+x])
                MA12RangeDates.append(stockDates[x])


        elif len(closePrices) > len(MA12AllTime): #make the 12 day MA if there arent enough dates
            for x in range(len(MA12AllTime)):

                MA12Range.append(MA12AllTime[x])
                MA12RangeDates.append(stockDates[len(stockDates)-len(MA12AllTime)+x])


        elif len(closePrices) == len(MA12AllTime):
            pass

        previousDayEMA12 = 0
        currentDayEMA12 = 0
        global EMA12AllTime
        EMA12AllTime = []

        EMA12AllTimeDates = []
        EMA12Range = []
        EMA12RangeDates = []
        closePriceEMA = 0

        smoothingConstant12 = 2/(12+1)

        currentDayEMA12 = MA12AllTime[0]

        for x in range(1, len(MA12AllTime)):
            #EMA = {Close - EMA(previous day)} x multiplier + EMA(previous day).
            previousDayEMA12 = currentDayEMA12
            closePriceEMA12 = allTimeClosePrices[len(allTimeClosePrices)-len(MA12AllTime)+x]

            currentDayEMA12 = ((closePriceEMA12-previousDayEMA12) * smoothingConstant12) + previousDayEMA12

            #print(currentDayEMA)
            EMA12AllTime.append(currentDayEMA12)
            EMA12AllTimeDates.append(allTimeStockDates[len(allTimeClosePrices)-len(MA12AllTime)+x])


        #print(EMA12Range)

        if len(closePrices) < len(EMA12AllTime): #make the 12 day EMA if there are enough dates
            for x in range(len(closePrices)):
                EMA12Range.append(EMA12AllTime[len(EMA12AllTime)-len(closePrices)+x])
                #print(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                #MA50RangeDates.append(stockDates[len(MA50AllTime)-len(closePrices)+x])

                #print(stockDates[len(MA50AllTime)-len(closePrices)+x])

            if ema12Var == 0:
                plot1.plot(stockDates, EMA12Range, color="blue", linewidth=1, label="12 EMA")
            if ema12Var == 1:
                #plot4.plot(stockDates, EMA12Range, color="blue", linewidth=1, label="12 EMA")
                pass
            if ema12Var == 2:
                plot1.plot(stockDates, EMA12Range, color="blue", linewidth=1, label="12 EMA")
                plot1.plot(stockDates, EMA12Range, color="blue", linewidth=1, label="12 EMA")

        elif len(closePrices) > len(EMA12AllTime): #make the 50 day MA if there arent enough dates
            for x in range(len(MA12Range)):
                EMA12Range.append(EMA12AllTime[len(EMA12AllTime)-len(EMA12Range)+x-1])
                EMA12RangeDates.append(MA12RangeDates[x])

            if ema12Var == 0:
                plot1.plot(EMA12AllTimeDates, EMA12AllTime, color="blue", linewidth=1, label="12 EMA")
            if ema12Var == 1:
                #plot4.plot(EMA12AllTimeDates, EMA12AllTime, color="blue", linewidth=1, label="12 EMA")
                pass
            if ema12Var == 2:
                plot1.plot(EMA12AllTimeDates, EMA12AllTime, color="blue", linewidth=1, label="12 EMA")
                plot4.plot(EMA12AllTimeDates, EMA12AllTime, color="blue", linewidth=1, label="12 EMA")

        elif len(closePrices) == len(EMA12AllTime):
            pass
    #________________________________________________
    #finding the 26 day EMA

    def find26EMA(ema26Var):
        MA26AllTime = []
        MA26Range = []
        MA26RangeDates = []

        MA26Total = 0

        for x in range(26, len(allTimeClosePrices)):
            MA12Total = 0
            for y in range(26):
                MA26Total = MA26Total + allTimeClosePrices[x-26+y]

            MA26AllTime.append(MA26Total/26)
            #print(MA12Total/12)

        if len(closePrices) < len(MA26AllTime): #make the 26 day MA if there are enough dates
            for x in range(len(closePrices)):
                MA26Range.append(MA26AllTime[len(MA26AllTime)-len(closePrices)+x])
                #print(MA14AllTime[len(closePrices)-len(MA14AllTime)+x])
                MA26RangeDates.append(stockDates[x])


        elif len(closePrices) > len(MA26AllTime): #make the 26 day MA if there arent enough dates
            for x in range(len(MA26AllTime)):

                MA26Range.append(MA26AllTime[x])
                MA26RangeDates.append(stockDates[len(stockDates)-len(MA26AllTime)+x])


        elif len(closePrices) == len(MA26AllTime):
            pass

        previousDayEMA26 = 0
        currentDayEMA26 = 0
        global EMA26AllTime
        EMA26AllTime = []
        global EMA26AllTimeDates
        EMA26AllTimeDates = []

        EMA26Range = []
        EMA26RangeDates = []
        closePriceEMA26 = 0

        smoothingConstant26 = 2/(26+1)

        currentDayEMA26 = MA26AllTime[0]

        for x in range(1, len(MA26AllTime)):
            #EMA = {Close - EMA(previous day)} x multiplier + EMA(previous day).
            previousDayEMA26 = currentDayEMA26
            closePriceEMA26 = allTimeClosePrices[len(allTimeClosePrices)-len(MA26AllTime)+x]

            currentDayEMA26 = ((closePriceEMA26-previousDayEMA26) * smoothingConstant26) + previousDayEMA26

            #print(currentDayEMA)
            EMA26AllTime.append(currentDayEMA26)
            EMA26AllTimeDates.append(allTimeStockDates[len(allTimeClosePrices)-len(MA26AllTime)+x])


        #print(EMA12Range)

        if len(closePrices) < len(EMA26AllTime): #make the 12 day EMA if there are enough dates
            for x in range(len(closePrices)):
                EMA26Range.append(EMA26AllTime[len(EMA26AllTime)-len(closePrices)+x])
                #print(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                #MA50RangeDates.append(stockDates[len(MA50AllTime)-len(closePrices)+x])

                #print(stockDates[len(MA50AllTime)-len(closePrices)+x])
            if ema26Var == 0:
                plot1.plot(stockDates, EMA26Range, color="red", linewidth=1, label="26 EMA")
            if ema26Var == 1:
                #plot4.plot(stockDates, EMA26Range, color="red", linewidth=1, label="26 EMA")
                pass
            if ema26Var == 2:
                plot1.plot(stockDates, EMA26Range, color="red", linewidth=1, label="26 EMA")
                plot4.plot(stockDates, EMA26Range, color="red", linewidth=1, label="26 EMA")

        elif len(closePrices) > len(EMA26AllTime): #make the 50 day MA if there arent enough dates
            for x in range(len(MA26Range)):
                EMA26Range.append(EMA26AllTime[len(EMA26AllTime)-len(EMA26Range)+x-1])
                EMA26RangeDates.append(MA26RangeDates[x])

            if ema26Var == 0:
                plot1.plot(EMA26AllTimeDates, EMA26AllTime, color="red", linewidth=1, label="26 EMA")
            if ema26Var == 1:
                #plot4.plot(EMA26AllTimeDates, EMA26AllTime, color="red", linewidth=1, label="26 EMA")
                pass
            if ema26Var == 2:
                plot1.plot(EMA26AllTimeDates, EMA26AllTime, color="red", linewidth=1, label="26 EMA")
                plot4.plot(EMA26AllTimeDates, EMA26AllTime, color="red", linewidth=1, label="26 EMA")


        elif len(closePrices) == len(EMA26AllTime):
            pass

    #________________________________________________
    #find and draw the MACD graph
    def findMACD():
        #plot4 = fig4.add_subplot(111)

        macdAllTime = []
        macdRange = []
        macdRangeDates = []

        for x in range(len(EMA26AllTime)):

            macdAllTime.append(EMA12AllTime[x+14]-EMA26AllTime[x])

        MA9AllTime = []
        MA9Range = []
        MA9RangeDates = []

        MA9Total = 0

        for x in range(9, len(macdAllTime)):
            MA9Total = 0
            for y in range(9):
                MA9Total = MA9Total + macdAllTime[x-9+y]

            MA9AllTime.append(MA9Total/9)

        previousDayEMA9 = 0
        currentDayEMA9 = 0
        global EMA9AllTime
        EMA9AllTime = []

        EMA9AllTimeDates = []
        EMA9Range = []
        EMA9RangeDates = []
        closePriceEMA9 = 0

        smoothingConstant9 = 2/(9+1)

        currentDayEMA9 = MA9AllTime[0]

        for x in range(1, len(MA9AllTime)):
            #EMA = {Close - EMA(previous day)} x multiplier + EMA(previous day).
            previousDayEMA9 = currentDayEMA9
            closePriceEMA9 = macdAllTime[len(macdAllTime)-len(MA9AllTime)+x]

            currentDayEMA9 = ((closePriceEMA9-previousDayEMA9) * smoothingConstant9) + previousDayEMA9

            #print(currentDayEMA)
            EMA9AllTime.append(currentDayEMA9)
            EMA9AllTimeDates.append(allTimeStockDates[len(macdAllTime)-len(MA9AllTime)+x+27])

        macdBarsAllTime = []
        macdBarsRange = []
        macdDifference = 0
        macdBarAllTimeColor = []
        macdBarRangeColor = []

        for x in range(len(EMA9AllTime)):
            macdDifference = macdAllTime[len(macdAllTime)-len(EMA9AllTime)+x]-EMA9AllTime[x]
            macdBarsAllTime.append(macdDifference)
            if macdDifference > 0:
                macdBarAllTimeColor.append("green")
            elif macdDifference < 0:
                macdBarAllTimeColor.append("red")
            else:
                macdBarAllTimeColor.append("black")

        macdZeroValue = []

        for x in range(len(stockDates)):
            macdZeroValue.append(0)

        if len(closePrices) < len(macdAllTime): #make the 50 day MA if there are enough dates
            for x in range(len(closePrices)):
                macdRange.append(macdAllTime[len(macdAllTime)-len(closePrices)+x])
                EMA9Range.append(EMA9AllTime[len(EMA9AllTime)-len(closePrices)+x])
                macdBarsRange.append(macdBarsAllTime[len(macdBarsAllTime)-len(closePrices)+x])
                macdBarRangeColor.append(macdBarAllTimeColor[len(macdBarAllTimeColor)-len(closePrices)+x])

            plot4.plot(stockDates, macdRange, color="red", linewidth=1, label="MACD")
            plot4.plot(stockDates, EMA9Range, color="green", linewidth=1, label="9EMA")
            plot4.bar(stockDates, macdBarsRange, color=macdBarRangeColor, width=0.8)

        elif len(closePrices) > len(macdAllTime): #make the 50 day MA if there arent enough dates
            for x in range(len(macdAllTime)):

                macdRange.append(macdAllTime[x])
                macdRangeDates.append(stockDates[len(stockDates)-len(macdAllTime)+x])

            plot4.plot(macdRangeDates, macdRange, color="red", linewidth=1, label="MACD")
            plot4.plot(EMA9AllTimeDates, EMA9AllTime, color="green", linewidth=1, label="9EMA")
            plot4.bar(EMA9AllTimeDates, macdBarsAllTime, color=macdBarAllTimeColor, width=0.8)

        plot4.plot(stockDates, macdZeroValue, color="#39FF14", linewidth=0.5)

        global canvas4
        canvas4 = FigureCanvasTkAgg(fig4, master = root)
        canvas4.draw()
        canvas4.get_tk_widget().place(x=10, y=700)

        plot4.set_facecolor("black")
        plot4.tick_params(axis='x', colors='#39FF14')
        plot4.tick_params(axis='y', colors='#39FF14')

        legend4 = fig4.legend(loc='upper right', shadow=False, labelcolor = "#39FF14")

        legend4.get_frame().set_facecolor('black')

        fig4.tight_layout()
        fig4.set_facecolor("black")
    #________________________________________________
    #finding ADX
    def findADX():
        negativeDM = 0
        negativeDMAverage = 0
        negativeDMList = []
        negativeDMListRange = []
        negativeDMListRangeDates = []
        negativeDMListAverage = []

        positiveDM = 0
        positiveDMAverage = 0
        positiveDMList = []
        positiveDMListRange = []
        positiveDMListRangeDates = []
        positiveDMListAverage = []

        trueRange = 0
        trueRangeList = []
        averageTrueRange = 0
        averageTrueRangeList = []
        averageTrueRangeListRange = []
        averageTrueRangeListRangeDates = []

        optionOne = 0 #Current High – Current Low
        optionTwo = 0 #abs (Current High – Previous Close)
        optionThree = 0 #abs (Previous Close – Current Low)

        upMove = 0
        upMoveList = []

        downMove = 0
        downMoveList = []

        for x in range(1, len(allTimeClosePrices)):
            upMove = allTimeHighPrices[x]-allTimeHighPrices[x-1]
            downMove = allTimeLowPrices[x]-allTimeLowPrices[x-1]

            if upMove > downMove:
                if upMove > 0:
                    positiveDMList.append(upMove)
            else:
                positiveDMList.append(0)

            if downMove > upMove:
                if downMove > 0:
                    negativeDMList.append(downMove)
            else:
                negativeDMList.append(0)

        for x in range(1, 14):#get the first ATR Value for a 14 day period
            if (allTimeHighPrices[x]-allTimeHighPrices[x-1]) > (allTimeLowPrices[x-1]-allTimeLowPrices[x]):#get the positive DM
                positiveDM = positiveDM + max(allTimeHighPrices[x]-allTimeHighPrices[x-1], 0)

            if (allTimeLowPrices[x-1]-allTimeLowPrices[x]) > (allTimeHighPrices[x]-allTimeHighPrices[x-1]): #get the negative DM
                negativeDM = negativeDM + max(allTimeLowPrices[x-1]-allTimeLowPrices[x], 0)

            #negativeDMList.append(negativeDM)

            optionOne = allTimeHighPrices[x]-allTimeLowPrices[x]

            optionTwo = allTimeHighPrices[x]-allTimeClosePrices[x-1]
            if optionTwo > 0:
                optionTwo = optionTwo
            elif optionTwo < 0:
                optionTwo = optionTwo*-1

            optionThree = allTimeClosePrices[x-1]-allTimeLowPrices[x]
            if optionThree > 0:
                optionThree = optionThree
            elif optionThree < 0:
                optionThree = optionThree*-1

            #print(str(optionOne)+"  "+str(optionTwo)+"  "+str(optionThree)+"  "+str(max(optionOne, optionTwo, optionThree)))
            #trueRangeList.append(max(optionOne, optionTwo, optionThree))
            trueRange = trueRange + max(optionOne, optionTwo, optionThree)


        averageTrueRange = trueRange/14
        negativeDMAverage = negativeDM/14
        positiveDMAverage = positiveDM/14

        averageTrueRangeList.append(averageTrueRange)
        negativeDMListAverage.append(negativeDMAverage)
        positiveDMListAverage.append(positiveDMAverage)

        for x in range(14, len(allTimeLowPrices)):#get the rest of the ATR values
            if (allTimeHighPrices[x]-allTimeHighPrices[x-1]) > (allTimeLowPrices[x-1]-allTimeLowPrices[x]):#get the positive DM
                positiveDM = max(allTimeHighPrices[x]-allTimeHighPrices[x-1], 0)

            if (allTimeLowPrices[x-1]-allTimeLowPrices[x]) > (allTimeHighPrices[x]-allTimeHighPrices[x-1]): #get the negative DM
                negativeDM = max(allTimeLowPrices[x-1]-allTimeLowPrices[x], 0)

            if positiveDM < 0 and negativeDM < 0:#if + and - DM are negative
                positiveDM = 0
                negativeDM = 0


            optionOne = allTimeHighPrices[x]-allTimeLowPrices[x]

            optionTwo = allTimeHighPrices[x]-allTimeClosePrices[x-1]
            if optionTwo > 0:
                optionTwo = optionTwo
            elif optionTwo < 0:
                optionTwo = optionTwo*-1

            optionThree = allTimeClosePrices[x-1]-allTimeLowPrices[x]
            if optionThree > 0:
                optionThree = optionThree
            elif optionThree < 0:
                optionThree = optionThree*-1

            averageTrueRange = ((averageTrueRangeList[x-14]*13) + max(optionOne, optionTwo, optionThree))/14
            negativeDMAverage = ((negativeDMListAverage[x-14]*13) + negativeDM)/14
            positiveDMAverage = ((positiveDMListAverage[x-14]*13) + positiveDM)/14

            averageTrueRangeList.append(averageTrueRange)
            negativeDMListAverage.append(negativeDMAverage)
            positiveDMListAverage.append(positiveDMAverage)

        for x in range(len(averageTrueRangeList)):
            negativeDMList.append((negativeDMListAverage[x]/averageTrueRangeList[x])*100)
            positiveDMList.append((positiveDMListAverage[x]/averageTrueRangeList[x])*100)

        #print(negativeDMList)

        if len(closePrices) < len(averageTrueRangeList): #make the 50 day MA if there are enough dates
            for x in range(len(closePrices)):
                averageTrueRangeListRange.append(averageTrueRangeList[len(averageTrueRangeList)-len(closePrices)+x])
                negativeDMListRange.append(negativeDMList[len(averageTrueRangeList)-len(closePrices)+x])
                positiveDMListRange.append(positiveDMList[len(averageTrueRangeList)-len(closePrices)+x])
                #print(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                #MA50RangeDates.append(stockDates[len(MA50AllTime)-len(closePrices)+x])

                #print(stockDates[len(MA50AllTime)-len(closePrices)+x])
            plot5.plot(stockDates, averageTrueRangeListRange, color="blue", linewidth=1, label="14 ATR")
            plot5.plot(stockDates, negativeDMListRange, color="red", linewidth=1, label="-DM")
            plot5.plot(stockDates, positiveDMListRange, color="green", linewidth=1, label="+DM")

        elif len(closePrices) > len(averageTrueRangeList): #make the 50 day MA if there arent enough dates
            for x in range(len(averageTrueRangeList)):

                averageTrueRangeListRange.append(averageTrueRangeList[x])
                #print(MA200AllTime[len(MA200AllTime)-len(closePrices)+x])
                averageTrueRangeListRangeDates.append(stockDates[len(stockDates)-len(averageTrueRangeList)+x])

                #print(stockDates[len(MA50AllTime)-len(closePrices)+x])
            plot5.plot(averageTrueRangeListRangeDates, averageTrueRangeListRange, color="green", linewidth=1, label="14 ATR")

        global canvas5
        canvas5 = FigureCanvasTkAgg(fig5, master = root)
        canvas5.draw()
        canvas5.get_tk_widget().place(x=10, y=700)

        plot5.set_facecolor("black")
        plot5.tick_params(axis='x', colors='#39FF14')
        plot5.tick_params(axis='y', colors='#39FF14')

        legend5 = fig5.legend(loc='upper right', shadow=False, labelcolor = "#39FF14")

        legend5.get_frame().set_facecolor('black')

        fig5.tight_layout()
        fig5.set_facecolor("black")

        #print(trueRangeList)


    #________________________________________________

    if graph2CheckButton5Var.get() == 1 and graph2CheckButton6Var.get() == 0:
        findRSI()

    else:
        pass

    #print(stockDates[0])

    #________________________________________________
    #find the data for the OBV chart
    if graph2CheckButton5Var.get() == 0 and graph2CheckButton6Var.get() == 1:
        findOBV()

    #________________________________________________
    #finding 200 day moving average
    #print(graph2CheckButton3Var.get())
    if graph2CheckButton3Var.get() == 1:
        #print(len(stockDates))
        find200MA()

    #________________________________________________
    #finding 50 day moving average
    if graph2CheckButton4Var.get() == 1:
        find50MA()

    #________________________________________________

    if graph2CheckButton8Var.get() == 1:
        findBolBands()

    elif graph2CheckButton8Var.get() == 0:
        pass

    #________________________________________________
    #finding the 12 day EMA
    # EMA = {Close - EMA(previous day)} x multiplier + EMA(previous day).

    if graph2CheckButton9Var.get() == 1:
        find12EMA(0)

    elif graph2CheckButton9Var.get() == 0:
        pass

    #________________________________________________
    #finding the 26 day EMA

    if graph2CheckButton10Var.get() == 1:
        find26EMA(0)

    elif graph2CheckButton10Var.get() == 0:
        pass

    #________________________________________________
    #find the MACD values and draw the graph1Menu
    if graph2CheckButton11Var.get() == 1:
        find26EMA(1)
        find12EMA(1)
        findMACD()



    elif graph2CheckButton11Var.get() == 0:
        pass
    #________________________________________________
    #find the ADX values
    if graph2CheckButton12Var.get() == 1:
        findADX()



    elif graph2CheckButton12Var.get() == 0:
        pass
    #________________________________________________


    # plotting the graph of open prices
    plot1.plot(stockDates, closePrices, color="#39FF14", linewidth=0.5, label="200 Day MA")
    #mpf.plot(rangeCandleDataDF, type="candle", style="yahoo", ax=plot1)

    plot1.set_facecolor("black")
    plot1.tick_params(axis='x', colors='#39FF14')
    plot1.tick_params(axis='y', colors='#39FF14')

    fig.tight_layout()
    fig.set_facecolor("black")
    fig.suptitle(""+str(stockTicker), color="#39FF14")

    legend = fig.legend(loc='upper right', shadow=False, labelcolor = "#39FF14")

    legend.get_frame().set_facecolor('black')


    # creating the Tkinter canvas
    # containing the Matplotlib figure
    global canvas
    canvas = FigureCanvasTkAgg(fig, master = root)

    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(x=10, y=100)

root.mainloop()

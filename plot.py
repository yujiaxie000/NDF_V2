import matplotlib.pyplot as plt

def oriPlot(L):
    for aSlice in L:
        x = []
        y = []
        for aPoint in aSlice:
            x.append(aPoint[0])
            y.append(aPoint[1])
            plt.plot(x,y, color = 'r')
    plt.show()

def myPlot(L, Lndf):
    for aSlice in L:
        x = []
        y = []
        for aPoint in aSlice:
            x.append(aPoint[0])
            y.append(aPoint[1])
            plt.plot(x,y, color = 'r')
    for aSlice in Lndf:
        xndf = []
        yndf = []
        #print(aSlice, 'o')
        for aPoint in aSlice:
            xndf.append(aPoint[0])
            yndf.append(aPoint[1])
            plt.plot(xndf,yndf, color='b', marker='o')
    plt.show()
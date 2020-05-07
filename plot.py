# from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def plot(strings, compact):
    plotData = []
    for i in range(len(compact)):
        amountA = 0
        amountC = 0
        amountG = 0
        amountT = 0
        for string in strings:
            if string[i] == 'A':
                amountA += 1
            elif string[i] == 'C':
                amountC += 1
            elif string[i] == 'G':
                amountG += 1
            elif string[i] == 'T':
                amountT += 1
        total = amountA + amountC + amountG + amountT
        plotData.append([amountA/total, amountC/total, amountG/total, amountT/total])


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = [x[0] for x in plotData]
    y = [x[1] for x in plotData]
    z = [x[2] for x in plotData]
    c = [x[3] for x in plotData]

    ax.set_xlabel('A')
    ax.set_ylabel('C')
    ax.set_zlabel('G')
    # ax.set_clabel('T')

    img = ax.scatter(x, y, z, c=c, cmap=plt.hot())
    fig.colorbar(img)
    plt.show()
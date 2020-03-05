from sympy import *
import re
import math
import numpy as np

with open(r'C:\Users\qianp\Desktop\Realizable_Gauss_Paragraphs_1_1_3RIIreduction.txt')as f:
    data = f.readlines()
    data = data
origindata = []
for i in data:
    i = i[:-1]
    origindata.append(i)

pattern = re.compile("^h\d\Wv\d\W")
pattern2 = re.compile(".*v\d\W$")
pat = re.compile("\W")
newData = []
newDatapro = []

for i in origindata:
    if not re.match(pattern, i) and not re.match(pattern2, i):
        newData.append(i)
print(len(newData))

for line in newData:
    pattern = re.compile("[a-z]")
    patternnum = re.compile("[0-9]")
    patternsuperscript = re.compile("\W")
    symbols = re.findall(pattern, line)

    numbers = re.findall(patternnum, line)

    superscripts = re.findall(patternsuperscript, line)

    paragraph = [symbols, numbers, superscripts]
    newDatapro.append(paragraph)


def generateArcs(origindata):
    arcsdata = []
    k = 0
    for paragraph in origindata:
        k += 1

        symbols, numbers, superscripts = paragraph[0], paragraph[1], paragraph[2]
        arcs = dict()
        for j in range(0, len(symbols)):
            arc = []
            arcsymbol = []
            arcnumber = []
            arcscript = []
            if symbols[j] == "u":
                i = j
                flag = False
                while i <= len(symbols) and flag == False:
                    if i == len(symbols):
                        i = 0
                    arcsymbol.append(symbols[i])
                    arcnumber.append(numbers[i])
                    arcscript.append(superscripts[i])
                    if symbols[i] == "u" and not i == j and flag == False:
                        flag = True

                    i += 1
                arc = [arcsymbol, arcnumber, arcscript]

            if len(arc) > 1:
                key = numbers[j]
                arcs[key] = arc
        arcsdata.append(arcs)
    return arcsdata


def generateMatrix(arcsdata):
    x = Symbol("x")
    y = Symbol("y")
    t = Symbol("t")

    datamatrix = []
    for i in range(0, len(arcsdata)):
        matric = []
        for label in arcsdata[i].keys():
            row = [0] * len(arcsdata[i].items())
            target = "o" + label
            counter = 0
            for fragment in arcsdata[i].values():
                if "h" in fragment[0] or "v" in fragment[0]:
                    try:
                        hindex = fragment[0].index("h")
                    except:
                        hindex = math.inf

                    try:
                        vindex = fragment[0].index("v")
                    except:
                        vindex = math.inf

                    try:
                        targetindex = [index for index in range(0, len(fragment[1])) if
                                       fragment[0][index] + fragment[1][index] == target][0]
                    except:
                        targetindex = math.inf

                    ymult = y
                    xmult = x
                    if isinstance(hindex, int):
                        if not fragment[2][hindex] == "+":
                            ymult = y ** (-1)
                    if isinstance(vindex, int):
                        if not fragment[2][vindex] == "+":
                            xmult = x ** (-1)

                    if targetindex < hindex and targetindex < vindex:
                        row[counter] = 1
                    else:
                        if targetindex > hindex and targetindex > vindex:
                            row[counter] = 1 * xmult * ymult
                        elif hindex <= targetindex < vindex:
                            row[counter] = 1 * ymult
                        elif hindex > targetindex >= vindex:
                            row[counter] = 1 * xmult

                else:
                    if not target in fragment:
                        row[counter] = 0
                    else:
                        row[counter] = 1

                counter += 1
            matric.append(row)
        datamatrix.append(matric)
    return np.array(datamatrix) * (1 - t)


def generateArcMaxtrix(arcsdata, generatorlist):
    x = Symbol("x")
    y = Symbol("y")
    generatormatrix = []
    for i in range(0, len(arcsdata)):
        generator = []
        for label in arcsdata[i].keys():
            generatorrow = [0] * len(arcsdata[i].keys())
            crossing = label

            for fragment in arcsdata[i].values():
                columnindex = list(arcsdata[i].values()).index(fragment)

                try:
                    hindex = fragment[0].index("h")
                except:
                    hindex = math.inf

                try:
                    vindex = fragment[0].index("v")
                except:
                    vindex = math.inf

                ymulti = y
                xmulti = x
                if isinstance(hindex, int):
                    if fragment[-1][hindex] == "-":
                        ymulti = y ** (-1)
                if isinstance(vindex, int):
                    if fragment[-1][vindex] == "-":
                        xmulti = x ** (-1)

                if crossing in fragment[1]:
                    if crossing in fragment[1]:
                        if fragment[1][0] == crossing:
                            if fragment[-1][0] == "+":
                                generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[0]
                            else:
                                generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[-1]
                        else:
                            """
                            crossingindex=[cindex for cindex in range(0,len(fragment[1])) if fragment[1][cindex] == crossing]
                            for cindex in crossingindex:
                                if hindex > cindex and vindex > cindex:
                                    if fragment[0][cindex] == "o":
                                        generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[1]
                                    elif fragment[0][cindex] == "u":
                                        if fragment[-1][cindex] == "+":
                                            generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[-1]
                                        elif fragment[-1][cindex] == "-":
                                            generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[0]
                                elif hindex < cindex < vindex:
                                    if fragment[0][cindex] == "o":
                                        generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[1]*ymulti
                                    elif fragment[0][cindex] == "u":
                                        if fragment[-1][cindex] == "+":
                                            generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[-1]*ymulti
                                        elif fragment[-1][cindex] == "-":
                                            generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[0]*ymulti
                                    pass
                                elif vindex < cindex < hindex:
                                    if fragment[0][cindex] == "o":
                                        generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[1] * xmulti
                                    elif fragment[0][cindex] == "u":
                                        if fragment[-1][cindex] == "+":
                                            generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[-1] * xmulti
                                        elif fragment[-1][cindex] == "-":
                                            generatorrow[columnindex] = generatorrow[columnindex] + generatorlist[0] * xmulti

                            """
                            generatorrow[columnindex] = generatorrow[columnindex] + getDelta(fragment, crossing, hindex,
                                                                                             vindex, generatorlist,
                                                                                             xmulti, ymulti)

            generator.append(generatorrow)
        generatormatrix.append(generator)
    return np.array(generatormatrix)


def getDelta(fragment, crossing, hindex, vindex, generatorlist, xmulti, ymulti):
    crossingIndex = [cindex for cindex in range(0, len(fragment[1])) if
                     fragment[1][cindex] == crossing and not cindex == hindex and not cindex == vindex]
    deltaFinal = 0
    for cIndex in crossingIndex:
        delta = 1
        if fragment[0][cIndex] == "o":
            delta = delta * generatorlist[1]
        elif fragment[0][cIndex] == "u":
            if fragment[-1][cIndex] == "+":
                delta = delta * generatorlist[-1]
            elif fragment[-1][cIndex] == "-":
                delta = delta * generatorlist[0]

        if hindex < cIndex < vindex:
            delta = delta * ymulti
        elif vindex < cIndex < hindex:
            delta = delta * xmulti

        deltaFinal = deltaFinal + delta
    return deltaFinal


arcsdata = generateArcs([[["h", "u", "o", "v", "u", "u", "o", "o"], ["1", "1", "2", "1", "3", "2", "1", "3"],
                          ["+", "+", "+", "+", "+", "+", "+", "+"]]])
arcmatrix = generateMatrix(arcsdata)
generateMatrix = generateArcMaxtrix(arcsdata, [-1, 1 - Symbol("t"), Symbol("t")])
print(generateMatrix)

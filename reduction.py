import re

scripts=["+","-"]
with open(r'C:\Users\qianp\Downloads\Realizable_Gauss_Paragraphs_1_1_3.txt') as f:
    data=f.readlines()
    data=data[:-1]

fagpuls=False
fagminus=False
vafterhset=[]
hstartvendset=[]
vinmiddleset=[]
count=0
count2=0
count3=0
pat=re.compile("\W")
newData=[]


print("original dataset: ",len(data))



for line in data:#generate three lists of each paragraph
    pattern=re.compile("[a-z]")
    patternnum=re.compile("[0-9]")
    patternsuperscript=re.compile("\W")
    symbols=re.findall(pattern,line)
  #  print(symbols)
    numbers=re.findall(patternnum,line)
  #  print(numbers)
    superscripts=re.findall(patternsuperscript,line)
    superscripts.remove("\n")
  #  print(superscripts)
    paragraph=[symbols,numbers,superscripts]
    newData.append(paragraph)


def eliminate(paragraph):#eliminate the paragraph with oiui
    flag=False
    hindex = paragraph[0].index("h")
    vindex = paragraph[0].index("v")
    numlist = paragraph[1].copy()

    del numlist[hindex]
    del numlist[vindex-1]

    indexlistfor1 = [index for index in range(len(numlist)) if numlist[index] == "1"]
    indexlistfor2 = [index for index in range(len(numlist)) if numlist[index] == "2"]
    indexlistfor3=[index for index in range(len(numlist)) if numlist[index] == "3"]
    indexlistfor4 = [index for index in range(len(numlist)) if numlist[index] == "4"]

    if len(indexlistfor1) > 1 and len(indexlistfor2) > 1 and len(indexlistfor3)>1 :
        dis1 = abs(indexlistfor1[1] - indexlistfor1[0])
        dis2 = abs(indexlistfor2[1] - indexlistfor2[0])
        dis3=abs(indexlistfor3[1]-indexlistfor3[0])
      #  dis4=abs(indexlistfor4[1]-indexlistfor4[0])
        if dis1==1:
            flag=True
        elif dis2==1:
            flag=True
        elif dis3==1:
            flag=True
     #   elif dis4==1:
         #   flag=True



    return  flag



def checksamesame(paragraph1, paragraph2):#reduction based Pro Kurlin introduced
    """""
    removing all the index of hs and vs in the number list of both paragraphs
    """""
    flag = False
    hindex1=paragraph1[0].index("h")
    vindex1=paragraph2[0].index("v")
    hindex2=paragraph1[0].index("h")
    vindex2=paragraph2[0].index("v")

    numlist1 = paragraph1[1].copy()
    scriptlist1=paragraph1[2].copy()
    del numlist1[hindex1]
    del numlist1[vindex1-1]
    del scriptlist1[hindex1]
    del scriptlist1[vindex1-1]

    numlist2 = paragraph2[1].copy()
    scriptlist2=paragraph2[2].copy()
    del numlist2[hindex2]
    del numlist2[vindex2-1]
    del scriptlist2[hindex1]
    del scriptlist2[vindex1-1]
    originlength=len(numlist1)


    count=0
    """"
    check the equality of symbols of 2 paragraphs, if they are the same,then check the numlist
    by checking each pair of two elements with same index, if each one pair is matched, then count+1
    if the count is equal to half of the length of numlist.
    """
    """""
    if paragraph1[0] == paragraph2[0] and not paragraph1[1] == paragraph2[1]:#check whether symbols are equal
        if paragraph1[2][hindex1] == paragraph2[2][hindex2]:#check the superscripts of h
            if paragraph1[2][vindex1] == paragraph2[2][vindex2]:#check the superscript of v
                for i in range(len(numlist1)):
                    indexlist1for1 = [index for index in range(len(numlist1)) if numlist1[index] == numlist1[i]]
                    if len(numlist1) > 1:
                        # print(numlist1[i],numlist2[i])
                        if not numlist1[i] == numlist2[i]:
                            target=numlist2[i]
                            #print("before:",numlist1,numlist2)
                            for j in range(len(numlist2)):
                                if numlist2[j] == target:
                                    numlist2[i] = numlist1[i]
                                    scriptlist2[i] = scriptlist1[i]
                                    numlist2[j] = numlist1[i]
                                    scriptlist2[j] = scriptlist1[i]
                           # print("after:",numlist1,numlist2)
                            if numlist1[indexlist1for1[1]] == numlist2[indexlist1for1[1]]:
                                if scriptlist1[indexlist1for1[1]] == scriptlist2[indexlist1for1[1]]:#check the equality of superscript after switching
                                    count += 1
                        else:
                            count += 1
                    if count == len(numlist1) / 2:
                        flag = True
                        break
        """
    iternumber=1
    if paragraph1[2][hindex1] == paragraph2[2][hindex2] and paragraph1[2][vindex1] == paragraph1[2][vindex2]:
        if paragraph1[0] == paragraph2[0] and not paragraph1[1] == paragraph2[1]:
            if paragraph1[2][vindex1] == paragraph2[2][vindex2]:
                i = 0
                while len(numlist1) >= 1:
                    oldtarget = numlist2[i]
                    indexlist1for1 = [index for index in range(len(numlist1)) if numlist1[index] == numlist1[i]]
                    print(numlist1,numlist2)
                    if iternumber==originlength-1:
                        if not numlist1[i]==numlist2[i]:
                            flag=False
                            break

                    if not numlist1[i] == numlist2[i]:
                        numlist2[i] = numlist1[i]
                        for j in range(len(numlist2)):
                            if numlist2[j] == oldtarget:
                                    scriptlist2[i] = scriptlist1[i]
                                    numlist2[j] = numlist1[i]
                                    scriptlist2[j] = scriptlist1[i]
                        #  print(numlist1, numlist2)
                        counting = []
                        for n in range(len(indexlist1for1)):
                            # print(indexlist1for1[n])
                            # print(numlist1[indexlist1for1[n]], numlist2[indexlist1for1[n]])
                            if numlist1[indexlist1for1[n]] == numlist2[indexlist1for1[n]]:
                                if scriptlist2[indexlist1for1[n]] == scriptlist1[indexlist1for1[n]]:
                                    counting.append(indexlist1for1[n])
                        #        del numlist1[indexlist1for1[n]]
                        #    del numlist2[indexlist1for1[n]]
                        counter = 0
                        #  print(counting)
                        for k in counting:
                            #   print(k)
                            if counter == len(counting):
                                break
                            if counter > 0:
                                k = k - 1
                            del numlist1[k]
                            del numlist2[k]
                            counter += 1
                        iternumber+=1
                        print(numlist1,numlist2)

                    else:
                        del numlist1[i]
                        del numlist2[i]
                        iternumber+=1

                if len(numlist1) < 1:
                    flag = True

    return flag
    """""
    if paragraph1[0] == paragraph2[0] and not paragraph1[1] == paragraph2[1]:  # check whether symbols are equal
            if paragraph1[2][hindex1] == paragraph2[2][hindex2]:  # check the superscripts of h
                if paragraph1[2][vindex1] == paragraph2[2][vindex2]:  # check the superscript of v
                    for i in range(len(numlist1)):
                        turnedflag=False
                        oldtarget=numlist2[i]
                        indexlist1for1 = [index for index in range(len(numlist1)) if numlist1[index] == numlist1[i]]
                        scriptlist1forpuls = [index for index in range(len(scriptlist1)) if scriptlist1[index] == "+"]
                        scriptlist2forpuls=[index for index in range(len(scriptlist2)) if scriptlist2[index] == "+"]
                        if len(numlist1) > 1:
                            if len(scriptlist1forpuls)==len(scriptlist2forpuls):
                                if not numlist1[i] == numlist2[i]:
                                    for j in range(i+1,len(numlist2)):
                                        if numlist2[j] == oldtarget:
                                            if turnedflag==False:
                                                numlist2[i] = numlist1[i]
                                                scriptlist2[i] = scriptlist1[i]
                                                numlist2[j] = numlist1[i]
                                                scriptlist2[j] = scriptlist1[i]
                                                turnedflag = True
                                            if numlist1[indexlist1for1[1]] == numlist2[indexlist1for1[1]]:
                                                    if scriptlist1[indexlist1for1[1]] == scriptlist2[indexlist1for1[1]]:  # check the equality of superscript after switching
                                                        count += 1
                                else:
                                    if not numlist1[indexlist1for1[1]]==numlist2[indexlist1for1[1]]:
                                        flag=False
                                        break
                                    else:
                                        if scriptlist1[i] == scriptlist2[i]:
                                            count += 1

                        if count == len(numlist1) / 2:
                            flag = True
                            break


    return flag
"""
#checksamesame([["h","v","o","u","o","u"],["1","1","1","1","2","2"],["+","+","+","-","+","+"]],[["h","v","o","u","o","u"],["1","1","1","2","2","1"],["+","+","+","+","+","+"]])


def r2reduction(paragraph):
    flag = False
    indexlistforo = [index for index in range(len(paragraph[0])) if paragraph[0][index] == "o"]
    #print(indexlistforo)
    indexlistforu = [index for index in range(len(paragraph[0])) if paragraph[0][index] == "u"]
   # print(indexlistforu)

    for j in range(len(indexlistforo)):
        if j + 1 < len(indexlistforo):
            if abs(indexlistforo[j + 1] - indexlistforo[j]) == abs(indexlistforu[j + 1] - indexlistforu[j]) == 1:
              #  print("True")
                if not (paragraph[2][indexlistforo[j]] == paragraph[2][indexlistforo[j + 1]]):
                    if not paragraph[2][indexlistforu[j]] == paragraph[2][indexlistforu[j + 1]]:
                        flag = True
                        break
   # print()
    return flag

def eliminate2(paragraph):  # eliminate the paragraph with oiui
    flag = False
    hindex = paragraph[0].index("h")
    vindex = paragraph[0].index("v")
    numlist = paragraph[1].copy()

    del numlist[hindex]
    del numlist[vindex - 1]

    indexlistfor3 = [index for index in range(len(numlist)) if numlist[index] == "3"]
    # indexlistfor2 = [index for index in range(len(numlist)) if numlist[index] == "2"]

    if len(indexlistfor3) > 1:
        dis3 = abs(indexlistfor3[1] - indexlistfor3[0])
        if dis3 == 1:
            flag = True
    return flag

def RIreduction(result):
    needtoremove=[]
    for i in range(len(result)):
        if eliminate(result[i]):
            needtoremove.append(i)

    newresult=[]
    for j in range(len(result)):
        if j not in needtoremove:
            newresult.append(result[j])
    return newresult

def RIIreduction(result):
    needtoremove=[]
    for i in range(len(result)):
        if r2reduction(result[i]):
            needtoremove.append(i)

    newresult=[]
    for j in range(len(result)):
        if j not in needtoremove:
            newresult.append(result[j])
    return newresult

RIreductionresult=RIreduction(newData)
RIIreductionresult=RIIreduction(RIreductionresult)

print(len(RIIreductionresult))

i=0
result=[]
needtoremove=[]
for i in range(len(RIIreductionresult)):
   # print("checking equality of paragraph "+data[i]+" no.",i)
    for j in range(i+1,len(RIIreductionresult)):
        if j<len(RIIreductionresult) :
                    if checksamesame(RIIreductionresult[i], RIIreductionresult[j]):
                        if RIIreductionresult[i] == [["h", "v", "o", "u", "o", "u", "o", "u"], ["1", "1", "1", "2", "3", "1", "2", "3"],
                                  ["+", "+", "+", "+", "+", "+", "+", "+"]]:
                            print("here it is")
                            print(RIIreductionresult[j])
                        if RIIreductionresult[i][1]<RIIreductionresult[i][1]:
                            needtoremove.append(i)
                        else:
                            needtoremove.append(j)


for i in range(len(RIIreductionresult)):
    if i not in needtoremove:
        result.append(RIIreductionresult[i])

for i in result:
    string = ""
    for j in range(len(i[0])):
        symbol = i[0][j] + i[1][j] + i[2][j]
        string = string + symbol
    print(string)
print(len(result))

""""
RI reduction
"""
""""
for i in result:
    string = ""
    for j in range(len(i[0])):
        symbol = i[0][j] + i[1][j] + i[2][j]
        string = string + symbol
    print(string)
print(len(result))
"""


#with open(r'C:\Users\qianp\Desktop\Realizable_Gauss_Paragraphs_1_1_3.txt',"w")as f:
 #   for i in result:
  #      string=""
   #     for j in range(len(i[0])):
    #        symbol = i[0][j] + i[1][j] + i[2][j]
     #       string = string + symbol
      #  string=string+"\n"
       # f.writelines(string)

with open(r'C:\Users\qianp\Desktop\Realizable_Gauss_Paragraphs_1_1_3RIIreduction.txt',"w")as f:
    for i in result:
        string=""
        for j in range(len(i[0])):
            symbol = i[0][j] + i[1][j] + i[2][j]
            string = string + symbol
        string=string+"\n"
        f.writelines(string)

#print(len(newresult),len(result))
#print([[1,1,1],[2,2,2]]==[[1,1,1],[2,2,2]])
#print([["h","u","o","v","o","u"],["1","1","2","1","1","2"],["+","-","-","-","-","-"]] in result)
print(checksamesame([["h","v","o","u","o","u","o","u"],["1","1","1","3","2","1","3","2"],["+","+","+","+","+","+","+","+"]],[["h","v","o","u","o","u","o","u"],["1","1","1","2","3","1","2","3"],["+","+","+","+","+","+","+","+"]]))
print([["h","v","o","u","o","u","o","u"],["1","1","1","3","2","1","3","2"],["+","+","+","+","+","+","+","+"]]in result,[["h","v","o","u","o","u","o","u"],["1","1","1","2","3","1","2","3"],["+","+","+","+","+","+","+","+"]]in result)
#checksamesame([["h","v","o","u","o","u"],["1","1","1","1","2","2"],["+","+","+","+","+","+"]],[["h","v","o","u","u","o"],["1","1","2","2","1","1"],["+","+","+","+","+","+"]])










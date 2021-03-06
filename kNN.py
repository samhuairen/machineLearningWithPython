#!/usr/bin/python
#coding:utf-8
from numpy import *
import operator

def createDateSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=["A","A","B","B"]
    return group,labels

def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDisstances=sqDiffMat.sum(axis=1)
    distances=sqDisstances**0.5
    sortedDistIndicies=distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    sortedClassCount=sorted(classCount.iteritems(),
        key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
# group=createDateSet()[0]
# labels=createDateSet()[1]
# inX=[1.2,1.2]
# print classify0(inX,group,labels,3)
def file2matrix(filename):
    fr=open(filename)
    arrayOfLines=fr.readlines()
    numberOfLines=len(arrayOfLines)
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    for line in arrayOfLines:
        line=line.strip()
        listFromLine=line.split("\t")
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector
def autoNorm(dataSet):
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    #normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minVals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals
def datingClassTest():
    hoRatio=0.10
    datingDataMat,datingDataLabels=file2matrix("datingTestSet2.txt")
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0
    for i in range(numTestVecs):
        classifierResults=classify0(normMat[i,:],normMat[numTestVecs:m,],datingDataLabels[numTestVecs:m],3)
        print "the classfier came back with: %d, the real answer is : %d" % (classifierResults,datingDataLabels[i])
        if (classifierResults!=datingDataLabels[i]):
            errorCount+=1.0
    print "the total error rate is :%f" % (errorCount/float(numTestVecs))
def classifyPerson():
    resultsList=["not at all","in small dose","in larger dose"]
    percentTats=float(raw_input("percentage time spent playing video games?"))
    ffMiles=float(raw_input("frequent filer miles earned per year?"))
    iceCream=float(raw_input("liters of icecream consummed per year?"))
    datingDataMat,datingDataLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResults=classify0((inArr-minVals)/ranges,normMat,datingDataLabels,3)
    print "you probably like this person ", resultsList[classifierResults-1] 













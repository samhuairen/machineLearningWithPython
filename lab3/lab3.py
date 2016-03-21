#!/usr/bin/python
#coding:utf-8
from numpy import *
from os import listdir
def img2Vector(filename):
    returnVector=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            returnVector[0,32*i+j]=int(lineStr[j])
    return returnVector

def handwritingClassTest():
    hwLabels=[]
    trainingFileList=listdir('trainingDigits')
    m=len(trainingFileList)
    traingMat=zeros((m,1024))
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split(".")[0]
        classNumStr=int(fileStr.split("_")[0])
        hwLabels.append(classNumStr)
        traingMat[i,:]=img2Vector('trainingDigits/%s' % fileNameStr)
    testFileList=listdir('testDigits')
    errorCount=0.0
    mTest=len(testFileList)
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split(".")[0]
        classNumStr=int(fileStr.split("_")[0])
        vectUnderTest=img2Vector("testDigits/%s" % fileNameStr)
        classifierResults=classify0(vectUnderTest,traingMat,hwLabels,3)
        print "the classifier came back with:%d,the real answer is : %d" %(classifierResults,classNumStr)
        if (classifierResults!=classNumStr): errorCount+=1.0
    print "\n the total number of errors is : %d" % errorCount
    print "\n the total error rate is : %f " % (errorCount/float(mTest))

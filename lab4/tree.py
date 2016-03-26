#!/usr/bin/python
from math import log
import operator

def calcShannonEnt(dataSet):
    """calculte shannon entropy for a give dataset"""
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1 # get the count of each label
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries
        shannonEnt -=prob*log(prob,2)       # return all kinds of entropy
    return shannonEnt
def createDataSet():
    dataSet=[[1,1,'yes'],
    [1,1,'yes'],
    [1,0,'no'],
    [0,1,'no'],
    [0,1,'no'],
    ]
    labels=['no surfacing','flippers']
    return dataSet,labels

def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVect=featVec[:axis]
            reducedFeatVect.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVect)
    return retDataSet
def  chooseBestFeatureToSplit(dataSet):
    numFeatures=len(dataSet[0])-1
    baseEntropy=calcShannonEnt(dataSet)
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numFeatures):
        featList=[example[i] for example in dataSet]
        uniqueVals=set(featList)
        newEntropy=0.0
        for value in uniqueVals:                                #split dataSet with characters, but we must input unique value,
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))   # calculte the propotion of each split dataset
            newEntropy+=prob*calcShannonEnt(subDataSet) # get the split dataset entropy 
        infoGain=baseEntropy - newEntropy   # get infoGain from baseEntropy and the entropy calculted after split 
        if (infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

def majorityCount(classList):   #python for order a dict where it reserves the data for frequencies,like function "table" in R and sort the table
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote] +=1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet ]
    if classList.count(classList[0])==len(classList): # if the labels are all the same, stop split
        return classList[0]
    if len(dataSet[0])==1:                                       # if all the features are used and the data set still can not 
    #devided the only one group which contain the same feature, choose the majority class
        return majorityCount(classList)
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLables=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLables) # use recursion 
    return myTree

def loadData(filepath):
    fr=open(filepath,'r')
    lense=[item.strip().split('\t') for item in fr.readlines()]
    labels=['age', 'prescript', 'astigmatic', 'tearRate']
    return lense,labels

from numpy import*

def loadSipData():
	dataMat=matrix([[1.,2.1],[2.,1.1],[1.3,1.],[1.,1.],[2.,1.]])
	classLabels=[1.0,1.0,-1.0,-1.0,1.0]
	
	return dataMat,classLabels

def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
	retArray=ones((shape(dataMatrix)[0],1))
	if threshIneq=='lt':retArray[dataMatrix[:,dimen]<=threshVal]=-1.0
	else:
		retArray[dataMatrix[:,dimen]>threshVal]=-1.0
	return retArray

def buildStump(dataArr,classLabels,D):
	dataMatrix=mat(dataArr);labelMat=mat(classLabels).T
	m,n=shape(dataMatrix)
	numSteps=10.0;bestStump={};bestClasEst=mat(zeros((m,1)))
	minError=inf
	for i in range(n):
		rangeMin=dataMatrix[:,i].min();rangeMax=dataMatrix[:,i].max();
		stepSize=(rangeMax-rangeMin)/numSteps
		for j in range(-1,int(numSteps)+1):
			for inequal in ['lt','gt']:
				threshVal=(rangeMin+float(j)*stepSize)
				predictedicVals=stumpClassify(dataMatrix,i,threshVal,inequal)
				errArr=mat(ones((m,1)))
				errArr[predictedicVals==labelMat]=0
				weightedError=D.T*errArr
				print "split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshVal, inequal, weightedError)
				if weightedError < minError:
					minError = weightedError
					bestClasEst = predictedicVals.copy()
					bestStump['dim'] = i
					bestStump['thresh'] = threshVal
					bestStump['ineq'] = inequal
	return bestStump,minError,bestClasEst


def adaBoostTrainDs(dataArr,classLabels,numIt=40):
	weakClassArr=[]
	m=shape(dataArr)[0]
	D=mat(ones((m,1))/m)
	aggClassEst=mat(zeros((m,1)))
	for i in range(numIt):
		bestStump,error,classEst=buildStump(dataArr, classLabels, D)
		print"D:",D.T
		alpha=float(0.5*log((1.0-error)/max(error,1e-16)))
		bestStump['alpha']=alpha
		weakClassArr.append(bestStump)
		print("classEst:",classEst.T)
		expon=multiply(-1*alpha*mat(classLabels).T,classEst)
		D=multiply(D,exp(expon))
		D=D/D.sum()
		aggClassEst+=alpha*classEst
		print("aggClassEst",aggClassEst.T)
		aggErrors=multiply(sign(aggClassEst)!=mat(classLabels).T,ones((m,1)))
		errorRate=aggErrors.sum()/m
		print("total error:",errorRate,"\n")
		if errorRate==0.0:break
	return weakClassArr


def adaClassify(datToClass,classifierArr):
	dataMatrix=mat(datToClass)
	m=shape(dataMatrix)[0]
	aggClassEst=mat(zeros((m,1)))
	for i in range(len(classifierArr)):
		classEst=stumpClassify(dataMatrix,classifierArr[i]['dim'],classifierArr[i]['thresh'],classifierArr[i]['ineq'])
		aggClassEst+=classifierArr[i]['alpha']*classEst
		print aggClassEst
	return sign(aggClassEst)



def loadDataSet(fileName):
	numFeat = len(open(fileName).readline().split('\t'))
	dataMat = []; labelMat = []
	fr = open(fileName)
	for line in fr.readlines():
		lineArr=[]
		curLine = line.strip().split('\t')
		for i in range(numFeat-1):
			lineArr.append(float(curLine[i]))
		dataMat.append(lineArr)
		labelMat.append(float(curLine[-1]))
	return dataMat,labelMat


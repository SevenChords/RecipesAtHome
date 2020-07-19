from logger import log

def getInsertionIndex(legalMoves, stepIndex, frames):
	tempIndex = 0
	while(tempIndex < len(legalMoves[stepIndex]) and legalMoves[stepIndex][tempIndex][2] < frames):
		tempIndex += 1
	#log(7, "Moves", "Index", "", "Index found: " + str(tempIndex) + ".")
	return tempIndex
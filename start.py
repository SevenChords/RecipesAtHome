import multiprocessing
from ctypes import c_int
from calculator import calculateOrder
from inventory import getStartingInventory, getInventoryFrames
from recipes import getRecipeList
from config import getConfig
from logger import log

def worker(doneQueue, *args):
	for result in calculateOrder(*args):
		#write the calculated result to the "done" queue
		doneQueue.put(result, False)

def work(frameRecord, startingInventory, recipeList, invFrames):
	#create queue for results to be pushed to
	doneQueue = multiprocessing.Queue(workerCount)
	#start workers
	for i in range(workerCount):
		instance = multiprocessing.Process(
			target=worker, args=(doneQueue, i, frameRecord, startingInventory,
								 recipeList, invFrames))
		instance.daemon = True
		instance.start()
	#wait for each result from the workers
	while True:
		yield doneQueue.get(True)

if __name__ == '__main__':
	frameRecord = multiprocessing.Value(c_int)
	frameRecord.value = 9999
	cycle_count = 1
	startingInventory = getStartingInventory()
	recipeList = getRecipeList()
	invFrames = getInventoryFrames()
	workerCount = int(getConfig("workerCount"))
	#start the work
	for result in work(frameRecord, startingInventory, recipeList,
					   invFrames):
		log(1, "Main", "Results", "",
			'cycle {0} done, current record: {1} frames. Record on call {2}.'
			.format(cycle_count, frameRecord.value, result[1]))
		cycle_count += 1

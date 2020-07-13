import multiprocessing
from calculator import calculateOrder
from inventory import getStartingInventory, getInventoryFrames
from recipes import getRecipeList
from config import getConfig
from logger import log

def worker(workQueue, doneQueue):
	while(True):
		job = workQueue.get(True)
		#waiting for a job to appear
		#in this case job refers to a single instance of calculating the recipe order
		result =  calculateOrder(job[0], job[1], job[2], job[3], job[4])
		#write the calculated result to the "done" queue
		doneQueue.put(result, False)

def work(currentFrameRecord, startingInventory, recipeList, invFrames):
	#create queues
	doneQueue = multiprocessing.Queue(workerCount)
	workQueue = multiprocessing.Queue(workerCount)
	#create array for all the instances that are running
	instances = []
	#start instances
	for i in range(workerCount):
		instance = multiprocessing.Process(target=worker, args=(workQueue, doneQueue))
		instance.daemon = True
		instance.start()
		instances.append(instance)
	#start jobs
	for i in range (workerCount):
		job = [i, currentFrameRecord, startingInventory, recipeList, invFrames]
		workQueue.put(job, False)
	#waiting for first result
	result = doneQueue.get(True)
	#terminate the other instances still running
	for instance in instances:
		instance.terminate()
	return result

if __name__ == '__main__':
	currentFrameRecord = 9999
	cycle_count = 1
	startingInventory = getStartingInventory()
	recipeList = getRecipeList()
	invFrames = getInventoryFrames()
	workerCount = int(getConfig("workerCount"))
	while(True):
		#start the work
		result = work(currentFrameRecord, startingInventory, recipeList, invFrames)
		#sanity check
		if(result[0] < currentFrameRecord):
			currentFrameRecord = result[0]
			log(1, "Main", "Results", "", 'cycle {0} done, current record: {1} frames. Record on call {2}.'.format(cycle_count, currentFrameRecord, result[1]))
		cycle_count += 1

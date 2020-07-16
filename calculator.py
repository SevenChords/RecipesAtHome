import copy
import random
from logger import log
from inventory import getAlphaSort, getTypeSort, remainingOutputsCanBeFulfilled
from moves import getInsertionIndex
from config import getConfig

def printResults(filename, writtenStep, framesTaken, totalFrames, inventory, outputCreated, itemNames, stepIndex):
	#Print the results of all states observed in the current stack
	file = open(filename, "w")
	#Write Header information
	file.write("Description\tFrames Taken\tTotal Frames")
	for z in range(20):
		file.write("\tSlot #{0}".format(z+1))
	for z in range(58):
		file.write("\t{0}".format(itemNames[z]))
	file.write("\n")
	log(5, "Calculator", "File", "Write", "Header for " + filename + " written.")
	#Print data information
	for i in range(0, stepIndex + 1):
		file.write("{0}\t{1}\t{2}".format(writtenStep[i],framesTaken[i],totalFrames[i]))
		for z in range(0,20):
			file.write("\t{0}".format(inventory[i][z]))
		for z in range(0,58):
			file.write("\t{0}".format(outputCreated[i][z]))
		file.write("\n")
		log(5, "Calculator", "File", "Write", "Data for Step " + str(writtenStep[i]) + " written.")
	file.close()

#Return the Alphabetic sorted version of the inventory
def sortAlpha(inventory):
	full_alpha_list = getAlphaSort()
	alpha_inventory = []

	for i in range(0,len(full_alpha_list)):
		for j in range(0,inventory.count(full_alpha_list[i])):
			alpha_inventory.append(full_alpha_list[i])

	#Remaining Spaces are "Blocked"
	while(len(alpha_inventory) < 20):
		alpha_inventory.append("BLOCKED")

	return alpha_inventory

#Return the Reverse-Alphabetic sorted version of the inventory
def sortReverseAlpha(inventory):
	full_alpha_list = getAlphaSort()
	reverse_alpha_inventory = []

	for i in range(len(full_alpha_list)-1,-1,-1):
		for j in range(0,inventory.count(full_alpha_list[i])):
			reverse_alpha_inventory.append(full_alpha_list[i])

	#Remaining Spaces are "Blocked"
	while(len(reverse_alpha_inventory) < 20):
		reverse_alpha_inventory.append("BLOCKED")

	return reverse_alpha_inventory

#Return the Type sorted version of the inventory
def sortType(inventory):
	full_type_list = getTypeSort()
	type_inventory = []

	for i in range(0,len(full_type_list)):
		for j in range(0,inventory.count(full_type_list[i])):
			type_inventory.append(full_type_list[i])

	#Remaining Spaces are "Blocked"
	while(len(type_inventory) < 20):
		type_inventory.append("BLOCKED")

	return type_inventory

#Return the Reverse-Type sorted version of the inventory
def sortReverseType(inventory):
	full_type_list = getTypeSort()
	reverse_type_inventory = []

	for i in range(len(full_type_list)-1,-1,-1):
		for j in range(0,inventory.count(full_type_list[i])):
			reverse_type_inventory.append(full_type_list[i])

	#Remaining Spaces are "Blocked"
	while(len(reverse_type_inventory) < 20):
		reverse_type_inventory.append("BLOCKED")

	return reverse_type_inventory

#Evaluates all possible placements of the Keel Mango and Courage Shell
#And all possible locations and types of sorting that can place the Coconut into a position where it can be duplicated
def HandleChapter5Eval(legal_moves, step_index, temp_inventory, tempOutputsFulfilled, recipeList, itemNames, invFrames, temp_frames_DB, temp_frames_CO):
	#Various Frame Counts
	TOSS_FRAMES = 23
	ALPHA_SORT_FRAMES = 38
	REVERSE_ALPHA_SORT_FRAMES = 40
	TYPE_SORT_FRAMES = 39
	REVERSE_TYPE_SORT_FRAMES = 41

	#For descriptive purposes later
	DB_place_index = temp_inventory.index("Dried Bouquet")
	CO_place_index = temp_inventory.index("Coconut")

	#======================================
	#Evaluate sorting before the Keel Mango
	#======================================

	#Alphabetically Sorted Inventory
	alpha_inventory = sortAlpha(temp_inventory)

	#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
	#Because the coconut is needed for duplication
	if(alpha_inventory.index("Coconut") >= 10):
		#Place the Keel Mango and Courage Shell
		for KM_place_index in range(0,10):
			for CS_place_index in range(0,10):
				#Check that the KM and CS don't replace DB or CO
				if(alpha_inventory[KM_place_index] != "Dried Bouquet" and
				   alpha_inventory[CS_place_index] != "Dried Bouquet" and
				   alpha_inventory[KM_place_index] != "Coconut" and
				   alpha_inventory[CS_place_index] != "Coconut" and
				   KM_place_index != CS_place_index):
					#Replace the items, remember what they were
					KM_replacement = alpha_inventory[KM_place_index]
					CS_replacement = alpha_inventory[CS_place_index]

					alpha_inventory[KM_place_index] = "Keel Mango"
					alpha_inventory[CS_place_index] = "Courage Shell"

					#Verify that this new inventory is at least capable of satisfying the remaining recipes
					if(remainingOutputsCanBeFulfilled(alpha_inventory, tempOutputsFulfilled, recipeList, itemNames)):
						#Calculate the overall frame count
						temp_frames_KM = TOSS_FRAMES + invFrames[20-alpha_inventory.count("BLOCKED")][KM_place_index]
						temp_frames_CS = TOSS_FRAMES + invFrames[20-alpha_inventory.count("BLOCKED")][CS_place_index]
						temp_frame_sum = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS + ALPHA_SORT_FRAMES

						#Get the index on where to insert this legal move to
						insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

						#Describe how the break should play out
						ch5description = "Ch.5 Break: DB in slot {0}, CO in slot {1}, Sort (Alpha), KM in slot {2}, CS in slot {3}".format(DB_place_index+1,
																																		   CO_place_index+1,
																																		   KM_place_index+1,
																																		   CS_place_index+1)
						#Append the Legal Move
						legal_moves[step_index].insert(insertIndex,[ch5description,58,temp_frame_sum,copy.copy(alpha_inventory)])

					#Return the replaced items for the next loop
					alpha_inventory[KM_place_index] = KM_replacement
					alpha_inventory[CS_place_index] = CS_replacement

	#Reverse Alphabetical Sorted Inventory
	reverse_alpha_inventory = sortReverseAlpha(temp_inventory)

	#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
	#Because the coconut is needed for duplication
	if(reverse_alpha_inventory.index("Coconut") >= 10):
		#Place the Keel Mango and Courage Shell
		for KM_place_index in range(0,10):
			for CS_place_index in range(0,10):
				#Check that the KM and CS don't replace DB or CO
				if(reverse_alpha_inventory[KM_place_index] != "Dried Bouquet" and
				   reverse_alpha_inventory[CS_place_index] != "Dried Bouquet" and
				   reverse_alpha_inventory[KM_place_index] != "Coconut" and
				   reverse_alpha_inventory[CS_place_index] != "Coconut" and
				   KM_place_index != CS_place_index):
					#Replace the items, remember what they were
					KM_replacement = reverse_alpha_inventory[KM_place_index]
					CS_replacement = reverse_alpha_inventory[CS_place_index]

					reverse_alpha_inventory[KM_place_index] = "Keel Mango"
					reverse_alpha_inventory[CS_place_index] = "Courage Shell"

					#Verify that this new inventory is at least capable of satisfying the remaining recipes
					if(remainingOutputsCanBeFulfilled(reverse_alpha_inventory, tempOutputsFulfilled, recipeList, itemNames)):
						#Calculate the overall frame count
						temp_frames_KM = TOSS_FRAMES + invFrames[20-reverse_alpha_inventory.count("BLOCKED")][KM_place_index]
						temp_frames_CS = TOSS_FRAMES + invFrames[20-reverse_alpha_inventory.count("BLOCKED")][CS_place_index]
						temp_frame_sum = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS + REVERSE_ALPHA_SORT_FRAMES

						#Get the index on where to insert this legal move to
						insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

						#Describe how the break should play out
						ch5description = "Ch.5 Break: DB in slot {0}, CO in slot {1}, Sort (Reverse-Alpha), KM in slot {2}, CS in slot {3}".format(DB_place_index+1,
																																		   		   CO_place_index+1,
																																		   		   KM_place_index+1,
																																		   		   CS_place_index+1)
						#Append the Legal Move
						legal_moves[step_index].insert(insertIndex,[ch5description,58,temp_frame_sum,copy.copy(reverse_alpha_inventory)])

					#Return the replaced items for the next loop
					reverse_alpha_inventory[KM_place_index] = KM_replacement
					reverse_alpha_inventory[CS_place_index] = CS_replacement

	#Type Sorted Inventory
	type_inventory = sortType(temp_inventory)

	#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
	#Because the coconut is needed for duplication
	if(type_inventory.index("Coconut") >= 10):
		#Place the Keel Mango and Courage Shell
		for KM_place_index in range(0,10):
			for CS_place_index in range(0,10):
				#Check that the KM and CS don't replace DB or CO
				if(type_inventory[KM_place_index] != "Dried Bouquet" and
				   type_inventory[CS_place_index] != "Dried Bouquet" and
				   type_inventory[KM_place_index] != "Coconut" and
				   type_inventory[CS_place_index] != "Coconut" and
				   KM_place_index != CS_place_index):
					#Replace the items, remember what they were
					KM_replacement = type_inventory[KM_place_index]
					CS_replacement = type_inventory[CS_place_index]

					type_inventory[KM_place_index] = "Keel Mango"
					type_inventory[CS_place_index] = "Courage Shell"

					#Verify that this new inventory is at least capable of satisfying the remaining recipes
					if(remainingOutputsCanBeFulfilled(type_inventory, tempOutputsFulfilled, recipeList, itemNames)):
						#Calculate the overall frame count
						temp_frames_KM = TOSS_FRAMES + invFrames[20-type_inventory.count("BLOCKED")][KM_place_index]
						temp_frames_CS = TOSS_FRAMES + invFrames[20-type_inventory.count("BLOCKED")][CS_place_index]
						temp_frame_sum = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS + TYPE_SORT_FRAMES

						#Get the index on where to insert this legal move to
						insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

						#Describe how the break should play out
						ch5description = "Ch.5 Break: DB in slot {0}, CO in slot {1}, Sort (Type), KM in slot {2}, CS in slot {3}".format(DB_place_index+1,
																																		  CO_place_index+1,
																																		  KM_place_index+1,
																																		  CS_place_index+1)
						#Append the Legal Move
						legal_moves[step_index].insert(insertIndex,[ch5description,58,temp_frame_sum,copy.copy(type_inventory)])

					#Return the replaced items for the next loop
					type_inventory[KM_place_index] = KM_replacement
					type_inventory[CS_place_index] = CS_replacement

	#Reverse Type Sorted Inventory
	reverse_type_inventory = sortReverseType(temp_inventory)

	#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
	#Because the coconut is needed for duplication
	if(reverse_type_inventory.index("Coconut") >= 10):
		#Place the Keel Mango and Courage Shell
		for KM_place_index in range(0,10):
			for CS_place_index in range(0,10):
				#Check that the KM and CS don't replace DB or CO
				if(reverse_type_inventory[KM_place_index] != "Dried Bouquet" and
				   reverse_type_inventory[CS_place_index] != "Dried Bouquet" and
				   reverse_type_inventory[KM_place_index] != "Coconut" and
				   reverse_type_inventory[CS_place_index] != "Coconut" and
				   KM_place_index != CS_place_index):
					#Replace the items, remember what they were
					KM_replacement = reverse_type_inventory[KM_place_index]
					CS_replacement = reverse_type_inventory[CS_place_index]

					reverse_type_inventory[KM_place_index] = "Keel Mango"
					reverse_type_inventory[CS_place_index] = "Courage Shell"

					#Verify that this new inventory is at least capable of satisfying the remaining recipes
					if(remainingOutputsCanBeFulfilled(type_inventory, tempOutputsFulfilled, recipeList, itemNames)):
						#Calculate the overall frame count
						temp_frames_KM = TOSS_FRAMES + invFrames[20-reverse_type_inventory.count("BLOCKED")][KM_place_index]
						temp_frames_CS = TOSS_FRAMES + invFrames[20-reverse_type_inventory.count("BLOCKED")][CS_place_index]
						temp_frame_sum = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS + REVERSE_TYPE_SORT_FRAMES

						#Get the index on where to insert this legal move to
						insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

						#Describe how the break should play out
						ch5description = "Ch.5 Break: DB in slot {0}, CO in slot {1}, Sort (Reverse-Type), KM in slot {2}, CS in slot {3}".format(DB_place_index+1,
																																		  		  CO_place_index+1,
																																		  		  KM_place_index+1,
																																		  		  CS_place_index+1)
						#Append the Legal Move
						legal_moves[step_index].insert(insertIndex,[ch5description,58,temp_frame_sum,copy.copy(reverse_type_inventory)])

					#Return the replaced items for the next loop
					reverse_type_inventory[KM_place_index] = KM_replacement
					reverse_type_inventory[CS_place_index] = CS_replacement

	#=====================================
	#Evaluate sorting after the Keel Mango
	#=====================================

	#Default Keel Mango Placement Bounds
	KM_lower_bound = 0
	KM_upper_bound = 10

	#Restrict the bounds if there is still a "NULL" in the inventory
	#Because the Keel Mango can only go into the first available NULL spot
	if("NULL" in temp_inventory):
		KM_lower_bound = temp_inventory.index("NULL")
		KM_upper_bound = KM_lower_bound + 1

	#Place the Keel Mango
	for KM_place_index in range(KM_lower_bound,KM_upper_bound):

		#Replace the Keel Mango, remember what they were
		KM_replacement = temp_inventory[KM_place_index]

		#Calculate the needed frames
		if(KM_upper_bound - KM_lower_bound > 1):
			temp_frames_KM = TOSS_FRAMES + invFrames[20-temp_inventory.count("BLOCKED")][KM_place_index]
		else:
			temp_frames_KM = 0

		#Perform all sorts
		#Alphabetically Sorted Inventory
		alpha_inventory = sortAlpha(temp_inventory)

		#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
		#Because the coconut is needed for duplication
		if(alpha_inventory.index("Coconut") >= 10):
			#Place the Courage Shell
			for CS_place_index in range(0,10):
				#Check that the Courage Shell doesn't replace DB, CO, or KM
				if(alpha_inventory[CS_place_index] != "Dried Bouquet" and
				   alpha_inventory[CS_place_index] != "Coconut" and
				   alpha_inventory[CS_place_index] != "Keel Mango"):
					#Replace the item, remember what it was
					CS_replacement = alpha_inventory[CS_place_index]
					alpha_inventory[CS_place_index] = "Courage Shell"

					#Verify that this new inventory is at least capable of satisfying the remaining recipes
					if(remainingOutputsCanBeFulfilled(type_inventory, tempOutputsFulfilled, recipeList, itemNames)):
						#Calculate the overall frame count
						temp_frames_CS = TOSS_FRAMES + invFrames[20-alpha_inventory.count("BLOCKED")][CS_place_index]
						temp_frame_sum = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS + ALPHA_SORT_FRAMES

						#Get the index on where to insert this legal move to
						insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

						#Describe how the break should play out
						ch5description = "Ch.5 Break: DB in slot {0}, CO in slot {1}, KM in slot {2}, Sort (Alpha), CS in slot {3}".format(DB_place_index+1,
																																		   CO_place_index+1,
																																		   KM_place_index+1,
																																		   CS_place_index+1)
						#Append the Legal Move
						legal_moves[step_index].insert(insertIndex,[ch5description,58,temp_frame_sum,copy.copy(alpha_inventory)])

					#Return the replaced items for the next loop
					alpha_inventory[CS_place_index] = CS_replacement

		#Reverse Alphabetical Sorted Inventory
		reverse_alpha_inventory = sortReverseAlpha(temp_inventory)

		#Only bother further evaluation if the sort placed the Coconut in the latter half of the inventory
		#Because the coconut is needed for duplication
		if(reverse_alpha_inventory.index("Coconut") >= 10):
			#Place the Courage Shell
			for CS_place_index in range(0,10):
				#Check that the Courage Shell doesn't replace DB, CO, or KM
				if(reverse_alpha_inventory[CS_place_index] != "Dried Bouquet" and
				   reverse_alpha_inventory[CS_place_index] != "Coconut" and
				   reverse_alpha_inventory[CS_place_index] != "Keel Mango"):
					#Replace the item, remember what it was
					CS_replacement = reverse_alpha_inventory[CS_place_index]
					reverse_alpha_inventory[CS_place_index] = "Courage Shell"

					#Verify that this new inventory is at least capable of satisfying the remaining recipes
					if(remainingOutputsCanBeFulfilled(type_inventory, tempOutputsFulfilled, recipeList, itemNames)):
						#Calculate the overall frame count
						temp_frames_CS = TOSS_FRAMES + invFrames[20-reverse_alpha_inventory.count("BLOCKED")][CS_place_index]
						temp_frame_sum = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS + REVERSE_ALPHA_SORT_FRAMES

						#Get the index on where to insert this legal move to
						insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

						#Describe how the break should play out
						ch5description = "Ch.5 Break: DB in slot {0}, CO in slot {1}, KM in slot {2}, Sort (Reverse-Alpha), CS in slot {3}".format(DB_place_index+1,
																																		           CO_place_index+1,
																																		           KM_place_index+1,
																																		           CS_place_index+1)
						#Append the Legal Move
						legal_moves[step_index].insert(insertIndex,[ch5description,58,temp_frame_sum,copy.copy(reverse_alpha_inventory)])

					#Return the replaced items for the next loop
					reverse_alpha_inventory[CS_place_index] = CS_replacement

		#Type Sorted Inventory
		type_inventory = sortType(temp_inventory)

		#Only bother further evaluation if the sort placed the Coconut in the latter half of the inventory
		#Because the coconut is needed for duplication
		if(type_inventory.index("Coconut") >= 10):
			#Place the Courage Shell
			for CS_place_index in range(0,10):
				#Check that the Courage Shell doesn't replace DB, CO, or KM
				if(type_inventory[CS_place_index] != "Dried Bouquet" and
				   type_inventory[CS_place_index] != "Coconut" and
				   type_inventory[CS_place_index] != "Keel Mango"):
					#Replace the item, remember what it was
					CS_replacement = type_inventory[CS_place_index]
					type_inventory[CS_place_index] = "Courage Shell"

					#Verify that this new inventory is at least capable of satisfying the remaining recipes
					if(remainingOutputsCanBeFulfilled(type_inventory, tempOutputsFulfilled, recipeList, itemNames)):
						#Calculate the overall frame count
						temp_frames_CS = TOSS_FRAMES + invFrames[20-type_inventory.count("BLOCKED")][CS_place_index]
						temp_frame_sum = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS + TYPE_SORT_FRAMES

						#Get the index on where to insert this legal move to
						insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

						#Describe how the break should play out
						ch5description = "Ch.5 Break: DB in slot {0}, CO in slot {1}, KM in slot {2}, Sort (Type), CS in slot {3}".format(DB_place_index+1,
																																		  CO_place_index+1,
																																		  KM_place_index+1,
																																		  CS_place_index+1)
						#Append the Legal Move
						legal_moves[step_index].insert(insertIndex,[ch5description,58,temp_frame_sum,copy.copy(type_inventory)])

					#Return the replaced items for the next loop
					type_inventory[CS_place_index] = CS_replacement

		#Reverse Type Sorted Inventory
		reverse_type_inventory = sortReverseType(temp_inventory)

		#Only bother further evaluation if the sort placed the Coconut in the latter half of the inventory
		#Because the coconut is needed for duplication
		if(reverse_type_inventory.index("Coconut") >= 10):
			#Place the Courage Shell
			for CS_place_index in range(0,10):
				#Check that the Courage Shell doesn't replace DB, CO, or KM
				if(reverse_type_inventory[CS_place_index] != "Dried Bouquet" and
				   reverse_type_inventory[CS_place_index] != "Coconut" and
				   reverse_type_inventory[CS_place_index] != "Keel Mango"):
					#Replace the item, remember what it was
					CS_replacement = reverse_type_inventory[CS_place_index]
					reverse_type_inventory[CS_place_index] = "Courage Shell"

					#Verify that this new inventory is at least capable of satisfying the remaining recipes
					if(remainingOutputsCanBeFulfilled(reverse_type_inventory, tempOutputsFulfilled, recipeList, itemNames)):
						#Calculate the overall frame count
						temp_frames_CS = TOSS_FRAMES + invFrames[20-reverse_type_inventory.count("BLOCKED")][CS_place_index]
						temp_frame_sum = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS + REVERSE_TYPE_SORT_FRAMES

						#Get the index on where to insert this legal move to
						insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

						#Describe how the break should play out
						ch5description = "Ch.5 Break: DB in slot {0}, CO in slot {1}, KM in slot {2}, Sort (Reverse-Type), CS in slot {3}".format(DB_place_index+1,
																																		          CO_place_index+1,
																																		          KM_place_index+1,
																																		          CS_place_index+1)
						#Append the Legal Move
						legal_moves[step_index].insert(insertIndex,[ch5description,58,temp_frame_sum,copy.copy(reverse_type_inventory)])

					#Return the replaced items for the next loop
					reverse_type_inventory[CS_place_index] = CS_replacement

		#Return the replaced items for the next loop
		temp_inventory[KM_place_index] = KM_replacement

def calculateOrder(callNumber, currentFrameRecord, startingInventory, recipeList, invFrames):
	itemNames = []
	#Fill the itemNames
	for item in recipeList:
		itemNames.append(recipeList[item]["NAME"])
		log(7, "Calculator", "Items", "Scan", recipeList[item]["NAME"] + " scanned.")
	log(5, "Calculator", "Items", "Scan", "All item names scanned successfully.")
	randomise = bool(getConfig("randomise") == "True")
	select = bool(getConfig("select") == "True")
	#===============================================================================
	# GOAL
	#===============================================================================
	# The goal of this program is to find a roadmap of fulfilling all 57 Zess T.
	# recipes in as few frames as possible.
	#===============================================================================
	# RULES & ASSUMPTIONS
	#===============================================================================
	# A known glitch has been exploited that allows the ability to duplicate ingredient items
	# If you use an ingredient in slots 1-10, that slot becomes "NULL" and isn't duplicated
	# If you use an ingredient in slots 11-20, the item is duplicated
	# If there's a NULL slot, the recipe output will automatically fill the 1st NULL position
	# If there's no NULL slots, the player is given the option of tossing either the output item,
	#	or replacing any inventory in the first 10 slots item with the output item
	#	Attempting to replace an inventory itel in slots 11-20 will leave the inventory unchanged
	#		(In this instance, it's always faster to just toss the output item outright)
	# If there's a sort, all NULL slots are wiped away and are no longer available, becoming "BLOCKED" at the end of the inventory
	# "BLOCKED" spaces are assumed to be permanently unavailable for the remainder of recipe fulfillment
	# When navigating the inventory, it is assumed all "NULL" and "BLOCKED" spaces are hidden from the player
	#	For example, if 2 spaces are NULL, the player will only see the other 18 items to navigate through in the inventory
	# The first recipe that is fulfilled can only use a single ingredient


	# At some point, the player needs to trade 2 Hot Dogs and a Mousse Cake for a Dried Bouquet (Which is only needed for the Space Food recipe)
	# At another point, the player will need to collect the Keel Mango, Coconut, and Courage Shell after Chapter 5
	# So there's 2 sessions of recipe-fulfillment that will be needed (Pre-Ch.5 and Post-Ch.5)
	#===============================================================================
	# Algorithm Description
	#===============================================================================
	# Start Loop
	# Iterate through all Items that haven't been made already
	# Iterate through all their recipes that can be made with the current materials
	# Iterate through all placement options of the output ingredient (Tossing, Autofill, etc)
	# Determine how many relevant frames are required to fulfill this recipe and add it to a list of "legal moves" for the current state
	# Pick the Legal Move that takes the least frames, update the inventory based on that move, and recurse the loop again
	# If no legal moves are available and the end-state has not been reached,
	#	then return back up a layer and pick the next-fastest legal move at that state to recurse down
	# Repeat recursion until search space has been exhausted
	#===============================================================================

	#Total frames to choose an additional ingredient (As opposed to just a single ingredient)
	#This does not include the additional frames needed to navigate to the items that you want to use
	CHOOSE_2ND_INGREDIENT_FRAMES = 56
	#Total frames to toss any item (As opposed to the item being automatically placed in a NULL space)
	#This does not include the additional frames needed to navigate to the item that you want to toss
	TOSS_FRAMES = 23
	#Frames needed to sort the inventory by each method
	ALPHA_SORT_FRAMES = 38
	REVERSE_ALPHA_SORT_FRAMES = 40
	TYPE_SORT_FRAMES = 39
	REVERSE_TYPE_SORT_FRAMES = 41
	#If the player does not toss the final output item, 5 extra frames are needed to obtain jump storage
	JUMP_STORAGE_NO_TOSS_FRAMES = 5

	#start main loop
	while(True):
		stepIndex = 0
		iterationCount = 0
		#State Description for each "Step" taken
		writtenStep = ["Begin"]
		framesTaken = [0]
		totalFrames = [0]
		inventory = [startingInventory]
		outputCreated = [[False]*58]
		legalMoves = []

		#step_RECORD = -1

		while(iterationCount < 100000000):
	
			iterationCount += 1

			#if(stepIndex > step_RECORD):
			#	step_RECORD = stepIndex
			#	print(step_RECORD)
			#	printResults("results/DebugRoadmap.txt",writtenStep,framesTaken,totalFrames,inventory,outputCreated,itemNames,stepIndex)

			#Check for bad states to immediately retreat from
			if((not outputCreated[stepIndex][57] and (
				not "Fire Flower" in inventory[stepIndex] or
				not "Mystic Egg" in inventory[stepIndex] or
				not "Cake Mix" in inventory[stepIndex] or
				not "Turtley Leaf" in inventory[stepIndex] or 
				outputCreated[stepIndex][54] and not "Egg Bomb" in inventory[stepIndex]))): #If the Egg Bomb was made pre-Ch.5, make sure its still in the inventory
				#We need to have the fire flower for the post-chapter-5 intermission
		
				#Regardless of record status, it's time to go back up and find new endstates
				#Wipe away the current state
				writtenStep.pop()
				framesTaken.pop()
				totalFrames.pop()
				inventory.pop()
				outputCreated.pop()

				#Step back up a level
				stepIndex -= 1

			#Check for end condition (57 Recipes + the Chapter 5 intermission, which is treated as an additional "recipe")
			elif(outputCreated[stepIndex].count(True) == 58):
				#All Recipes have been fulfilled!
				#Check that the total time taken is strictly less than the current observed record.

				#Apply a frame penalty if the final move did not toss an item:
				if(not "toss" in writtenStep[-1]):
					writtenStep[-1] += " (No-Toss 5 Frame Penalty for Jump Storage)"
					framesTaken[-1] += JUMP_STORAGE_NO_TOSS_FRAMES
					totalFrames[-1] += JUMP_STORAGE_NO_TOSS_FRAMES
				else:
					writtenStep[-1] += " (Jump Storage on Tossed Item)"
		
				if(totalFrames[stepIndex] < currentFrameRecord):
					#New Record!
					currentFrameRecord = totalFrames[stepIndex]
					#print("New Record Time: {0}".format(totalFrames[stepIndex]))
					#Log the updated outcome
					printResults("results/[{0}].txt".format(totalFrames[stepIndex]),writtenStep,framesTaken,totalFrames,inventory,outputCreated,itemNames,stepIndex)

					return [totalFrames[stepIndex], callNumber]
						
				#Regardless of record status, its time to go back up and find new endstates
				#Wipe away the current state
				writtenStep.pop()
				framesTaken.pop()
				totalFrames.pop()
				inventory.pop()
				outputCreated.pop()

				#Step back up a level
				stepIndex -= 1

			#End condition not met, Check if this current level has something in the event queue
			elif(len(legalMoves) == stepIndex):
				legalMoves.append([])
				#Generate the list of all possible decisions

				#Only evaluate the 57th recipe (Mistake) when its the last recipe to fulfill
				# This is because it is relatively easy to craft this output with many of the previous outputs, and will take minimal frames
				if(outputCreated[stepIndex].count(True) == 57):
					upperOutputLimit = 58
				else:
					upperOutputLimit = 57
		
				for outputItem in range(1,upperOutputLimit):
					#Only want recipes that haven't already been fulfilled
					if(not outputCreated[stepIndex][outputItem-1]):
						#Iterate through all ingredientlists
						for recipe in recipeList[outputItem]["RECIPES"]:
							#Only want ingredient lists that can be satisfied by the current inventory
							if(all([ingredient in inventory[stepIndex] for ingredient in recipe])):						
								#This is a recipe that can be fulfilled right now!
								tempInventory = copy.copy(inventory[stepIndex])

								#Mark that the output has been fulfilled for viability determination
								tempOutputsFulfilled = copy.copy(outputCreated[stepIndex])
								tempOutputsFulfilled[outputItem-1] = True
						
								if(len(recipe) == 1):
									#This is a potentially viable recipe with 1 ingredient

									#Determine how many viable items are in the list (No Nulls or Blocked), and the location of the ingredient
									viableItems = 20 - (tempInventory.count("NULL")+tempInventory.count("BLOCKED"))
									ingredientLoc = tempInventory.index(recipe[0])

									#Determine the offset by "NULL"s before the desired item, as NULLs do not appear during inventory navigation
									ingredientOffset = 0
									for i in range(0,ingredientLoc):
										if(tempInventory[i] == "NULL"):
											ingredientOffset += 1

									#Modify the inventory if the ingredient was in the first 10 slots
									if(ingredientLoc < 10):
										tempInventory[ingredientLoc] = "NULL"

									#Determine how many frames will be needed to select that item  
									tempFrames = invFrames[viableItems][ingredientLoc-ingredientOffset]

									#Describe what items were used
									useDescription = "Use {0} in slot {1} ".format(recipe[0],ingredientLoc+1)
								else:							 
									#This is a potentially viable recipe with 2 ingredients
									#Baseline frames based on how many times we need to access the menu
									tempFrames = CHOOSE_2ND_INGREDIENT_FRAMES

									#Mark that the output has been fulfilled
									tempOutputsFulfilled = copy.copy(outputCreated[stepIndex])
									tempOutputsFulfilled[outputItem - 1] = True

									#Determine how many viable spaces there are and the locations of both ingredients
									viableItems = 20 - (tempInventory.count("NULL")+tempInventory.count("BLOCKED")) 
									ingredientLoc = [tempInventory.index(recipe[0]),
													 tempInventory.index(recipe[1])]

									ingredientName = [recipe[0],recipe[1]]
									ingredientOffset = [0,0]

									for ingred_eval in range(len(ingredientName)):
										ingredientOffset[ingred_eval] = 0
										for i in range(0,ingredientLoc[ingred_eval]):
											if(tempInventory[i] == "NULL"):
												ingredientOffset[ingred_eval] += 1

									#Determine which order of ingredients to take
									#The first picked item always vanishes from the list of ingredients when picking the 2nd ingredient
									#There are some configurations where it is 2 frames faster to pick the ingredients in the reverse order
									if((ingredientLoc[0]-ingredientOffset[0] >= 2 and
									    ingredientLoc[0]                     >  ingredientLoc[1] and
										ingredientLoc[0]-ingredientOffset[0] <= (viableItems//2)) or
									   (ingredientLoc[0]                     <  ingredientLoc[1] and
									    ingredientLoc[0]-ingredientOffset[0] >= (viableItems//2))):
										#It's faster to select the 2nd item, so make it the priority and switch the order
										ingredientLoc.reverse()
										ingredientOffset.reverse()
										ingredientName.reverse()

									#Calculate the number of frames needed to grab the first item
									tempFrames += invFrames[viableItems][ingredientLoc[0]-ingredientOffset[0]]

									#Set this inventory index to null if the item was in the first 10 slots
									#Also determine the frames needed for the 2nd ingredient
									if(ingredientLoc[0] < 10):
										tempInventory[ingredientLoc[0]] = "NULL"
										#print("---")
										#print(ingredientLoc)
										#print(ingredientOffset)
										#print(viableItems)
										tempFrames += invFrames[viableItems-1][ingredientLoc[1]-ingredientOffset[1]-1]
									else:
										tempFrames += invFrames[viableItems-0][ingredientLoc[1]-ingredientOffset[1]-0]

									#Set this inventory index to null if the item was in the first 10 slots
									if(ingredientLoc[1] < 10):
										tempInventory[ingredientLoc[1]] = "NULL"

									#Describe what items were used
									useDescription = "Use {0} in slot {1} and {2} in slot {3} ".format(ingredientName[0],
																									   ingredientLoc[0]+1,
																									   ingredientName[1],
																									   ingredientLoc[1]+1)

								#Handle allocation of the OUTPUT variable
								#Options vary by whether there are "NULL"s within the inventory
								try:
									#If there are NULLs in the inventory. The output will always go to 1st NULL in the inventory 
									placedIndex = tempInventory.index("NULL")

									tempInventory[placedIndex] = recipeList[outputItem]["NAME"]

									#Check to see if this state is viable
									if(remainingOutputsCanBeFulfilled(tempInventory, tempOutputsFulfilled, recipeList, itemNames)):
										#This is a viable state that doesn't increase frames at all (Output was auto-placed)
										#Determine where to insert this legal move into the list of legal moves (Sorted by frames taken)
										insertIndex = getInsertionIndex(legalMoves, stepIndex, tempFrames)

										placeDescription = "to make {0}, auto-placed in slot {1}".format(itemNames[outputItem-1],placedIndex+1)
										legalMoves[stepIndex].insert(insertIndex,[useDescription+placeDescription,outputItem,tempFrames,tempInventory])
								except:
									#There are no NULLs in the inventory. Something must be tossed
									#Total number of frames increased by forcing to toss something
									tempFrames += TOSS_FRAMES
							
									#Evaluate viability of tossing the output item itself
									if(remainingOutputsCanBeFulfilled(tempInventory, tempOutputsFulfilled, recipeList, itemNames)):
										#Temp frames do not increase as the output item is always at the very top of the list
										insertIndex = getInsertionIndex(legalMoves, stepIndex, tempFrames)


										placeDescription = "to make (and toss) {0}".format(itemNames[outputItem-1])
										legalMoves[stepIndex].insert(insertIndex,[useDescription+placeDescription,outputItem,tempFrames,tempInventory])

									#Evaluate the viability of tossing all current inventory items
									#Assumed that it is impossible to toss and replace any items in the last 10 positions
									for tossedIndex in range(0,10):
										#Only interested in slots that contain an actual item
										if(tempInventory[tossedIndex] == "NULL" or
										   tempInventory[tossedIndex] == "BLOCKED"):
											log(2, "Calculator", "Warn", "", "Shouldn't be here!")
											input()
										#Make a copy of the tempInventory with the replaced item
										replacedInventory = copy.copy(tempInventory)
										replacedInventory[tossedIndex] = itemNames[outputItem-1]
										tossedItemName = tempInventory[tossedIndex]

										if(remainingOutputsCanBeFulfilled(replacedInventory, tempOutputsFulfilled, recipeList, itemNames)):
											#Calculate the additional tossed frames. Have to +1 both viableItems and tosseditem as
											#the output is at the top of the list, pushing everything else down one spot
											replacedFrames = tempFrames+invFrames[viableItems+1][tossedIndex+1]
											insertIndex = getInsertionIndex(legalMoves, stepIndex, replacedFrames)
										
											placeDescription = "to make {0}, toss {1} in slot {2}".format(itemNames[outputItem-1],
																										   tossedItemName,
																										   tossedIndex+1)
											legalMoves[stepIndex].insert(insertIndex,[useDescription+placeDescription,outputItem,replacedFrames,replacedInventory])

				#=========================================================================================			
				# Special handling of the 58th item, which is representative of the Chapter 5 Intermission
				#=========================================================================================
				#The first item is trading the Mousse Cake and 2 Hot Dogs for a Dried Bouquet
				#Inventory must contain both items, Hot Dog must be in a slot that can be duplicated
				if(not outputCreated[stepIndex][57] and
				   "Mousse Cake" in inventory[stepIndex] and
				   "Hot Dog" in inventory[stepIndex][10:20]):

					#Create an outputs chart but with the Dried Bouquet collected
					#To ensure the produced inventory can fulfill all remaining recipes
					tempOutputsFulfilled = copy.copy(outputCreated[stepIndex])
					tempOutputsFulfilled[57] = True

					#Create a temp inventory
					tempInventory = copy.copy(inventory[stepIndex])

					#Determine how many spaces are available in the inventory
					#For frame calculation purposes
					viableItems = 20 - tempInventory.count("BLOCKED")

					#If the Mousse Cake is in the first 10 spots, change it to NULL
					#As it is used to acquire the Dried Bouquet (Hot Dog needs to be duped)
					mousse_cake_loc = tempInventory.index("Mousse Cake")
					if(mousse_cake_loc < 10):
						tempInventory[mousse_cake_loc] = "NULL"

					#Handle allocation of the first 2 Ch.5 Items (Dried Bouquet and Coconut)	
					if(tempInventory.count("NULL") >= 2):
						#The Dried Bouquet gets Auto Placed in the 1st available NULL
						tempindexDB = tempInventory.index("NULL")
						tempInventory[tempindexDB] = "Dried Bouquet"
						
						#Auto Placing takes zero frames
						temp_frames_DB = 0

						#The Coconut gets Auto Placed in the 2nd available NULL
						tempindexCO = tempInventory.index("NULL")
						tempInventory[tempindexCO] = "Coconut"

						#Auto Placing takes zero frames
						temp_frames_CO = 0
						
						#Handle the Allocation of the Coconut Sort, Keel Mango, and Courage Shell
						HandleChapter5Eval(legalMoves, stepIndex, tempInventory, tempOutputsFulfilled, recipeList, itemNames, invFrames, temp_frames_DB, temp_frames_CO)

					elif(tempInventory.count("NULL") == 1):
						#The Dried Bouquet gets Auto Placed in the 1st available NULL
						tempindexDB = tempInventory.index("NULL")
						tempInventory[tempindexDB] = "Dried Bouquet"

						#Auto Placing takes zero frames
						temp_frames_DB = 0

						#The Coconut can only be placed in first 10 slots
						for tempindexCO in range(0,10):
							#Don't waste time replacing the Dried Bouquet with the Coconut
							if(tempindexCO != tempindexDB):
								#Replace the item with the Coconut, but remember the replaced item
								tossed_item_1 = tempInventory[tempindexCO]
								tempInventory[tempindexCO] = "Coconut"

								#Calculate the number of frames needed to pick this slot for replacement
								temp_frames_CO = TOSS_FRAMES + invFrames[viableItems][tempindexCO]

								#Handle the Allocation of the Coconut Sort, Keel Mango, and Courage Shell
								HandleChapter5Eval(legalMoves, stepIndex, tempInventory, tempOutputsFulfilled, recipeList, itemNames, invFrames, temp_frames_DB, temp_frames_CO)

								#Reset what was previously in the Coconut's slot
								tempInventory[tempindexCO] = tossed_item_1
					else:
						#No NULLs to utilize for Chapter 5 Intermission
						#The Dried Bouquet can only be placed in the first 10 slots
						for tempindexDB in range(0,10):

							#Replace the item with the Dried Bouquet, but remember the replaced item
							tossed_item_1 = tempInventory[tempindexDB]
							tempInventory[tempindexDB] = "Dried Bouquet"

							#Calculate the number of frames needed to pick this slot for replacement
							temp_frames_DB = TOSS_FRAMES + invFrames[viableItems][tempindexDB]

							#The Coconut can only be placed in first 10 slots
							for tempindexCO in range(0,10):
								#Don't waste time replacing the Dried Bouquet with the Coconut
								if(tempindexCO != tempindexDB):
									#Handle the Allocation of the Coconut Sort, Keel Mango, and Courage Shell
									
									#Replace the item with the Dried Bouquet, but remember the replaced item
									tossed_item_2 = tempInventory[tempindexCO]
									tempInventory[tempindexCO] = "Coconut"

									#Calculate the number of frames needed to pick this slot for replacement
									temp_frames_CO = TOSS_FRAMES + invFrames[viableItems][tempindexCO]

									#Handle the Allocation of the Coconut Sort, Keel Mango, and Courage Shell
									HandleChapter5Eval(legalMoves, stepIndex, tempInventory, tempOutputsFulfilled, recipeList, itemNames, invFrames, temp_frames_DB, temp_frames_CO)

									#Reset what was preciously in the Coconut's Slot
									tempInventory[tempindexCO] = tossed_item_2
							
							#Reset what was previously in the Dried Bouquet's Slot
							tempInventory[tempindexDB] = tossed_item_1
				
				#======================================
				# Special Handling of Inventory Sorting
				#======================================
				#Avoid redundant searches
				if(writtenStep[stepIndex][0:4] != "Sort"):

					#Count the Number of sorts for capping purposes
					total_sorts = 0
					for i in range(0,stepIndex+1):
						if(writtenStep[i][0:4] == "Sort"):
							total_sorts += 1

					#Limit the number of sorts allowed in a roadmap
					if(total_sorts <= 10):
						
						#Alphabetical Sort
						alpha_inventory = sortAlpha(inventory[stepIndex])

						#Only add the legal move if the sort actually changes the inventory
						if(alpha_inventory != inventory[stepIndex]):
							tempindex = 0
							while(tempindex < len(legalMoves[stepIndex]) and legalMoves[stepIndex][tempindex][2] < ALPHA_SORT_FRAMES):
								tempindex += 1

							description = "Sort - Alphabetical"
							#legalMoves[stepIndex].insert(tempindex,[description,-1,alphaSortFrames,alphainventory])
							legalMoves[stepIndex].append([description,-1,ALPHA_SORT_FRAMES,alpha_inventory])

						#Reverse Alphabetical Sort
						reverse_alpha_inventory = sortReverseAlpha(inventory[stepIndex])

						#Only add the legal move if the sort actually changes the inventory
						if(reverse_alpha_inventory != inventory[stepIndex]):
							tempindex = 0
							while(tempindex < len(legalMoves[stepIndex]) and legalMoves[stepIndex][tempindex][2] < REVERSE_ALPHA_SORT_FRAMES):
								tempindex += 1

							description = "Sort - Reverse Alphabetical"
							#legalMoves[stepIndex].insert(tempindex,[description,-1,reversAlphaSortFrames,reversealphainventory])
							legalMoves[stepIndex].append([description,-1,REVERSE_ALPHA_SORT_FRAMES,reverse_alpha_inventory])

						#Type Sort
						type_inventory = sortType(inventory[stepIndex])

						#Only add the legal move if the sort actually changes the inventory
						if(type_inventory != inventory[stepIndex]):
							tempindex = 0
							while(tempindex < len(legalMoves[stepIndex]) and legalMoves[stepIndex][tempindex][2] < TYPE_SORT_FRAMES):
								tempindex += 1

							description = "Sort - Type"
							#legalMoves[stepIndex].insert(tempindex,[description,-1,typeSortFrames,typeinventory])
							legalMoves[stepIndex].append([description,-1,TYPE_SORT_FRAMES,type_inventory])

						#Reverse Type Sort
						reverse_type_inventory = sortReverseType(inventory[stepIndex])

						#Only add the legal move if the sort actually changes the inventory
						if(reverse_type_inventory != inventory[stepIndex]):
							tempindex = 0
							while(tempindex < len(legalMoves[stepIndex]) and legalMoves[stepIndex][tempindex][2] < REVERSE_TYPE_SORT_FRAMES):
								tempindex += 1

							description = "Sort - Reverse Type"
							#legalMoves[stepIndex].insert(tempindex,[description,-1,reverseTypeSortFrames,reversetypeinventory])
							legalMoves[stepIndex].append([description,-1,REVERSE_TYPE_SORT_FRAMES,reverse_type_inventory])

				#=====================================
				#All Legal Moves Evaluated and Listed!
				#=====================================

				#Filter out all legal moves that would exceed the current frame limit
				legalMoves[stepIndex] = list(filter(lambda x: x[2]+totalFrames[stepIndex] < currentFrameRecord, legalMoves[stepIndex]))
			
				#Filter out all legal moves that use 2 ingredients in the very first legal move
				if(stepIndex == 0):
					legalMoves[stepIndex] = list(filter(lambda x: not " and " in x[0], legalMoves[stepIndex]))

				#Just because, if the step index is sufficiently small, just shuffle!
				if(randomise and stepIndex < 20):
					random.shuffle(legalMoves[stepIndex])

				#Interesting methodology to pick out decent legal moves
				if(select and stepIndex < 30) :
					while(len(legalMoves[stepIndex]) > 1 and random.random() < 0.15):
						legalMoves[stepIndex].pop(-1)

				if(len(legalMoves[stepIndex]) == 0):
					#There are no legal moves to iterate on, go back up...
					#Wipe away the current state
					writtenStep.pop()
					framesTaken.pop()
					totalFrames.pop()
					inventory.pop()
					outputCreated.pop()
					legalMoves.pop()

					#Step back up a level
					stepIndex -= 1
				else:
					#Once the list is generated, choose the top-most (quickest) path and iterate downward
					writtenStep.append(legalMoves[stepIndex][0][0])
					framesTaken.append(legalMoves[stepIndex][0][2])
					totalFrames.append(totalFrames[stepIndex] + legalMoves[stepIndex][0][2])
					inventory.append(legalMoves[stepIndex][0][3])
					outputCreated.append(copy.copy(outputCreated[stepIndex]))

					if(legalMoves[stepIndex][0][1] >= 0):
						outputCreated[stepIndex + 1][legalMoves[stepIndex][0][1]-1] = True

					stepIndex += 1
			else:
				#Pop the 1st instance of the list, as it has already been recursed down
				legalMoves[stepIndex].pop(0)

				#Filter out all legal moves that would exceed the current frame limit
				legalMoves[stepIndex] = list(filter(lambda x: x[2]+totalFrames[stepIndex] < currentFrameRecord, legalMoves[stepIndex]))

				#Just because, if the step index is sufficiently small, just shuffle!
				if(randomise):
					if(stepIndex < 20):
						random.shuffle(legalMoves[stepIndex])

				if(len(legalMoves[stepIndex]) == 0):
					#No legal moves are left to evaluate, go back up...
					#Wipe away the current state
					writtenStep.pop()
					framesTaken.pop()
					totalFrames.pop()
					inventory.pop()
					outputCreated.pop()
					legalMoves.pop()

					#Step back up a level
					stepIndex -= 1
				else:
					#Once the list is generated, choose the top-most (quickest) path and iterate downward
					writtenStep.append(legalMoves[stepIndex][0][0])
					framesTaken.append(legalMoves[stepIndex][0][2])
					totalFrames.append(totalFrames[stepIndex] + legalMoves[stepIndex][0][2])
					inventory.append(legalMoves[stepIndex][0][3])
					outputCreated.append(copy.copy(outputCreated[stepIndex]))

					if(legalMoves[stepIndex][0][1] >= 0):
						outputCreated[stepIndex + 1][legalMoves[stepIndex][0][1]-1] = True

					stepIndex += 1
					#logging for progress display
					if(iterationCount % 500000 == 0):
						log(3, "Calculator", "Info", "Call " + str(callNumber), "{0} Steps taken using {1} frames; {2}k iterations".format(stepIndex, totalFrames[stepIndex], iterationCount / 1000))
					elif(iterationCount % 100000 == 0):
						log(4, "Calculator", "Info", "Call " + str(callNumber), "{0} Steps taken using {1} frames; {2}k iterations".format(stepIndex, totalFrames[stepIndex], iterationCount / 1000))
					elif(iterationCount % 1000 == 0):
						log(6, "Calculator", "Info", "Call " + str(callNumber), "{0} Steps taken using {1} frames; {2}k iterations".format(stepIndex, totalFrames[stepIndex], iterationCount / 1000))

import copy
import random
from logger import log
from inventory import getAlphaSort, getTypeSort, remainingOutputsCanBeFulfilled
from moves import getInsertionIndex
from config import getConfig

#Total frames to choose an additional ingredient (As opposed to just a single ingredient)
#This does not include the additional frames needed to navigate to the items that you want to use
CHOOSE_2ND_INGREDIENT_FRAMES = 56
#Total frames to toss any item (As opposed to the item being automatically placed in a NULL space)
#This does not include the additional frames needed to navigate to the item that you want to toss
TOSS_FRAMES = 32
#Frames needed to sort the inventory by each method
ALPHA_SORT_FRAMES = 38
REVERSE_ALPHA_SORT_FRAMES = 40
TYPE_SORT_FRAMES = 39
REVERSE_TYPE_SORT_FRAMES = 41
#If the player does not toss the final output item, 5 extra frames are needed to obtain jump storage
JUMP_STORAGE_NO_TOSS_FRAMES = 5

#Finished Roadmaps can potentially have some legal moves rearranged to faster points in time
#Give the search space some buffer frames so that if a roadmap is discovered that is "close" to the frame record,
#Perform optimal shuffling of the moves to find the best possible rearranged roadmap and evaluate for new records
BUFFER_SEARCH_FRAMES = 120

def printResults(filename, writtenStep, framesTaken, totalFrames, inventory, outputCreated, itemNames):
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
	for i in range(0, len(writtenStep)):
		file.write("{0}\t{1}\t{2}".format(writtenStep[i],framesTaken[i],totalFrames[i]))
		for z in range(20):
			file.write("\t{0}".format(inventory[i][z]))
		for z in range(58):
			file.write("\t{0}".format(outputCreated[i][z]))
		file.write("\n")
		log(5, "Calculator", "File", "Write", "Data for Step " + str(writtenStep[i]) + " written.")
	file.close()

#Return the sorted version of the inventory, as dictated by the full sorted dictionary
#Also which direction to sort the inventory
def getSortedInventory(inventory, full_sorted_list, is_reversed):
	sorted_inventory = []

	if(is_reversed):
		for i in range(len(full_sorted_list)-1,-1,-1):
			for j in range(0,inventory.count(full_sorted_list[i])):
				sorted_inventory.append(full_sorted_list[i])
	else:
		for i in range(0,len(full_sorted_list)):
			for j in range(0,inventory.count(full_sorted_list[i])):
				sorted_inventory.append(full_sorted_list[i])

	#Remaining Spaces are "Blocked"
	while(len(sorted_inventory) < 20):
		sorted_inventory.append("BLOCKED")

	return sorted_inventory

#Handles Allocation of the Keel Mango and Courage Shell
#Both of which happen *after* the sort to correctly place the Coconut in a location
#Where it can be duplicated
def handleChapter5EarlySortEndItems(legal_moves,
									step_index,
									inventory,
									tempOutputsFulfilled,
									recipeList,
									itemNames,
									invFrames,
									SORT_FRAMES,
									sort_name,
									temp_frames_DB,
									temp_frames_CO,
									DB_place_index,
									CO_place_index):
	#Place the Keel Mango and Courage Shell
	for KM_place_index in range(0,10):
		for CS_place_index in range(KM_place_index+1,10):

			#Replace the 1st chosen item with the KM
			kmcs_temp_inventory = copy.copy(inventory)
			for index_eval in range(KM_place_index,0,-1):
				kmcs_temp_inventory[index_eval] = kmcs_temp_inventory[index_eval-1]
			
			kmcs_temp_inventory[0] = "Keel Mango"

			#Replace the 2nd chosen item with the CO
			for index_eval in range(CS_place_index,0,-1):
				kmcs_temp_inventory[index_eval] = kmcs_temp_inventory[index_eval-1]
			
			kmcs_temp_inventory[0] = "Courage Shell"

			#Ensure the Thunder Rage is still in the inventory
			if(kmcs_temp_inventory.count("Thunder Rage") == 1):
				#The next event is using the Thunder Rage item before resuming the 2nd session of recipe fulfillment
				TR_use_index = kmcs_temp_inventory.index("Thunder Rage")

				if(TR_use_index < 10):
					#Using the Thunder Rage will cause a NULL to appear in that slot
					kmcs_temp_inventory[TR_use_index] = "NULL"

				#Calculate the frames of these actions
				temp_frames_KM = TOSS_FRAMES + invFrames[20-kmcs_temp_inventory.count("BLOCKED")][KM_place_index]
				temp_frames_CS = TOSS_FRAMES + invFrames[20-kmcs_temp_inventory.count("BLOCKED")][CS_place_index]
				temp_frames_TR =               invFrames[20-kmcs_temp_inventory.count("BLOCKED")][TR_use_index]
				temp_frame_sum = (temp_frames_DB +
								temp_frames_CO +
								temp_frames_KM +
								temp_frames_CS +
								temp_frames_TR +
								SORT_FRAMES)

				#Determine if the remaining inventory is sufficient to fulfill all remaining recipes
				if(remainingOutputsCanBeFulfilled(kmcs_temp_inventory, tempOutputsFulfilled, recipeList, itemNames)):
					#Get the index on where to insert this legal move to
					insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

					#Describe how the break should play out
					desc = "Ch.5 Break: Replace #{1} for DB, Replace #{2} for CO, Sort ({0}), Replace #{3} for KM, replace #{4} for CS, Use TR in #{5}".format(sort_name,
																																			   				   DB_place_index+1,
																																		       				   CO_place_index+1,
																																		       				   KM_place_index+1,
																																		       				   CS_place_index+1,
																																			   				   TR_use_index+1)
					#Append the Legal Move
					legal_moves[step_index].insert(insertIndex,[desc,58,temp_frame_sum,copy.copy(kmcs_temp_inventory)])

#Handles Allocation of the Courage Shell
#The inventory has already had the keel mango placed,
#and a sort has occurred to place the coconut into a location
#where it can be duplicated.
def handleChapter5LateSortEndItems(legal_moves,
								   step_index,
								   inventory,
								   tempOutputsFulfilled,
								   recipeList,
								   itemNames,
								   invFrames,
								   SORT_FRAMES,
								   sort_name,
								   temp_frames_DB,
								   temp_frames_CO,
								   temp_frames_KM,
								   DB_place_index,
								   CO_place_index,
								   KM_place_index):
	#Place the Courage Shell
	for CS_place_index in range(0,10):

		#Replace the chosen item with the CS
		cs_temp_inventory = copy.copy(inventory)
		for index_eval in range(CS_place_index,0,-1):
			cs_temp_inventory[index_eval] = cs_temp_inventory[index_eval-1]
		
		cs_temp_inventory[0] = "Courage Shell"

		#Ensure the Thunder Rage is still in the inventory
		if(cs_temp_inventory.count("Thunder Rage") == 1):
			#The next event is using the Thunder Rage item before resuming the 2nd session of recipe fulfillment
			TR_use_index = cs_temp_inventory.index("Thunder Rage")

			if(TR_use_index < 10):
				#Using the Thunder Rage will cause a NULL to appear in that slot
				cs_temp_inventory[TR_use_index] = "NULL"

			#Calculate the frames of these actions
			temp_frames_CS = TOSS_FRAMES + invFrames[20-cs_temp_inventory.count("BLOCKED")][CS_place_index]
			temp_frames_TR =               invFrames[20-cs_temp_inventory.count("BLOCKED")][TR_use_index]
			temp_frame_sum = (temp_frames_DB +
							  temp_frames_CO +
							  temp_frames_KM +
							  temp_frames_CS +
							  temp_frames_TR +
							  SORT_FRAMES)

			#Determine if the remaining inventory is sufficient to fulfill all remaining recipes
			if(remainingOutputsCanBeFulfilled(cs_temp_inventory, tempOutputsFulfilled, recipeList, itemNames)):
				#Get the index on where to insert this legal move to
				insertIndex = getInsertionIndex(legal_moves, step_index, temp_frame_sum)

				#Describe how the break should play out
				desc = "Ch.5 Break: Replace #{1} for DB, Replace #{2} for CO, Replace #{3} for KM, Sort ({0}), replace #{4} for CS, Use TR in #{5}".format(sort_name,
																																						   DB_place_index+1,
																																						   CO_place_index+1,
																																						   KM_place_index+1,
																																						   CS_place_index+1,
																																						   TR_use_index+1)
				#Append the Legal Move
				legal_moves[step_index].insert(insertIndex,[desc,58,temp_frame_sum,copy.copy(cs_temp_inventory)])

#Evaluates all possible placements of the Keel Mango and Courage Shell
#And all possible locations and types of sorting that can place the Coconut into a position where it can be duplicated
def handleChapter5Eval(legal_moves,
					   step_index,
					   temp_inventory,
					   tempOutputsFulfilled,
					   recipeList,
					   itemNames,
					   invFrames,
					   temp_frames_DB,
					   temp_frames_CO,
					   DB_place_index,
					   CO_place_index,
					   full_alpha_list,
					   full_type_list):

	#======================================
	#Evaluate sorting before the Keel Mango
	#======================================

	#Alphabetically Sorted Inventory
	alpha_inventory = getSortedInventory(temp_inventory, full_alpha_list, False)

	#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
	#Because the coconut is needed for duplication
	if(alpha_inventory.index("Coconut") >= 10):
		#Handle all placements of the Keel Mango, Courage Shell, and usage of the Thunder Rage
		handleChapter5EarlySortEndItems(legal_moves,
										step_index,
										alpha_inventory,
										tempOutputsFulfilled,
										recipeList,
										itemNames,
										invFrames,
										ALPHA_SORT_FRAMES,
										"Alpha",
										temp_frames_DB,
										temp_frames_CO,
										DB_place_index,
										CO_place_index)

	#Reverse Alphabetical Sorted Inventory
	reverse_alpha_inventory = getSortedInventory(temp_inventory, full_alpha_list, True)

	#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
	#Because the coconut is needed for duplication
	if(reverse_alpha_inventory.index("Coconut") >= 10):
		#Handle all placements of the Keel Mango, Courage Shell, and usage of the Thunder Rage
		handleChapter5EarlySortEndItems(legal_moves,
										step_index,
										reverse_alpha_inventory,
										tempOutputsFulfilled,
										recipeList,
										itemNames,
										invFrames,
										REVERSE_ALPHA_SORT_FRAMES,
										"Reverse-Alpha",
										temp_frames_DB,
										temp_frames_CO,
										DB_place_index,
										CO_place_index)

	#Type Sorted Inventory
	type_inventory = getSortedInventory(temp_inventory, full_type_list, False)

	#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
	#Because the coconut is needed for duplication
	if(type_inventory.index("Coconut") >= 10):
		#Handle all placements of the Keel Mango, Courage Shell, and usage of the Thunder Rage
		handleChapter5EarlySortEndItems(legal_moves,
										step_index,
										type_inventory,
										tempOutputsFulfilled,
										recipeList,
										itemNames,
										invFrames,
										TYPE_SORT_FRAMES,
										"Type",
										temp_frames_DB,
										temp_frames_CO,
										DB_place_index,
										CO_place_index)

	#Reverse Type Sorted Inventory
	reverse_type_inventory = getSortedInventory(temp_inventory, full_type_list, True)

	#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
	#Because the coconut is needed for duplication
	if(reverse_type_inventory.index("Coconut") >= 10):
		#Handle all placements of the Keel Mango, Courage Shell, and usage of the Thunder Rage
		handleChapter5EarlySortEndItems(legal_moves,
										step_index,
										reverse_type_inventory,
										tempOutputsFulfilled,
										recipeList,
										itemNames,
										invFrames,
										REVERSE_TYPE_SORT_FRAMES,
										"Reverse-Type",
										temp_frames_DB,
										temp_frames_CO,
										DB_place_index,
										CO_place_index)

	#=====================================
	#Evaluate sorting after the Keel Mango
	#=====================================

	#Default Keel Mango Placement Bounds
	KM_upper_bound = 10

	#Restrict the bounds if there is still a "NULL" in the inventory
	#Because the Keel Mango can only go into the first slot
	if("NULL" in temp_inventory):
		KM_upper_bound = 1

	#Place the Keel Mango
	for KM_place_index in range(0,KM_upper_bound):
		#Making a copy of the temp inventory for what it looks like after the allocation of the KM
		#This is just the easiest method I could think of, it can probably be done more efficiently
		km_temp_inventory = copy.copy(temp_inventory)

		#Calculate the needed frames
		if(KM_upper_bound == 10):
			#An item is being tossed
			temp_frames_KM = TOSS_FRAMES + invFrames[20 - km_temp_inventory.count("BLOCKED")][KM_place_index]

			#Update the inventory such that all items above the NULL are moved down one place
			#And the KM is placed into slot 1
			for index_eval in range(KM_place_index,0,-1):
				km_temp_inventory[index_eval] = km_temp_inventory[index_eval-1]
		else:
			#There was a null somewhere, so this is effectively a free action
			temp_frames_KM = 0

			#Update the inventory such that all items above the NULL are moved down one place
			#And the KM is placed into slot 1
			for index_eval in range(km_temp_inventory.index("NULL"),0,-1):
				km_temp_inventory[index_eval] = km_temp_inventory[index_eval-1]

		#The vacancy at the start of the inventory is now occupied with the new item
		km_temp_inventory[0] = "Keel Mango"

		#Ensure the Coconut is in the remaining inventory
		if(km_temp_inventory.count("Coconut") == 1):
			#Perform all sorts
			#Alphabetically Sorted Inventory
			alpha_inventory = getSortedInventory(km_temp_inventory, full_alpha_list, False)

			#Only bother with further evaluation if the sort placed the Coconut in the latter half of the inventory
			#Because the coconut is needed for duplication
			if(alpha_inventory.index("Coconut") >= 10):
				#Handle all placements of the Courage Shell and usage of the Thunder Rage
				handleChapter5LateSortEndItems(legal_moves,
											   step_index,
											   alpha_inventory,
											   tempOutputsFulfilled,
											   recipeList,
											   itemNames,
											   invFrames,
											   ALPHA_SORT_FRAMES,
											   "Alpha",
											   temp_frames_DB,
											   temp_frames_CO,
											   temp_frames_KM,
											   DB_place_index,
											   CO_place_index,
											   KM_place_index)

			#Reverse Alphabetical Sorted Inventory
			reverse_alpha_inventory = getSortedInventory(km_temp_inventory, full_alpha_list, True)

			#Only bother further evaluation if the sort placed the Coconut in the latter half of the inventory
			#Because the coconut is needed for duplication
			if(reverse_alpha_inventory.index("Coconut") >= 10):
				#Handle all placements of the Courage Shell and usage of the Thunder Rage
				handleChapter5LateSortEndItems(legal_moves,
											   step_index,
											   reverse_alpha_inventory,
											   tempOutputsFulfilled,
											   recipeList,
											   itemNames,
											   invFrames,
											   REVERSE_ALPHA_SORT_FRAMES,
											   "Reverse-Alpha",
											   temp_frames_DB,
											   temp_frames_CO,
											   temp_frames_KM,
											   DB_place_index,
											   CO_place_index,
											   KM_place_index)

			#Type Sorted Inventory
			type_inventory = getSortedInventory(km_temp_inventory, full_type_list, False)

			#Only bother further evaluation if the sort placed the Coconut in the latter half of the inventory
			#Because the coconut is needed for duplication
			if(type_inventory.index("Coconut") >= 10):
				#Handle all placements of the Courage Shell and usage of the Thunder Rage
				handleChapter5LateSortEndItems(legal_moves,
											   step_index,
											   type_inventory,
											   tempOutputsFulfilled,
											   recipeList,
											   itemNames,
											   invFrames,
											   TYPE_SORT_FRAMES,
											   "Type",
											   temp_frames_DB,
											   temp_frames_CO,
											   temp_frames_KM,
											   DB_place_index,
											   CO_place_index,
											   KM_place_index)

			#Reverse Type Sorted Inventory
			reverse_type_inventory = getSortedInventory(km_temp_inventory, full_type_list, True)

			#Only bother further evaluation if the sort placed the Coconut in the latter half of the inventory
			#Because the coconut is needed for duplication
			if(reverse_type_inventory.index("Coconut") >= 10):
				#Handle all placements of the Courage Shell and usage of the Thunder Rage
				handleChapter5LateSortEndItems(legal_moves,
											   step_index,
											   reverse_type_inventory,
											   tempOutputsFulfilled,
											   recipeList,
											   itemNames,
											   invFrames,
											   REVERSE_TYPE_SORT_FRAMES,
											   "Reverse-Type",
											   temp_frames_DB,
											   temp_frames_CO,
											   temp_frames_KM,
											   DB_place_index,
											   CO_place_index,
											   KM_place_index)

#OptimizeRoadMap
#Rearranges a given roadmap where possible to reduce the total number of frames
#Only works for legal moves that don't alter the inventory
def OptimizeRoadMap(written_step,
					frames_taken,
					total_frames,
					inventory,
					output_created,
					ITEM_NAMES,
					RECIPE_LIST,
					INV_FRAMES):
	
	#List of ingredients that can be potentially rearranged into a better location within the roadmap
	rearranged_items = []

	#Determine which steps can be rearranged
	#Evaluate the list in reverse order for easy list manipulation
	#The first and last step won't be changed
	for i in range(len(written_step)-2,0,-1):
		if("(and toss)" in written_step[i]):
			#This item can potentially be relocated to a quicker time
			tossed_item = written_step[i].split(") ")[-1][1:-1]
			rearranged_items.append(tossed_item)
			written_step.pop(i)
			frames_taken.pop(i)
			total_frames.pop(i)
			inventory.pop(i)
			output_created.pop(i)

			#Wipe that the output has been created for the item being rearranged
			for j in range(i,len(written_step)):
				output_created[j][ITEM_NAMES.index(tossed_item)] = False
	
	#Now that all rearranged items have been removed
	#Find The optimal place they can be inserted again, such that they don't affect the inventory
	for i in rearranged_items:
		#Establish a default bound for the optimal place for this item
		record_frames = 9999
		record_placement_index = -1
		record_description = ""

		#Evaluate all recipes and determine the optimal recipe and location
		for recipe in RECIPE_LIST[ITEM_NAMES.index(i)+1]["RECIPES"]:
			for interval in range(0,len(inventory)):
				#Only want recipes where all ingredients are in the last 10 slots of the evaluated inventory
				if(all([ingredient in inventory[interval] for ingredient in recipe])):
					if(all([inventory[interval].index(ingredient) >= 10 for ingredient in recipe])):
						#The very first recipe fulfillment (if we're evaluating there)
						#must take a single ingredient
						if(interval > 0 or len(recipe) == 1):
							#This is a valid recipe and location to fulfill (and toss) this output item
							#Calculate the frames needed to produce this step
							temp_frames = TOSS_FRAMES
							temp_use_desc = ""

							if(len(recipe) == 1):
								#Only one ingredient to navigate to
								temp_frames += INV_FRAMES[20 - inventory[interval].count("BLOCKED")][inventory[interval].index(recipe[0])]
								temp_use_desc = "Use [{0}] in slot {1} ".format(recipe[0],inventory[interval].index(recipe[0])+1)
							else:
								#Two ingredients to navitgate to, but order matters
								#Pick the larger-index number ingredient first, as it will reduce the frames needed to
								#reach the other ingredient
								temp_frames += CHOOSE_2ND_INGREDIENT_FRAMES
								if(inventory[interval].index(recipe[0]) > inventory[interval].index(recipe[1])):
									temp_frames += INV_FRAMES[20 - inventory[interval].count("BLOCKED")][inventory[interval].index(recipe[0])]
									temp_frames += INV_FRAMES[19 - inventory[interval].count("BLOCKED")][inventory[interval].index(recipe[1])]
									temp_use_desc = "Use [{0}] in slot {1} and [{2}] in slot {3} ".format(recipe[0],
																									  	  inventory[interval].index(recipe[0])+1,
																									  	  recipe[1],
																									  	  inventory[interval].index(recipe[1])+1)
								else:
									temp_frames += INV_FRAMES[20 - inventory[interval].count("BLOCKED")][inventory[interval].index(recipe[1])]
									temp_frames += INV_FRAMES[19 - inventory[interval].count("BLOCKED")][inventory[interval].index(recipe[0])]
									temp_use_desc = "Use [{0}] in slot {1} and [{2}] in slot {3} ".format(recipe[1],
																									  	  inventory[interval].index(recipe[1])+1,
																									  	  recipe[0],
																									  	  inventory[interval].index(recipe[0])+1)
							
							#Compare the temp frames to the current record
							if(temp_frames < record_frames):
								#Update the record information
								record_frames = temp_frames
								record_placement_index = interval
								record_description = temp_use_desc + "to make (and toss) <{0}>".format(i)

		#All recipes and intervals have been evaluated
		#Insert the optimized output in the designated interval
		if(record_placement_index != -1):
			written_step.insert  (record_placement_index+1, record_description)
			frames_taken.insert  (record_placement_index+1, record_frames)
			total_frames.insert  (record_placement_index+1, 0)
			inventory.insert     (record_placement_index+1,copy.copy(inventory     [record_placement_index]))
			output_created.insert(record_placement_index+1,copy.copy(output_created[record_placement_index]))

			#Update that the output is now being created in the new location
			for j in range(record_placement_index+1,len(written_step)):
				output_created[j][ITEM_NAMES.index(i)] = True
		else:
			#This is an error
			log(7, "Calculator", "Roadmap", "Optimize", "OptimizeRoadmap couldn't find valid placement of {0}".format(i))
	
	#All items have been rearranged and placed into a new roadmap
	#Re-calculate the total frame count
	for i in range(1,len(written_step)):
		total_frames[i] = total_frames[i-1] + frames_taken[i]

	return total_frames[-1]

#The primary subroutine:
#Search the entire space for possible roadmaps to fulfilling all recipes as quickly as possible
def calculateOrder(callNumber, startingInventory, recipeList, invFrames, current_frame_record):
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

	sorted_alpha_list = getAlphaSort()
	sorted_type_list = getTypeSort()
	
	#How many times a worker is evaluating a new random branch
	total_dives = 0

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

		total_dives += 1
		log(3, "Calculator", "Info", "Call " + str(callNumber),"Searching New Branch #{0}".format(total_dives))

		#If the iteration count exceeds a given threshold,
		#Then reset the entire search space and begin anew
		while(iterationCount < 100000):

			#Check for bad states to immediately retreat from
			#The Thunder Rage must remain in the inventory until the Ch.5 Intermission
			if((not outputCreated[stepIndex][57]) and (not "Thunder Rage" in inventory[stepIndex])):
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
		
				if(totalFrames[stepIndex] < current_frame_record + BUFFER_SEARCH_FRAMES):
					#A finished roadmap has been generated
					#Evaluate the roadmap to determine where moves can be reallocated for quicker access of ingredients
					rearranged_written_step = copy.deepcopy(writtenStep)
					rearranged_frames_taken = copy.deepcopy(framesTaken)
					rearranged_total_frames = copy.deepcopy(totalFrames)
					rearranged_inventory =    copy.deepcopy(inventory)
					rearranged_output_created = copy.deepcopy(outputCreated)

					rearranged_frame_record = OptimizeRoadMap(rearranged_written_step,
															  rearranged_frames_taken,
															  rearranged_total_frames,
															  rearranged_inventory,
															  rearranged_output_created,
															  itemNames,
															  recipeList,
															  invFrames)

					log(3, "Calculator", "OptimizeRoadmap", "Call " + str(callNumber), "Rearranging Saved {0} Frames!".format(totalFrames[stepIndex]-rearranged_frame_record))

					if(rearranged_frame_record < current_frame_record):
						current_frame_record = rearranged_frame_record
						printResults("results/[{0}].txt".format(rearranged_frame_record),rearranged_written_step,rearranged_frames_taken,rearranged_total_frames,rearranged_inventory,rearranged_output_created,itemNames)
						return [rearranged_frame_record, callNumber]
						
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
									useDescription = "Use [{0}] in slot {1} ".format(recipe[0],ingredientLoc+1)
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
										tempFrames += invFrames[viableItems-1][ingredientLoc[1]-ingredientOffset[1]-1]
									else:
										tempFrames += invFrames[viableItems-0][ingredientLoc[1]-ingredientOffset[1]-0]

									#Set this inventory index to null if the item was in the first 10 slots
									if(ingredientLoc[1] < 10):
										tempInventory[ingredientLoc[1]] = "NULL"

									#Describe what items were used
									useDescription = "Use [{0}] in slot {1} and [{2}] in slot {3} ".format(ingredientName[0],
																									       ingredientLoc[0]+1,
																									       ingredientName[1],
																									       ingredientLoc[1]+1)

								#Handle allocation of the OUTPUT variable
								#Options vary by whether there are "NULL"s within the inventory
								try:
									#If there are NULLs in the inventory,
									#All items before the 1st NULL get moved down 1 position									
									for index_eval in range(tempInventory.index("NULL"),0,-1):
										tempInventory[index_eval] = tempInventory[index_eval-1]

									#The vacancy at the start of the inventory is now occupied with the new item
									tempInventory[0] = recipeList[outputItem]["NAME"]

									#Check to see if this state is viable
									if(remainingOutputsCanBeFulfilled(tempInventory, tempOutputsFulfilled, recipeList, itemNames)):
										#This is a viable state that doesn't increase frames at all (Output was auto-placed)
										#Determine where to insert this legal move into the list of legal moves (Sorted by frames taken)
										insertIndex = getInsertionIndex(legalMoves, stepIndex, tempFrames)

										placeDescription = "to make (and auto-place) <{0}>".format(itemNames[outputItem-1])
										legalMoves[stepIndex].insert(insertIndex,[useDescription+placeDescription,outputItem,tempFrames,tempInventory])
								except:
									#There are no NULLs in the inventory. Something must be tossed
									#Total number of frames increased by forcing to toss something
									tempFrames += TOSS_FRAMES
							
									#Evaluate viability of tossing the output item itself
									if(remainingOutputsCanBeFulfilled(tempInventory, tempOutputsFulfilled, recipeList, itemNames)):
										#Temp frames do not increase as the output item is always at the very top of the list
										insertIndex = getInsertionIndex(legalMoves, stepIndex, tempFrames)


										placeDescription = "to make (and toss) <{0}>".format(itemNames[outputItem-1])
										legalMoves[stepIndex].insert(insertIndex,[useDescription+placeDescription,outputItem,tempFrames,tempInventory])

									#Evaluate the viability of tossing all current inventory items
									#Assumed that it is impossible to toss and replace any items in the last 10 positions
									for tossedIndex in range(0,10):
										#Make a copy of the tempInventory with the replaced item
										replacedInventory = copy.copy(tempInventory)
										tossedItemName = tempInventory[tossedIndex]

										#All items before the selected removal item get moved down 1 position									
										for index_eval in range(tossedIndex,0,-1):
											replacedInventory[index_eval] = replacedInventory[index_eval-1]

										#The vacancy at the start of the inventory is now occupied with the new item
										replacedInventory[0] = recipeList[outputItem]["NAME"]

										if(remainingOutputsCanBeFulfilled(replacedInventory, tempOutputsFulfilled, recipeList, itemNames)):
											#Calculate the additional tossed frames. Have to +1 both viableItems and tosseditem as
											#the output is at the top of the list, pushing everything else down one spot
											replacedFrames = tempFrames+invFrames[viableItems+1][tossedIndex+1]
											insertIndex = getInsertionIndex(legalMoves, stepIndex, replacedFrames)
										
											placeDescription = "to make <{0}>, toss [{1}] in slot {2}".format(itemNames[outputItem-1],
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
					viableItems = 20 - (tempInventory.count("BLOCKED") + tempInventory.count("NULL"))

					#If the Mousse Cake is in the first 10 spots, change it to NULL
					#As it is used to acquire the Dried Bouquet (Hot Dog needs to be duped)
					mousse_cake_loc = tempInventory.index("Mousse Cake")
					if(mousse_cake_loc < 10):
						tempInventory[mousse_cake_loc] = "NULL"
						viableItems -= 1

					#Handle allocation of the first 2 Ch.5 Items (Dried Bouquet and Coconut)	
					if(tempInventory.count("NULL") >= 2):
						#The Dried Bouquet gets Auto Placed in the 1st slot...
						#And everything else gets shifted down one to fill the first NULL 
						for index_eval in range(tempInventory.index("NULL"),0,-1):
							tempInventory[index_eval] = tempInventory[index_eval-1]

						#The vacancy at the start of the inventory is now occupied with the new item
						tempInventory[0] = "Dried Bouquet"
						tempindexDB = 1	
						viableItems += 1					

						#The Coconut gets Auto Placed in the 1st slot...
						#And everything else gets shifted down one to fill the first NULL 
						for index_eval in range(tempInventory.index("NULL"),0,-1):
							tempInventory[index_eval] = tempInventory[index_eval-1]

						#The vacancy at the start of the inventory is now occupied with the new item
						tempInventory[0] = "Coconut"
						tempindexCO = 1
						viableItems += 1

						#Auto Placing takes zero frames
						temp_frames_DB = 0
						temp_frames_CO = 0
						
						#Handle the Allocation of the Coconut Sort, Keel Mango, and Courage Shell
						handleChapter5Eval(legalMoves,
										   stepIndex,
										   tempInventory,
										   tempOutputsFulfilled,
										   recipeList,
										   itemNames,
										   invFrames,
										   temp_frames_DB,
										   temp_frames_CO,
										   0, #DB was auto-placed in the 1st index
										   0, #CO was auto-placed in the 1st index
										   sorted_alpha_list,
										   sorted_type_list)

					elif(tempInventory.count("NULL") == 1):
						#The Dried Bouquet gets Auto Placed in the 1st slot...
						#And everything else gets shifted down one to fill the first NULL 
						for index_eval in range(tempInventory.index("NULL"),0,-1):
							tempInventory[index_eval] = tempInventory[index_eval-1]

						#The vacancy at the start of the inventory is now occupied with the new item
						tempInventory[0] = "Dried Bouquet"
						tempindexDB = 0
						viableItems += 1

						#Auto Placing takes zero frames
						temp_frames_DB = 0

						#The Coconut can only be placed in first 10 slots
						#Dried Bouquet will always be in the first slot
						for tempindexCO in range(1,10):
							#Don't waste time replacing the Dried Bouquet or Thunder Rage with the Coconut
							if(tempInventory[tempindexCO] != "Thunder Rage"):
								#Replace the item with the Coconut
								#All items above the replaced item float down one space
								#and the Coconut is always placed in slot 1 
								co_temp_inventory = copy.copy(tempInventory)
								for index_eval in range(tempindexCO,0,-1):
									co_temp_inventory[index_eval] = co_temp_inventory[index_eval-1]
								
								co_temp_inventory[0] = "Coconut"

								#Calculate the number of frames needed to pick this slot for replacement
								temp_frames_CO = TOSS_FRAMES + invFrames[viableItems][tempindexCO]

								#Handle the Allocation of the Coconut Sort, Keel Mango, and Courage Shell
								handleChapter5Eval(legalMoves,
								                   stepIndex,
												   co_temp_inventory,
												   tempOutputsFulfilled,
												   recipeList,
												   itemNames,
												   invFrames,
												   temp_frames_DB,
												   temp_frames_CO,
												   0, #DB was auto-placed in the 1st index
												   tempindexCO, #CO was manually placed
												   sorted_alpha_list,
												   sorted_type_list)
					else:
						#No NULLs to utilize for Chapter 5 Intermission
						#Both the DB and CO can only replace items in the first 10 slots
						#The remaining items always slide down to fill the vacanacy
						#The DB will eventually end up in Slot #2 and
						#The CO will eventually end up in Slot #1
						for tempindexDB in range(0,10):
							for tempindexCO in range(tempindexDB+1,10):
								#Replace the 1st chosen item with the DB
								dbco_temp_inventory = copy.copy(tempInventory)
								for index_eval in range(tempindexDB,0,-1):
									dbco_temp_inventory[index_eval] = dbco_temp_inventory[index_eval-1]
								
								dbco_temp_inventory[0] = "Coconut"

								#Replace the 2nd chosen item with the CO
								for index_eval in range(tempindexCO,0,-1):
									dbco_temp_inventory[index_eval] = dbco_temp_inventory[index_eval-1]
								
								dbco_temp_inventory[0] = "Coconut"

								#Calculate the frames of these actions
								temp_frames_DB = TOSS_FRAMES + invFrames[viableItems][tempindexDB]
								temp_frames_CO = TOSS_FRAMES + invFrames[viableItems][tempindexCO]
								
								#Only evaluate the remainder of the Ch.5 Intermission if the
								#Thunder Rage is still present in the inventory
								if(dbco_temp_inventory.count("Thunder Rage") >= 1):
									#Handle the Allocation of the Coconut Sort, Keel Mango, and Courage Shell
									handleChapter5Eval(legalMoves,
									                   stepIndex,
													   dbco_temp_inventory,
													   tempOutputsFulfilled,
													   recipeList,
													   itemNames,
													   invFrames,
													   temp_frames_DB,
													   temp_frames_CO,
													   tempindexDB, #DB was manually placed
													   tempindexCO, #CO was manually placed
													   sorted_alpha_list,
													   sorted_type_list)
				
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
						alpha_inventory = getSortedInventory(inventory[stepIndex], sorted_alpha_list, False)

						#Only add the legal move if the sort actually changes the inventory
						if(alpha_inventory != inventory[stepIndex]):
							tempindex = 0
							while(tempindex < len(legalMoves[stepIndex]) and legalMoves[stepIndex][tempindex][2] < ALPHA_SORT_FRAMES):
								tempindex += 1

							description = "Sort - Alphabetical"
							#legalMoves[stepIndex].insert(tempindex,[description,-1,alphaSortFrames,alphainventory])
							legalMoves[stepIndex].append([description,-1,ALPHA_SORT_FRAMES,alpha_inventory])

						#Reverse Alphabetical Sort
						reverse_alpha_inventory = getSortedInventory(inventory[stepIndex], sorted_alpha_list, True)

						#Only add the legal move if the sort actually changes the inventory
						if(reverse_alpha_inventory != inventory[stepIndex]):
							tempindex = 0
							while(tempindex < len(legalMoves[stepIndex]) and legalMoves[stepIndex][tempindex][2] < REVERSE_ALPHA_SORT_FRAMES):
								tempindex += 1

							description = "Sort - Reverse Alphabetical"
							#legalMoves[stepIndex].insert(tempindex,[description,-1,reversAlphaSortFrames,reversealphainventory])
							legalMoves[stepIndex].append([description,-1,REVERSE_ALPHA_SORT_FRAMES,reverse_alpha_inventory])

						#Type Sort
						type_inventory = getSortedInventory(inventory[stepIndex], sorted_type_list, False)

						#Only add the legal move if the sort actually changes the inventory
						if(type_inventory != inventory[stepIndex]):
							tempindex = 0
							while(tempindex < len(legalMoves[stepIndex]) and legalMoves[stepIndex][tempindex][2] < TYPE_SORT_FRAMES):
								tempindex += 1

							description = "Sort - Type"
							#legalMoves[stepIndex].insert(tempindex,[description,-1,typeSortFrames,typeinventory])
							legalMoves[stepIndex].append([description,-1,TYPE_SORT_FRAMES,type_inventory])

						#Reverse Type Sort
						reverse_type_inventory = getSortedInventory(inventory[stepIndex], sorted_type_list, True)

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
				legalMoves[stepIndex] = list(filter(lambda x: x[2]+totalFrames[stepIndex] < (current_frame_record + BUFFER_SEARCH_FRAMES), legalMoves[stepIndex]))
			
				#Filter out all legal moves that use 2 ingredients in the very first legal move
				if(stepIndex == 0):
					legalMoves[stepIndex] = list(filter(lambda x: not " and " in x[0], legalMoves[stepIndex]))

				#Somewhat Random process of picking the quicker moves to recurse down
				#Arbitrarilty remove the first listed move with a given probability
				if(select) :
					total_moves = len(legalMoves[stepIndex])
					while(total_moves > 1 and random.random() < 0.5):
						total_moves = len(legalMoves[stepIndex])
						legalMoves[stepIndex].pop(0)

				#When not doing the "Select" methodology, and opting for Randomize
				#Just shuffle the entire list of legal moves and pick the new first item
				elif(randomise):
					random.shuffle(legalMoves[stepIndex])

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
				legalMoves[stepIndex] = list(filter(lambda x: x[2]+totalFrames[stepIndex] < (current_frame_record + BUFFER_SEARCH_FRAMES), legalMoves[stepIndex]))

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
					iterationCount += 1
					if(iterationCount % 1000 == 0):
						log(6, "Calculator", "Info", "Call " + str(callNumber), "{0} Steps taken currently, {1} frames accumulated so far; {2}k iterations".format(stepIndex, totalFrames[stepIndex], iterationCount / 1000))

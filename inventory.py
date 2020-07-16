import copy
import os
import math
from logger import log
from recipes import getRecipeList

#recipeList = getRecipeList()
#itemNames = []
#Fill the itemNames
#for item in recipeList:
#	itemNames.append(recipeList[item]["NAME"])
#	log(7, "Inventory", "Items", "Scan", recipeList[item]["NAME"] + " scanned.")
#log(5, "Inventory", "Items", "Scan", "All item names scanned successfully.")

def getAlphaSort():
	file = open(os.getcwd() + "/itemSorts/alphabetic.txt","r")
	log(2, "Inventory", "Sort", "Load", "Sort list loaded from file.")
	sortList = []
	for line in file:
		sortList.append(line.strip("\n"))
		log(7, "Inventory", "Sort", "Load", line.strip("\n") + " added to sort list")
	log(2, "Inventory", "Sort", "Load", "Finished creating sort list.")
	log(5, "Inventory", "Sort", "Load", str(sortList))
	file.close()
	return sortList

def getTypeSort():
	file = open(os.getcwd() + "/itemSorts/type.txt","r")
	log(2, "Inventory", "Sort", "Load", "Sort list loaded from file.")
	sortList = []
	for line in file:
		sortList.append(line.strip("\n"))
		log(7, "Inventory", "Sort", "Load", line.strip("\n") + " added to sort list")
	log(2, "Inventory", "Sort", "Load", "Finished creating sort list.")
	log(5, "Inventory", "Sort", "Load", str(sortList))
	file.close()
	return sortList

def getStartingInventory():
	file = open(os.getcwd() + "/inventory.txt","r")
	log(2, "Inventory", "Init", "Load", "Starting inventory file loaded.")
	inventory = []
	for line in file:
		inventory.append(line.strip("\n"))
		log(7, "Inventory", "Init", "Load", line.strip("\n") + " added to inventory")
	log(2, "Inventory", "Init", "Load", "Finished setting up starting inventory")
	log(5, "Inventory", "Init", "Load", str(inventory))
	file.close
	return inventory

def getInventoryFrames():
	invFrames = [[]]
	for i in range(21):
		# if(i == 0):
		# 	invFrames.append([0])
		# else:
			frames = []
			frameList = [0,0,2,4,6,8,10,12,14,16,18]
			for j in range(i+1):
				if(j < i+1-j):
					frames.append(frameList[j])
				else:
					frames.append(frameList[i-j+1])
			invFrames.append(frames)
			log(7, "Inventory", "Frames", "Generate", "Frame " + str(frames) + " added to invFrames")
	log(2, "Inventory", "Frames", "Generate", "Inventory Frames Generated")
	log(5, "Inventory", "Frames", "Generate", str(invFrames))
	return invFrames

def checkRecipe(recipe, inventoryLocal, outputCreated, recipeList, itemNames):
	#Determine if the recipe items can still be fulfilled
	for item in recipe:
		#Check if we already have the item
		if item in inventoryLocal:
			pass
		#Check if it can be made but hasn't been
		elif item in itemNames and not outputCreated[itemNames.index(item)]:
			for newRecipe in recipeList[itemNames.index(item)+1]["RECIPES"]:
				#Recurse on all recipes that can make this item
				tempOutputCreated = copy.copy(outputCreated)
				tempOutputCreated[itemNames.index(item)] = True
				if checkRecipe(newRecipe, inventoryLocal, tempOutputCreated,
							   recipeList, itemNames):
					break
			#The item cannot be produced with the current inventory
			else:
				return False
		else:
			#The item cannot be made or was thrown out
			return False
	#All items in the recipe are able to be made
	return True

def remainingOutputsCanBeFulfilled(inventoryLocal, outputCreated, recipeList,
								   itemNames):
	#With the given inventory, can the remaining recipes be fulfilled?
	#If Chapter 5 has not been done, add the items it gives us
	inventoryLocal = (inventoryLocal + ["Keel Mango", "Coconut",
										"Dried Bouquet", "Courage Shell"]
					  if not outputCreated[57] else inventoryLocal)
	#Iterate through all output items that haven't been created
	for outputItem in recipeList:
		if(not outputCreated[outputItem-1]):
			#Check if any recipe to make the item can be fulfilled
			for recipe in recipeList[outputItem]["RECIPES"]:
			#This is done to avoid infinite recursion
			#TODO: Check if there's a more efficient algorithm
				tempOutputCreated = copy.copy(outputCreated)
				tempOutputCreated[outputItem-1] = True
				if checkRecipe(recipe, inventoryLocal, tempOutputCreated,
							   recipeList, itemNames):
					break
			else:
				return False
	#All remaining outputs can still be fulfilled
	return True

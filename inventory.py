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

def checkRecipe(recipe, makeableItems, outputCreated, dependentIndices,
				recipeList, itemNames):
	#Determine if the recipe items can still be fulfilled
	for itemName in recipe:
		#Check if we already have the item or know we can make it
		if itemName in makeableItems:
			continue
		try:
			#Throws if item cannot ever be made
			itemIndex = itemNames.index(itemName)
			#Check if it hasn't been made and doesn't depend on any item
			#it is needed to make
			if not (outputCreated[itemIndex] or itemIndex in dependentIndices):
				#Anything made for this item cannot depend on it
				newDependentIndices = dependentIndices + [itemIndex]
				#Recurse on all recipes that can make this item
				for newRecipe in recipeList[itemIndex+1]["RECIPES"]:
					if checkRecipe(newRecipe, makeableItems, outputCreated,
								   newDependentIndices, recipeList, itemNames):
						#Stop looking for recipes to make the item
						makeableItems.add(itemName)
						break
				#The item cannot be produced with the current inventory
				else:
					return False
				#The item was able to be made
				continue
			#The item cannot be produced due to the current history
			return False
		#The item cannot ever be created
		except ValueError:
			return False
	#All items in the recipe are able to be made
	return True

def remainingOutputsCanBeFulfilled(inventoryLocal, outputCreated, recipeList,
								   itemNames):
	#With the given inventory, can the remaining recipes be fulfilled?
	makeableItems = set(inventoryLocal)
	#If Chapter 5 has not been done, add the items it gives us
	if not outputCreated[57]:
		makeableItems.update(["Keel Mango", "Coconut", "Dried Bouquet",
							  "Courage Shell"])
	#Iterate through all output items that haven't been created
	for outputItem in recipeList:
		if(not outputCreated[outputItem-1]):
			#List of items to not try to make
			dependentIndices = [outputItem-1]
			#Check if any recipe to make the item can be fulfilled
			for recipe in recipeList[outputItem]["RECIPES"]:
				if checkRecipe(recipe, makeableItems, outputCreated,
							   dependentIndices, recipeList, itemNames):
					#Stop looking for recipes to make the item
					makeableItems.add(itemNames[outputItem-1])
					break
			#The item cannot be produced
			else:
				return False
	#All remaining outputs can still be fulfilled
	return True

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
	file = open(os.getcwd() + "/itemSorts/alphabetic_sort-JP.txt","r")
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
	file = open(os.getcwd() + "/itemSorts/type_sort-JP.txt","r")
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

def checkIngredients(recipe, inventoryLocal, outputCreated, recipeList, itemNames, level=0):
	#With the given inventory and knolwedge of which outputs have already been created,
	#Determine if the given recipe can be fulfilled
	for item in recipe:
		if item in inventoryLocal:
			#This item is in the current inventory, do nothing for now
			pass
		elif item in itemNames and(not outputCreated[itemNames.index(item)]):
			#This item is not in the current inventory, but it is another output item that hasn't been made yet
			#Check all recipes of the output item to see if it can be made with the current inventory.
			if(level < 3):
				#Don't evaluate any further than the 3rd recursion level
				#Done to avoid infinite recipe loops (Inky Sauce > Shroom Broth > Poison Shroom > Inky Sauce > ...)
				tempGoodRecipe = False
				for newRecipe in recipeList[itemNames.index(item)+1]["RECIPES"]:
					#Check to see if this ingredient can be made with other ingredients the player has
					if(checkIngredients(newRecipe, inventoryLocal, outputCreated, recipeList, itemNames, level + 1)):
						#At least one recipe can be fulfilled now.
						tempGoodRecipe = True
					#log(7, "Inventory", "Recipe", "Check", "Recipe " + str(newRecipe) + " has been evaluated.")
				#After evaluating all recipes of the item, if that item cannot be produced, return false
				if(not tempGoodRecipe):
					#log(7, "Inventory", "Recipe", "Check", str(item) + " can't be produced with current inventory.")
					return False
			else:
				return False
		else:
			#The item isn't in the inventory, and can't be made through another recipe, return False
			return False
	#By getting here, we know all ingredients are at least possible to create still with the current inventory
	#log(5, "inventory", "Recipe", "Check", "It is still possible to make all the ingredients with the current inventory")
	return True

def checkIngredients(recipe, inventoryLocal, outputCreated, recipeList, itemNames):
 	#With the given inventory, determine if the remaining output items be fulfilled
 	for item in recipe:
 		if item in inventoryLocal:
 			#This item is in the current inventory, do nothing for now
 			pass
 		elif item in itemNames and(not outputCreated[itemNames.index(item)]):
 			tempGoodRecipe = False
 			for newRecipe in recipeList[itemNames.index(item)+1]["RECIPES"]:
 				#Recurse on all recipes that can make this item
 				tempOutputCreated = copy.copy(outputCreated)
 				tempOutputCreated[itemNames.index(item)] = True
 				tempGoodRecipe = tempGoodRecipe or checkIngredients(newRecipe, inventoryLocal, tempOutputCreated, recipeList, itemNames)
 				#log(7, "Inventory", "Recipe", "Check", str(newRecipe) + " has been evaluated.")
 			#After evaluating all recipes of the item, if that item cannot be produced, return false
 			if(not tempGoodRecipe):
 				#log(7, "Inventory", "Recipe", "Check", str(item) + " can't be produced with current inventory.")
 				return False
 		else:
 			#The item isn't in the inventory, and can't be made through another recipe, return False
 			return False
 	#By getting here, we know all items are at least possible to create still with the current inventory
 	#log(7, "inventory", "Recipe", "Check", "It is still possible to make all the items with the current inventory")
 	return True

def remainingOutputsCanBeFulfilled(inventoryLocal, outputCreated, recipeList, itemNames):
	#With the given inventory, can the remaining recipes be fulfilled?
	#Iterate through all remaining output items
	for outputItem in recipeList:
		#Only want output items that haven't already been created elsewhere
		if(not outputCreated[outputItem-1]):
			#Iterate through all recipes
			viableIngredientsFound = False
			for recipe in recipeList[outputItem]["RECIPES"]:
			#This is done to avoid infinite recursion
			#TODO: Check if there's a more efficient algorithm
				tempOutputCreated = copy.copy(outputCreated)
				tempOutputCreated[outputItem-1] = True
				viableIngredientsFound = viableIngredientsFound or checkIngredients(recipe, inventoryLocal, tempOutputCreated, recipeList, itemNames)
			if(not viableIngredientsFound):
				#There's a few exceptions
				if(outputCreated[57]):
					#the 58th "output" is really a representation of the Chapter 5 Intermission
					#Where the Keel Mango and Coconut are collected, so a few recipes before this intermission won't be viable
					#If chapter 5 has been done, then there's no exceptions anymore
					return False
				elif(recipeList[outputItem]["NAME"] in ["Zess Dinner", "Koopa Bun", "Fruit Parfait", "Mango Delight", "Love Pudding", "Fresh Juice", "Coco Candy", "Courage Meal", "Coconut Bomb", "Zess Dynamite"]):
					#This has flaws, but any items that need Keel Mangos or Coconuts
					#will be considered fine for pre-Chapter-5 evaluation
					pass
				else:
					#Any other output items will need something that we *should* have
					return False
		#log(7, "Inventory", "Recipe", "Check", str(recipeList[outputItem]["NAME"]) + " has been evaluated.")
	#haven't returned False in evaluating all output items
	#Meaning that all remeining outputs can still be fulfilled!
	#log(7, "Inventory", "Recipe", "Check", "All remaining output items can be fulfilled")
	return True

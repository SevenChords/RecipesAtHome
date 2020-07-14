import os
from logger import log

def getRecipeList():
	#load recipes file into single string
	file = open(os.getcwd() + "/recipes-JP.txt","r")
	recipeList = {}
	rawData = ""
	for line in file:
		rawData = rawData + line
		log(7, "Recipe", "Data", "Load", "Line " + line.strip("\n") + " added to raw data.")
	log(2, "Recipes", "Data", "Load", "Finished reading file.")
	log(5, "Recipes", "Data", "Load", str(rawData))
	file.close()
	#split into array with 58 recipes
	recipeData = rawData.split("\n===\n")
	log(2, "Recipes", "Data", "Split", "Splitting into individual Recipes done.")
	log(5, "Recipes", "Data", "Split", str(recipeData))
	#split recipes into NAME and RECIPES entry
	for i in range(len(recipeData)):
		recipeData[i] = recipeData[i].split("\n---\n")
		log(7, "Recipe", "Data", "Load", "Recipe " + str(recipeData[i]) + "loaded.")
	log(2, "Recipes", "Data", "Split", "Splitting recipes into \"NAME\" and \"RECIPES\" done.")
	log(5, "Recipes", "Data", "Split", str(recipeData))
	#split RECIPES entry into individual recipes
	for i in range(len(recipeData)):
		recipeData[i][1] = recipeData[i][1].split("\n")
		log(7, "Recipe", "Data", "Load", "Possible recipe " + str(recipeData[i][1]) + "registered.")
	log(2, "Recipes", "Data", "Split", "Splitting \"RECIPES\" into all possible recipes done.")
	log(5, "Recipes", "Data", "Split", str(recipeData))
	#split recipes into individual ingredients
	for i in range(len(recipeData)):
		for j in range(len(recipeData[i][1])):
			recipeData[i][1][j] = recipeData[i][1][j].split(", ")
			log(7, "Recipe", "Data", "Load", "Ingredient " + str(recipeData[i][1][j]) + " registered.")
	log(2, "Recipes", "Data", "Split", "Splitting recipes into individual ingredients done.")
	log(5, "Recipes", "Data", "Split", str(recipeData))
	recipeList = {}
	#store everything in a single dictionary for all recipes
	for i in range(len(recipeData)):
		toAdd = {}
		toAdd["NAME"] = recipeData[i][0]
		toAdd["RECIPES"] = recipeData[i][1]
		recipeKey = i + 1
		recipeList[recipeKey] = toAdd
		log(7, "Recipes", "Data", "Merge", "Recipe " + str(toAdd) + " added to dictionary.")
	log(2, "Recipes", "Data", "Merge", "Recipes merged into recipeList dictionary.")
	log(5, "Recipes", "Data", "Merge", str(recipeList))
	#return dictionary
	return recipeList

#initLogging(2)
#getRecipeList()
#mmLogFileObject.close()
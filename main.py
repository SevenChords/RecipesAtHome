from multiprocessing import Pool
import copy
import random

print('import done')

def roadmap(call_number, frame_record):
	ITEMS = {
		1: {"NAME":"Shroom Fry",
			"RECIPES":[["Dried Shroom"],
					   ["Mushroom"],
					   ["Poison Shroom"],
					   ["Super Shroom"],
					   ["Volt Shroom"],
					   #["Dried Shroom","Fire Flower"], #Trivial Improvement Exists
					   #["Dried Shroom","Volt Shroom"], #Trivial Improvement Exists
					   #["Mushroom","Dried Shroom"],	#Trivial Improvement Exists
					   #["Mushroom","Turtley Leaf"],	#Trivial Improvement Exists
					   #["Mushroom","Golden Leaf"],		#Trivial Improvement Exists
					   ],
		   },
		2: {"NAME":"Shroom Roast",
			"RECIPES":[["Slow Shroom"],
					   ["Life Shroom"],
					   #["Life Shroom","Volt Shroom"],	 #Trivial Improvement Exists
					   #["Mushroom","Fire Flower"],		 #Unnecessary 2 Ingredients
					   #["Mushroom","Super Shroom"],	 #Unnecessary 2 Ingredients
					   #["Mushroom","Volt Shroom"],		 #Unnecessary 2 Ingredients
					   #["Super Shroom","Dried Shroom"], #Unnecessary 2 Ingredients
					   #["Super Shroom","Volt Shroom"],	 #Unnecessary 2 Ingredients
					   #["Super Shroom","Turtley Leaf"], #Unnecessary 2 Ingredients
					   #["Super Shroom","Golden Leaf"],	 #Unnecessary 2 Ingredients
					   ],
			},
		3: {"NAME":"Shroom Steak",
			"RECIPES":[["Ultra Shroom"],
					   #["Life Shroom","Dried Shroom"], #Unnecessary 2 Ingredients
					   #["Life Shroom","Mushroom"],		#Unnecessary 2 Ingredients
					   #["Life Shroom","Super Shroom"], #Unnecessary 2 Ingredients
					   #["Life Shroom","Ultra Shroom"], #Trivial Improvement Exists
					   #["Life Shroom","Turtley Leaf"], #Unnecessary 2 Ingredients
					   #["Life Shroom","Golden Leaf"],	#Unnecessary 2 Ingredients
					   #["Ultra Shroom","Dried Shroom"],#Trivial Improvement Exists
					   #["Ultra Shroom","Mushroom"],	#Trivial Improvement Exists
					   #["Ultra Shroom","Super Shroom"],#Trivial Improvement Exists
					   #["Ultra Shroom","Volt Shroom"], #Trivial Improvement Exists
					   #["Ultra Shroom","Turtley Leaf"],#Trivial Improvement Exists
					   #["Ultra Shroom","Golden Leaf"], #Trivial Improvement Exists
					   ],
			},
		4: {"NAME":"Honey Shroom",
			"RECIPES":[["Mystery"],
					   #["Mushroom","Honey Syrup"],		#Unnecessary 2 Ingredients
					   #["Slow Shroom","Honey Syrup"],	#Unnecessary 2 Ingredients
					   #["Volt Shroom","Honey Syrup"],	#Unnecessary 2 Ingredients
					   ],
			},
		5: {"NAME":"Maple Shroom",
			"RECIPES":[["Mushroom","Maple Syrup"],
					   ["Volt Shroom","Maple Syrup"]],
			},
		6: {"NAME":"Jelly Shroom",
			"RECIPES":[["Mushroom","Jammin Jelly"],
					   ["Volt Shroom","Jammin Jelly"]],
			},
		7: {"NAME":"Honey Super",
			"RECIPES":[["Life Shroom","Honey Syrup"],
					   ["Super Shroom", "Honey Syrup"]],
			},
		8: {"NAME":"Maple Super",
			"RECIPES":[["Super Shroom","Maple Syrup"]],
			},
		9: {"NAME":"Jelly Super",
			"RECIPES":[["Life Shroom","Jammin Jelly"],
					   ["Super Shroom","Jammin Jelly"]],
			},
		10: {"NAME":"Honey Ultra",
			 "RECIPES":[["Ultra Shroom","Honey Syrup"]],
			 },
		11: {"NAME":"Maple Ultra",
			 "RECIPES":[["Ultra Shroom","Maple Syrup"]],
			 },
		12: {"NAME":"Jelly Ultra",
			 "RECIPES":[["Ultra Shroom","Jammin Jelly"]],
			 },
		13: {"NAME":"Zess Dinner",
			 "RECIPES":[["Mystery"],
						#["Mushroom","Horsetail"],			#Unnecessary 2 Ingredients
						#["Super Shroom","Fire Flower"],	#Unnecessary 2 Ingredients
						#["Super Shroom","Horsetail"],		#Unnecessary 2 Ingredients
						#["Super Shroom","Gradual Syrup"],	#Unnecessary 2 Ingredients
						#["Super Shroom","Keel Mango"],		#Unnecessary 2 Ingredients
						#["Super Shroom","Peachy Peach"],	#Unnecessary 2 Ingredients
						#["Ultra Shroom","Keel Mango"],		#Unnecessary 2 Ingredients
						#["Life Shroom","Fire Flower"],		#Unnecessary 2 Ingredients
						#["Life Shroom","Gradual Syrup"],	#Unnecessary 2 Ingredients
						#["Life Shroom","Horsetail"],		#Unnecessary 2 Ingredients
						#["Fresh Pasta","Mystic Egg"],		#Unnecessary 2 Ingredients
						#["Fresh Pasta","Coconut"],			#Unnecessary 2 Ingredients
						#["Fresh Pasta","Healthy Salad"],	#Unnecessary 2 Ingredients
						#["Healthy Salad","Shroom Fry"],	#Unnecessary 2 Ingredients
						#["Healthy Salad","Koopasta"],		#Unnecessary 2 Ingredients
						#["Healthy Salad","Spaghetti"],		#Unnecessary 2 Ingredients
						#["Spicy Pasta","Coconut"],			#Unnecessary 2 Ingredients
						#["Meteor Meal","Fruit Partaif"]	#Unnecessary 2 Ingredients
						],
			 },
		14: {"NAME":"Zess Special",
			 "RECIPES":[
						#["Whacka Bump"],					#Whacka Bump is never used in evaluation
						#["Fresh Pasta","Dried Shroom"],	#Fresh Pasta is never used in evaluation
						#["Fresh Pasta","Life Shroom"],		#Fresh Pasta is never used in evaluation
						#["Fresh Pasta","Mushroom"],		#Fresh Pasta is never used in evaluation
						#["Fresh Pasta","Super Shroom"],	#Fresh Pasta is never used in evaluation
						["Ultra Shroom","Fire Flower"],
						["Ultra Shroom","Peachy Peach"],
						#["Ultra Shroom","Gradual Syrup"],	#Gradual Syrup is never used in evaluation
						#["Ultra Shroom","Horsetail"],		#Horsetail is never used in evaluation
						["Healthy Salad","Ink Pasta"],
						["Healthy Salad","Shroom Roast"],
						["Healthy Salad","Spicy Pasta"]
						],
			 },
		15: {"NAME":"Zess Deluxe",
			 "RECIPES":[["Shroom Steak","Healthy Salad"],
						#["Ultra Shroom","Fresh Pasta"],	#Fresh Pasta is never used in evaluation
						#["Whacka Bump","Golden Leaf"],		#Whacka Bump is never used in evaluation
						],
			 },
		16: {"NAME":"Spaghetti",
			 "RECIPES":[["Mystery"],
						#["Fresh Pasta"],	#Fresh Pasta is never used in evaluation
						],
			 },
		17: {"NAME":"Koopasta",
			 "RECIPES":[["Mystery"],
						#["Fresh Pasta","Turtley Leaf"],	#Fresh Pasta is never used in evaluation
						#["Spaghetti","Turtley Leaf"],		#Unnecessary 2 Ingredients
						]
			 },
		18: {"NAME":"Spicy Pasta",
			 "RECIPES":[
						#["Hot Sauce","Fresh Pasta"],	#Fresh Pasta is never used in evaluation
						["Hot Sauce","Spaghetti"],
						["Hot Sauce","Koopasta"],
						],
			 },
		19: {"NAME":"Ink Pasta",
			 "RECIPES":[
						#["Inky Sauce","Fresh Pasta"],	#Fresh Pasta is never used in evaluation
						["Inky Sauce","Koopasta"],
						["Inky Sauce","Spaghetti"],
						["Inky Sauce","Spicy Pasta"]],
			 },
		20: {"NAME":"Spicy Soup",
			 "RECIPES":[["Mystery"],
						["Fire Flower"],
						#["Horsetail"],						#Horsetail is never used in evaluation
						["Snow Bunny"],
						#["Fire Flower","Hot Sauce"],		#Trivial Improvement Exists
						#["Fire Flower","Dried Bouquet"],	#Trivial Improvement Exists
						]
			 },
		21: {"NAME":"Fried Egg",
			 "RECIPES":[["Mystery"],
						["Mystic Egg"],
						],
			 },
		22: {"NAME":"Omelette Meal",
			 "RECIPES":[
						#["Mystic Egg","Horsetail"],	#Horsetail is never used in evaluation
						["Mystic Egg","Mushroom"],
						["Mystic Egg","Super Shroom"],
						["Mystic Egg","Life Shroom"],
						["Mystic Egg","Ultra Shroom"],
						],
			 },
		23: {"NAME":"Koopa Bun",
			 "RECIPES":[["Keel Mango","Turtley Leaf"],
						],
			 },
		24: {"NAME":"Healthy Salad",
			 "RECIPES":[["Turtley Leaf","Golden Leaf"],
						#["Turtley Leaf","Horsetail"],	#Horsetail is never used in evaluation
						],
			 },
		25: {"NAME":"Meteor Meal",
			 "RECIPES":[["Shroom Fry","Shooting Star"],
						["Shroom Roast","Shooting Star"],
						["Shroom Steak","Shooting Star"]],
			 },
		26: {"NAME":"Couples Cake",
			 "RECIPES":[["Snow Bunny","Spicy Soup"]],
			 },
		27: {"NAME":"Mousse Cake",
			 "RECIPES":[["Cake Mix"]],
			 },
		28: {"NAME":"Shroom Cake",
			 "RECIPES":[["Mushroom","Cake Mix"],
						["Super Shroom","Cake Mix"],
						["Life Shroom","Cake Mix"]],
			 },
		29: {"NAME":"Choco Cake",
			 "RECIPES":[["Cake Mix","Inky Sauce"],
						["Mousse Cake","Inky Sauce"]],
			 },
		30: {"NAME":"Heartful Cake",
			 "RECIPES":[["Cake Mix","Ruin Powder"],
						["Peachy Peach","Ruin Powder"]],
			 },
		31: {"NAME":"Fruit Parfait",
			 "RECIPES":[
						#["Keel Mango","Gradual Syrup"],	#Gradual Syrup is never used in evaluation
						["Keel Mango","Honey Syrup"],
						["Keel Mango","Jammin Jelly"],
						["Keel Mango","Maple Syrup"],
						["Keel Mango","Peachy Peach"],
						["Peachy Peach","Honey Syrup"],
						["Peachy Peach","Jammin Jelly"],
						["Peachy Peach","Maple Syrup"]],
			 },
		32: {"NAME":"Mango Delight",
			 "RECIPES":[["Keel Mango","Cake Mix"]],
			 },
		33: {"NAME":"Love Pudding",
			 "RECIPES":[["Mystic Egg","Mango Delight"]],
			 },
		34: {"NAME":"Zess Cookie",
			 "RECIPES":[["Mystery"],
						#["Cake Mix","Gradual Syrup"],	#Unnecessary 2 Ingredients
						#["Cake Mix","Maple Syrup"],	#Unnecessary 2 Ingredients
						#["Cake Mix","Mystic Egg"],		#Unnecessary 2 Ingredients
						],
			 },
		35: {"NAME":"Shroom Crepe",
			 "RECIPES":[["Ultra Shroom","Cake Mix"]],
			 },
		36: {"NAME":"Peach Tart",
			 "RECIPES":[["Peachy Peach","Cake Mix"]],
			 },
		37: {"NAME":"Koopa Tea",
			 "RECIPES":[["Mystery"],
						["Turtley Leaf"]],
			 },
		38: {"NAME":"Zess Tea",
			 "RECIPES":[["Mystery"],
						["Golden Leaf"],
						#["Maple Syrup","Jammin Jelly"],	#Unnecessary 2 Ingredients
						],
			 },
		39: {"NAME":"Shroom Broth",
			 "RECIPES":[["Golden Leaf","Poison Shroom"],
						["Golden Leaf","Slow Shroom"]],
			 },
		40: {"NAME":"Fresh Juice",
			 "RECIPES":[["Mystery"],
						#["Gradual Syrup"],					#Gradual Syrup is never used in evaluation
						["Honey Syrup"],
						["Jammin Jelly"],
						["Keel Mango"],
						["Maple Syrup"],
						["Peachy Peach"],
						#["Coconut","Keel Mango"],			#Unnecessary 2 Ingredients
						#["Coconut","Peachy Peach"],		#Unnecessary 2 Ingredients
						#["Coconut","Turtley Leaf"],		#Unnecessary 2 Ingredients
						#["Gradual Syrup","Turtley Leaf"],	#Unnecessary 2 Ingredients
						#["Gradual Syrup","Honey Syrup"],	#Unnecessary 2 Ingredients
						#["Honey Syrup","Jammin Jelly"],	#Unnecessary 2 Ingredients
						#["Honey Syrup","Maple Syrup"],		#Unnecessary 2 Ingredients
						#["Honey Syrup","Turtley Leaf"],	#Unnecessary 2 Ingredients
						#["Jammin Jelly","Gradual Syrup"],	#Unnecessary 2 Ingredients
						#["Jammin Jelly","Turtley Leaf"],	#Unnecessary 2 Ingredients
						#["Maple Syrup","Gradual Syrup"],	#Unnecessary 2 Ingredients
						#["Maple Syrup","Turtley Leaf"],	#Unnecessary 2 Ingredients
						],
			 },
		41: {"NAME":"Inky Sauce",
			 "RECIPES":[["Hot Sauce","Fresh Juice"],
						["Hot Sauce","Koopa Tea"],
						#["Hot Sauce","Shroom Broth"], #Infinite recipe recursion Inky Sauce ==> Shroom Broth ==> Poison Shroom ==> Inky Sauce...
						["Hot Sauce","Turtley Leaf"],
						["Hot Sauce","Zess Tea"],
						["Hot Sauce","Tasty Tonic"]],
			 },
		42: {"NAME":"Icicle Pop",
			 "RECIPES":[["Honey Syrup","Ice Storm"]],
			 },
		43: {"NAME":"Zess Frappe",
			 "RECIPES":[["Ice Storm","Maple Syrup"],
						["Ice Storm","Jammin Jelly"]],
			 },
		44: {"NAME":"Snow Bunny",
			 "RECIPES":[["Ice Storm","Golden Leaf"]],
			 },
		45: {"NAME":"Coco Candy",
			 "RECIPES":[["Cake Mix","Coconut"]],
			 },
		46: {"NAME":"Honey Candy",
			 "RECIPES":[["Honey Syrup","Cake Mix"]],
			 },
		47: {"NAME":"Jelly Candy",
			 "RECIPES":[["Jammin Jelly","Cake Mix"]],
			 },
		48: {"NAME":"Electro Pop",
			 "RECIPES":[["Cake Mix","Volt Shroom"]],
			 },
		49: {"NAME":"Fire Pop",
			 "RECIPES":[["Cake Mix","Fire Flower"],
						["Cake Mix","Hot Sauce"]],
			 },
		50: {"NAME":"Space Food",
			 "RECIPES":[["Dried Bouquet","Cake Mix"],
						["Dried Bouquet","Choco Cake"],
						["Dried Bouquet","Coco Candy"],
						["Dried Bouquet","Coconut"],
						["Dried Bouquet","Dried Shroom"],
						["Dried Bouquet","Electro Pop"],
						["Dried Bouquet","Fire Pop"],
						["Dried Bouquet","Fresh Juice"],
						["Dried Bouquet","Fried Egg"],
						["Dried Bouquet","Fruit Parfait"],
						["Dried Bouquet","Golden Leaf"],
						["Dried Bouquet","Healthy Salad"],
						["Dried Bouquet","Heartful Cake"],
						["Dried Bouquet","Honey Candy"],
						["Dried Bouquet","Honey Shroom"],
						["Dried Bouquet","Honey Super"],
						["Dried Bouquet","Honey Ultra"],
						["Dried Bouquet","Hot Dog"],
						["Dried Bouquet","Icicle Pop"],
						["Dried Bouquet","Ink Pasta"],
						["Dried Bouquet","Inky Sauce"],
						["Dried Bouquet","Jammin Jelly"],
						["Dried Bouquet","Jelly Candy"],
						["Dried Bouquet","Jelly Shroom"],
						["Dried Bouquet","Jelly Super"],
						["Dried Bouquet","Jelly Ultra"],
						["Dried Bouquet","Keel Mango"],
						["Dried Bouquet","Koopa Bun"],
						["Dried Bouquet","Koopa Tea"],
						["Dried Bouquet","Life Shroom"],
						#["Dried Bouquet","Love Pudding"],	#Unsure about this one
						["Dried Bouquet","Mango Delight"],
						["Dried Bouquet","Maple Shroom"],
						["Dried Bouquet","Maple Syrup"],
						["Dried Bouquet","Maple Ultra"],
						["Dried Bouquet","Meteor Meal"],
						["Dried Bouquet","Mistake"],
						["Dried Bouquet","Mousse Cake"],
						["Dried Bouquet","Mushroom"],
						["Dried Bouquet","Mystic Egg"],
						["Dried Bouquet","Omelette Meal"],
						["Dried Bouquet","Peachy Peach"],
						#["Dried Bouquet","Peach Tart"],	#Unsure about this one
						["Dried Bouquet","Shroom Cake"],
						["Dried Bouquet","Shroom Crepe"],
						["Dried Bouquet","Shroom Fry"],
						["Dried Bouquet","Shroom Roast"],
						["Dried Bouquet","Shroom Steak"],
						["Dried Bouquet","Snow Bunny"],
						["Dried Bouquet","Spaghetti"],
						["Dried Bouquet","Spicy Pasta"],
						["Dried Bouquet","Spicy Soup"],
						["Dried Bouquet","Super Shroom"],
						#["Dried Bouquet","Trial Stew"],	#Unsure about this one
						["Dried Bouquet","Turtley Leaf"],
						["Dried Bouquet","Ultra Shroom"],
						["Dried Bouquet","Zess Cookie"],
						["Dried Bouquet","Zess Deluxe"],
						["Dried Bouquet","Zess Dinner"],
						["Dried Bouquet","Zess Frappe"],
						["Dried Bouquet","Zess Special"],
						["Dried Bouquet","Zess Tea"],
						],
			 },
		51: {"NAME":"Poison Shroom",
			 "RECIPES":[["Inky Sauce","Slow Shroom"],
						#["Point Swap","Slow Shroom"],	#Point Swap is never used in evaluation
						],
			 },
		52: {"NAME":"Trial Stew",
			 "RECIPES":[["Poison Shroom","Couples Cake"]],
			 },
		53: {"NAME":"Courage Meal",
			 "RECIPES":[["Courage Shell","Zess Deluxe"],
						["Courage Shell","Zess Dinner"],
						["Courage Shell","Zess Special"]],
			 },
		54: {"NAME":"Coconut Bomb",
			 "RECIPES":[["Coconut","Fire Flower"]],
			 },
		55: {"NAME":"Egg Bomb",
			 "RECIPES":[["Mystery"],
						#["Dried Bouquet","Zess Dynamite"], #Unnecessary 2 Ingredients
						#["Mystic Egg","Fire Flower"],		#Unnecessary 2 Ingredients
						],
			 },
		56: {"NAME":"Zess Dynamite",
			 "RECIPES":[["Egg Bomb","Coconut Bomb"]],
			 },
		57: {"NAME":"Mistake",
			 "RECIPES":[["Shroom Fry"],
						["Shroom Roast"],
						["Shroom Steak"],
						["Honey Shroom"],
						["Maple Shroom"],
						["Jelly Shroom"],
						["Honey Super"],
						["Maple Super"],
						["Jelly Super"],
						["Honey Ultra"],
						["Maple Ultra"],
						["Jelly Ultra"],
						["Zess Dinner"],
						["Zess Special"],
						["Zess Deluxe"],
						["Spaghetti"],
						["Koopasta"],
						["Spicy Pasta"],
						["Ink Pasta"],
						["Spicy Soup"],
						["Fried Egg"],
						["Omelette Meal"],
						["Koopa Bun"],
						["Healthy Salad"],
						["Meteor Meal"],
						["Couples Cake"],
						["Mousse Cake"],
						["Shroom Cake"],
						["Choco Cake"],
						["Heartful Cake"],
						["Fruit Parfait"],
						["Mango Delight"],
						["Love Pudding"],
						["Zess Cookie"],
						["Shroom Crepe"],
						["Peach Tart"],
						["Koopa Tea"],
						["Zess Tea"],
						["Shroom Broth"],
						["Fresh Juice"],
						["Inky Sauce"],
						["Icicle Pop"],
						["Zess Frappe"],
						["Snow Bunny"],
						["Coco Candy"],
						["Honey Candy"],
						["Jelly Candy"],
						["Electro Pop"],
						["Fire Pop"],
						["Space Food"],
						["Poison Shroom"],
						["Trial Stew"],
						["Courage Meal"],
						["Coconut Bomb"],
						["Egg Bomb"],
						["Zess Dynamite"]],
			 },
	
		58: {"NAME":"Dried Bouquet", #When this ingredient is fulfilled, we also have to add Coconut, Courage Shell, and Keel Mango
			 "RECIPES":[["Hot Dog","Mousse Cake"]],
			 },
		}
	
	#randomize moves for step 1-20
	randomize = True
	#interesting way to pick legal moves
	select = False
	#log individual process state every 100000 iterations
	log_calls = True
	
	ITEM_NAMES = []


	#These items are listed in Japanese, which is why they don't actually look alphabetic
	#Comment Out Items that will never be encountered to save time on sorting moves
	ALPHABETIC_SORT = [
		#"POW Block",
		"Icicle Pop",
		#"Fright Mask",
		"Spicy Soup",
		"Ink Pasta",
		"Couples Cake",
		#"Point Swap",
		"Space Food",
		"Ultra Shroom",
		"Golden Leaf",
		"Cake Mix",
		"Courage Shell",
		"Courage Meal",
		"Thunder Bolt",
		#"Thunder Rage",
		"Koopa Tea",
		"Turtley Leaf",
		"Koopasta",
		#"[Koopa Curse]",
		"Koopa Bun",
		"Spicy Pasta",
		"Omelette Meal",
		"Mushroom",
		"Shroom Fry",
		"Shroom Crepe",
		"Shroom Cake",
		"Shroom Steak",
		"Shroom Roast",
		"Shooting Star",
		#"Gold Bar",
		#"Gold Bar x 3",
		"Life Shroom",
		#"Dizzy Dial",
		#"[Cake]",
		"Shroom Broth",
		"Ice Storm",
		"Coconut Bomb",
		"Coco Candy",
		#"Spite Pouch",
		"Mistake",
		"Dried Shroom",
		#"Inn Coupon",
		"Choco Cake",
		"Trial Stew",
		"Slow Shroom",
		"Gradual Syrup",
		"Super Shroom",
		#"HP Drain",
		"Tasty Tonic",
		#"Stopwatch",
		"Spaghetti",
		"Inky Sauce",
		#"Whacka Bump",
		#"Horsetail",
		#"[Trade Off]",
		#"Repel Cape",
		#"Boos Sheet",
		#"Power Punch",
		"Keel Mango",
		"Poison Shroom",
		"Dried Bouquet",
		"Mystery",
		"Zess Cookie",
		"Zess Special",
		"Zess Dynamite",
		"Zess Tea",
		"Zess Dinner",
		"Zess Deluxe",
		"Zess Frappe",
		#"Sleepy Sheep",
		"Love Pudding",
		"Honey Candy",
		"Honey Shroom",
		"Honey Super",
		"Honey Ultra",
		"Honey Syrup",
		"Egg Bomb",
		"Volt Shroom",
		"Electro Pop",
		"Peach Tart",
		"Peachy Peach",
		"Fire Pop",
		"Fire Flower",
		"Mystic Egg",
		#"Mr. Softener",
		"Fruit Parfait",
		"Fresh Juice",
		"Healthy Salad",
		"Meteor Meal",
		"Hot Dog",
		"Ruin Powder",
		"Mango Delight",
		#"Mini Mr. Mini",
		"Mousse Cake",
		"Maple Shroom",
		"Maple Super",
		"Maple Ultra",
		"Maple Syrup",
		"Fried Egg",
		"Heartful Cake",
		"Coconut",
		"Snow Bunny",
		#"Earth Quake",
		"Hot Sauce",
		"Jelly Shroom",
		"Jelly Super",
		"Jelly Ultra",
		"Jelly Candy",
		"Jammin Jelly",
		"Fresh Pasta",
		]


	#Comment Out Items that will never be encountered to save time on sorting moves
	TYPE_SORT = [
		#"[Koopa Curse]",
		"Mushroom",
		"Super Shroom",
		"Ultra Shroom",
		"Life Shroom",
		"Slow Shroom",
		"Dried Shroom",
		"Honey Syrup",
		"Maple Syrup",
		"Jammin Jelly",
		"Gradual Syrup",
		"Tasty Tonic",
		#"POW Block",
		"Fire Flower",
		"Ice Storm",
		"Earth Quake",
		"Thunder Bolt",
		"Thunder Rage",
		"Shooting Star",
		"Volt Shroom",
		"Repel Cape",
		"Boos Sheet",
		"Ruin Powder",
		#"Sleepy Sheep",
		#"Dizzy Dial",
		#"Stopwatch",
		#"Power Punch",
		#"Mini Mr. Mini",
		"Courage Shell",
		#"Mr. Softener",
		#"[Trade Off]",
		#"HP Drain",
		#"Point Swap",
		#"Fright Mask",
		"Mystery",
		#"Inn Coupon",
		#"Gold Bar",
		#"Gold Bar x 3",
		#"Whacka Bump",
		"Hot Dog",
		#"[Cake]",
		"Coconut",
		"Dried Bouquet",
		"Mystic Egg",
		"Golden Leaf",
		"Keel Mango",
		"Fresh Pasta",
		"Cake Mix",
		"Hot Sauce",
		"Turtley Leaf",
		#"Horsetail",
		"Peachy Peach",
		"Spite Pouch",
		"Shroom Fry",
		"Shroom Roast",
		"Shroom Steak",
		"Honey Shroom",
		"Maple Shroom",
		"Jelly Shroom",
		"Honey Super",
		"Maple Super",
		"Jelly Super",
		"Honey Ultra",
		"Maple Ultra",
		"Jelly Ultra",
		"Zess Dinner",
		"Zess Special",
		"Zess Deluxe",
		"Spaghetti",
		"Koopasta",
		"Spicy Pasta",
		"Ink Pasta",
		"Spicy Soup",
		"Fried Egg",
		"Omelette Meal",
		"Koopa Bun",
		"Healthy Salad",
		"Meteor Meal",
		"Couples Cake",
		"Mousse Cake",
		"Shroom Cake",
		"Choco Cake",
		"Heartful Cake",
		"Fruit Parfait",
		"Mango Delight",
		"Love Pudding",
		"Zess Cookie",
		"Shroom Crepe",
		"Peach Tart",
		"Koopa Tea",
		"Zess Tea",
		"Shroom Broth",
		"Fresh Juice",
		"Inky Sauce",
		"Icicle Pop",
		"Zess Frappe",
		"Snow Bunny",
		"Coco Candy",
		"Honey Candy",
		"Jelly Candy",
		"Electro Pop",
		"Fire Pop",
		"Space Food",
		"Poison Shroom",
		"Trial Stew",
		"Courage Meal",
		"Coconut Bomb",
		"Egg Bomb",
		"Zess Dynamite",
		"Mistake",
	]


	#How many frames does it take to select an inventory item?
	INV_FRAMES = [
		[], #0 Items
		[0], #1 Item
		[0,0], #2 Items
		[0,0,0], #3 Items
		[0,0,2,0], #4 Items
		[0,0,2,2,0], #5 Items
		[0,0,2,4,2,0], #6 Items
		[0,0,2,4,4,2,0], #7 Items
		[0,0,2,4,6,4,2,0], #8 Items
		[0,0,2,4,6,6,4,2,0], #9 Items
		[0,0,2,4,6,8,6,4,2,0], #10 Items
		[0,0,2,4,6,8,8,6,4,2,0], #11 Items
		[0,0,2,4,6,8,10,8,6,4,2,0], #12 Items
		[0,0,2,4,6,8,10,10,8,6,4,2,0], #13 Items
		[0,0,2,4,6,8,10,12,10,8,6,4,2,0], #14 Items
		[0,0,2,4,6,8,10,12,12,10,8,6,4,2,0], #15 Items
		[0,0,2,4,6,8,10,12,14,12,10,8,6,4,2,0], #16 Items
		[0,0,2,4,6,8,10,12,14,14,12,10,8,6,4,2,0], #17 Items
		[0,0,2,4,6,8,10,12,14,16,14,12,10,8,6,4,2,0], #18 Items
		[0,0,2,4,6,8,10,12,14,16,16,14,12,10,8,6,4,2,0], #19 Items
		[0,0,2,4,6,8,10,12,14,16,18,16,14,12,10,8,6,4,2,0], #20 Items
		[0,0,2,4,6,8,10,12,14,16,18,18,16,14,12,10,8,6,4,2,0], #21 Items
	]


	################################################################################
	# With the given inventory and knolwedge of which outputs have already been created,
	# Determine if the given recipe can be fulfilled
	################################################################################
	def check_ingredients(recipe, inventory, has_output_been_created, level=0):	  
		for item in recipe:
			if item in inventory:
				#This item is in the current inventory, do nothing for now
				pass
			elif item in ITEM_NAMES and (not has_output_been_created[ITEM_NAMES.index(item)]):
				#This item is not in the current inventory, but it is another output item that hasn't been made yet
				#Check all recipes of the output item to see if it can be made with the current inventory.
				if(level < 3):
					#Don't evaluate any further than the 3rd recursion level
					#Done to avoid infinite recipe loops (Inky Sauce > Shroom Broth > Poison Shroom > Inky Sauce > ...)
					temp_good_recipe = False
					for new_recipe in ITEMS[ITEM_NAMES.index(item)+1]["RECIPES"]:
						#Check to see if this ingredient can be made with other ingredients the player has
						if(check_ingredients(new_recipe, inventory, has_output_been_created,level+1)):
							#At least one recipe can be fulfilled now.
							temp_good_recipe = True


					#After evaluating all recipes of the ITEM, if that ITEM cannot be produced, return false
					if(not temp_good_recipe):
						return False
				else:
					return False
			else:
				#The item isn't in the inventory, and can't be made through another recipe, return False
				return False


		#By getting here, we know all ingredients are at least possible to create still with the current inventory
		return True	   


	################################################################################
	# With the given inventory, determine if the remaining output items be fulfilled
	################################################################################
	def check_ingredients(recipe, inventory, has_output_been_created):


		################print("Inside C_I: {0}".format(recipe))
		for item in recipe:
			if item in inventory:
				#This item is in the current inventory, do nothing for now
				pass
			elif item in ITEM_NAMES and (not has_output_been_created[ITEM_NAMES.index(item)]):
				temp_good_recipe = False
				for new_recipe in ITEMS[ITEM_NAMES.index(item)+1]["RECIPES"]:
					#Recurse on all recipes that can make this ITEM
					temp_output_created = copy.copy(has_output_been_created)
					temp_output_created[ITEM_NAMES.index(item)] = True
					temp_good_recipe = temp_good_recipe or check_ingredients(new_recipe, inventory, temp_output_created)


				#After evaluating all recipes of the ITEM, if that ITEM cannot be produced, return false
				if(not temp_good_recipe):
					return False
			else:
				#The item isn't in the inventory, and can't be made through another recipe, return False
				return False


		#By getting here, we know all ingredients are at least possible to create still with the current inventory
		return True	   


	################################################################################
	# With the given inventory, can the remaining recipes be fulfilled?
	################################################################################
	def remainingOutputsCanBeFulfilled(inventory, has_output_been_created):	   
		#Iterate through all remaining output items
		for output_item in ITEMS:
			#Only want output items that haven't already been created elsewhere
			if(not has_output_been_created[output_item-1]):
			
				#Iterate through all recipes
				viable_ingredients_found = False
				for recipe in ITEMS[output_item]["RECIPES"]:
					#This is done to avoid infinite recursion
					#TODO: Check if there's a more efficient algorithm
					temp_output_created = copy.copy(has_output_been_created)
					temp_output_created[output_item-1] = True
					viable_ingredients_found = viable_ingredients_found or check_ingredients(recipe, inventory, temp_output_created)


				if(not viable_ingredients_found):
					#There's a few exceptions
					if(has_output_been_created[57]):
						#the 58th "output" is really a representation of the Chapter 5 Intermission
						#Where the Keel Mango and Coconut are collected, so a few recipes before this intermission won't be viable
						#If chapter 5 has been done, then there's no exceptions anymore
						#if(print_debug):
						#	 print("Couldn't make product {0}".format(ITEM_NAMES[output_item-1]))
						return False
					elif(ITEMS[output_item]["NAME"] in ["Zess Dinner",
														"Koopa Bun",
														"Fruit Parfait",
														"Mango Delight",
														"Love Pudding",
														"Fresh Juice",
														"Coco Candy",
														"Courage Meal",
														"Coconut Bomb",
														"Zess Dynamite"]):
						#This has flaws, but any items that need Keel Mangos or Coconuts
						#will be considered fine for pre-Chapter-5 evaluation
						pass
					else:
					
						### print("THIS OUTPUT IS NO LONGER VIABLE!!!")


						#Any other output items will need something that we *should* have
						return False


		#Haven't returned false in evaluating all output items
		#Meaning that all remaining outputs can still be fulfilled!
		return True


	#####################################################################################
	# Print the Results of all states observed in the current stack
	#####################################################################################
	def print_results(filename,written_step,frames_taken,total_frames,inventory,output_created):
		f = open(filename,"w")
		#Write Header information
		f.write("Description\tFrames Taken\tTotal Frames")
		for z in range(0,20):
			f.write("\tSlot #{0}".format(z+1))
		for z in range(0,58):
			f.write("\t{0}".format(ITEM_NAMES[z]))
		f.write("\n")


		#Data Information		 
		for i in range(0,step_index+1):
			f.write("{0}\t{1}\t{2}".format(written_step[i],frames_taken[i],total_frames[i]))
			for z in range(0,20):
				f.write("\t{0}".format(inventory[i][z]))
			for z in range(0,58):
				f.write("\t{0}".format(output_created[i][z]))
			f.write("\n")
		f.close()


	#################################################################
	# Get the insertion index for where to place this legal move
	#################################################################
	def get_insertion_index(legal_moves, step_index, frames):
		temp_index = 0
		while(temp_index < len(legal_moves[step_index]) and legal_moves[step_index][temp_index][2] < frames):
			temp_index += 1
		return temp_index


	#####################################################################################
	# MAIN SUBROUTINE
	#####################################################################################


	#Fill the ITEM_NAMES
	for item in ITEMS:
		ITEM_NAMES.append(ITEMS[item]["NAME"])


	#Check that all inputted recipes and ingredients are in the list
	for i in ITEMS:
		if(ITEMS[i]["NAME"] not in ALPHABETIC_SORT):
			print("Item '{0}' not in Alphabetic Sort list".format(ITEMS[i]["NAME"]))
			input()
		if(ITEMS[i]["NAME"] not in TYPE_SORT):
			print("Item '{0}' not in Type Sort list".format(ITEMS[i]["NAME"]))
			input()
		for j in ITEMS[i]["RECIPES"]:
			for x in j:
				if x not in ALPHABETIC_SORT:
					print ("Ingredient '{0}' not in Alphabetic Sort list".format(x))
					input()
				if x not in TYPE_SORT:
					print ("Ingredient '{0}' not in Type Sort list".format(x))
					input()
	#print("All Items Checked to be in Alphabetic List")


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

	#frame_record is now set in async call
	#frame_record = 9999 #4409


	#Total frames to choose an additional ingredient (As opposed to just a single ingredient)
	#This does not include the additional frames needed to navigate to the items that you want to use
	CHOOSE_SECOND_INGREDIENT_FRAMES = 56


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

	while(True):

		step_index = 0
		iteration_count = 0

		#The Beginning Inventory
		STARTING_INVENTORY = []


		#Read in the starting inventor
		f = open("inventory.txt","r")
		for lines in f:
			ingredient = lines.strip("\n")
			if(not ingredient in ALPHABETIC_SORT):
				#print("Error: ({0}) Not Found in Alphabetic Sort List!".format(ingredient))
				input()
			elif(not ingredient in TYPE_SORT):
				#print("Error: ({0}) Not Found in Type Sort List!".format(ingredient))
				input()
			else:
				STARTING_INVENTORY.append(lines.strip("\n"))
		f.close()
		#print("Starting Inventory Inputted Successfully")


		#State Description for each 'Step' taken
		written_step = ["Begin"]
		frames_taken = [0]
		total_frames = [0]
		inventory = [STARTING_INVENTORY]
		output_created = [[False]*58]


		legal_moves=[]


		evaluation_counter = 0


		#Load in the latest temp_results
		loaded_temp_descriptions = []
		try:
			f = open("Temp Results.txt","r")
			for lines in f:
				loaded_temp_descriptions.append(lines.split("\t")[0])
			f.close()
			loaded_temp_descriptions.pop(0)
			loaded_temp_descriptions.pop(0)
			#print("Temp Results Loaded In, starting from last recorded checkpoint...")
		except:
			pass
			#print("Couldn't load in Temp Results. Starting anew")

		#print("=======================================")
		#print("Beginning Evaluation of Search Space...")
		#Begin the iterative loop
		while(iteration_count < 1000000):
			#Sanity Check Log Temporary Results
			evaluation_counter += 1
			if(evaluation_counter % 500000 == 0):
				#print(evaluation_counter)
				pass
				#print_results("Temp Results.txt",written_step,frames_taken,total_frames,inventory,output_created)


				#Use the below steps if you want to wipe everything away and start evaluation anew
				#step_index = 0
				#written_step = ["Begin"]
				#frames_taken = [0]
				#total_frames = [0]
				#inventory = [STARTING_QUEUE]
				#output_created = [[False]*58]
				#legal_moves=[]
	
			#Check for bad states to immediately retreat from
			if((not output_created[step_index][57] and
			   (not "Fire Flower" in inventory[step_index] or
				not "Mystic Egg" in inventory[step_index] or
				not "Cake Mix" in inventory[step_index] or
				not "Turtley Leaf" in inventory[step_index] or
				output_created[step_index][54] and not "Egg Bomb" in inventory[step_index]))): #If the Egg Bomb was made pre-Ch.5, make sure its still in the inventory
				#We need to have the fire flower for the post-chapter-5 intermission
		
				#Regardless of record status, it's time to go back up and find new endstates
				#Wipe away the current state
				written_step.pop()
				frames_taken.pop()
				total_frames.pop()
				inventory.pop()
				output_created.pop()


				#Step back up a level
				step_index -= 1


			#Check for end condition (57 Recipes + the Chapter 5 intermission, which is treated as an additional "recipe")
			elif(output_created[step_index].count(True) == 58):
				#All Recipes have been fulfilled!
				#Check that the total time taken is strictly less than the current observed record.


				#Apply a frame penalty if the final move did not toss an item:
				if(not "toss" in written_step[-1]):
					written_step[-1] += " (No-Toss 5 Frame Penalty for Jump Storage)"
					frames_taken[-1] += JUMP_STORAGE_NO_TOSS_FRAMES
					total_frames[-1] += JUMP_STORAGE_NO_TOSS_FRAMES
				else:
					written_step[-1] += " (Jump Storage on Tossed Item)"
		
				if(total_frames[step_index] < frame_record):
					#New Record!
					frame_record = total_frames[step_index]
					#print("New Record Time: {0}".format(total_frames[step_index]))
					#Log the updated outcome
					print_results("results/[{0}].txt".format(total_frames),written_step,frames_taken,total_frames,inventory,output_created)
					#pause after each new record to check results
					#raw_input()
					return [total_frames[step_index], call_number]
						


				#Regardless of record status, its time to go back up and find new endstates
				#Wipe away the current state
				written_step.pop()
				frames_taken.pop()
				total_frames.pop()
				inventory.pop()
				output_created.pop()


				#Step back up a level
				step_index -= 1


			#End condition not met, Check if this current level has something in the event queue
			elif(len(legal_moves) == step_index):
				legal_moves.append([])
				#Generate the list of all possible decisions


				#Only evaluate the 57th recipe (Mistake) when its the last recipe to fulfill
				# This is because it is relatively easy to craft this output with many of the previous outputs, and will take minimal frames
				if(output_created[step_index].count(True) == 57):
					upper_output_limit = 58
				else:
					upper_output_limit = 57
		
				for output_item in range(1,upper_output_limit):
					#Only want recipes that haven't already been fulfilled
					if(not output_created[step_index][output_item-1]):
						#Iterate through all ingredient_lists
						for recipe in ITEMS[output_item]["RECIPES"]:
							#Only want ingredient lists that can be satisfied by the current inventory
							if(all([ingredient in inventory[step_index] for ingredient in recipe])):						
								#This is a recipe that can be fulfilled right now!
								temp_inventory = copy.copy(inventory[step_index])


								#Mark that the output has been fulfilled for viability determination
								temp_outputs_fulfilled = copy.copy(output_created[step_index])
								temp_outputs_fulfilled[output_item-1] = True
						
								if(len(recipe) == 1):
									#This is a potentially viable recipe with 1 ingredient


									#Determine how many viable items are in the list (No Nulls or Blocked), and the location of the ingredient
									viable_items = 20 - (temp_inventory.count("NULL")+temp_inventory.count("BLOCKED"))
									ingredient_loc = temp_inventory.index(recipe[0])


									#Determine the offset by "NULL"s before the desired item, as NULLs do not appear during inventory navigation
									ingredient_offset = 0
									for i in range(0,ingredient_loc):
										if(temp_inventory[i] == "NULL"):
											ingredient_offset += 1


									#Modify the inventory if the ingredient was in the first 10 slots
									if(ingredient_loc < 10):
										temp_inventory[ingredient_loc] = "NULL"


									#Determine how many frames will be needed to select that item  
									temp_frames = INV_FRAMES[viable_items][ingredient_loc-ingredient_offset]


									#Describe what items were used
									use_description = "Use {0} in slot {1} ".format(recipe[0],ingredient_loc+1)
								else:							 
									#This is a potentially viable recipe with 2 ingredients
									#Baseline frames based on how many times we need to access the menu
									temp_frames = CHOOSE_SECOND_INGREDIENT_FRAMES


									#Mark that the output has been fulfilled
									temp_outputs_fulfilled = copy.copy(output_created[step_index])
									temp_outputs_fulfilled[output_item - 1] = True


									#Determine how many viable spaces there are and the locations of both ingredients
									viable_items = 20 - (temp_inventory.count("NULL")+temp_inventory.count("BLOCKED")) 
									ingredient_loc = [temp_inventory.index(recipe[0]),
													  temp_inventory.index(recipe[1])]


									ingredient_name_0 = recipe[0]
									ingredient_name_1 = recipe[1]


									ingredient_offset_0 = 0
									for i in range(0,ingredient_loc[0]):
										if(temp_inventory[i] == "NULL"):
											ingredient_offset_0 += 1


									ingredient_offset_1 = 0
									for i in range(0,ingredient_loc[1]):
										if(temp_inventory[i] == "NULL"):
											ingredient_offset_1 += 1


									#Determine which order of ingredients to take (Always take the quickest 1st)
									if(INV_FRAMES[viable_items][ingredient_loc[1]-ingredient_offset_1] < INV_FRAMES[viable_items][ingredient_loc[0]-ingredient_offset_0]):
										#It's faster to select the 2nd item, so make it the priority and switch the order
										ingredient_loc.reverse()


										#Flip the ingredient offsets too (TODO: Make less awful)
										temp = ingredient_offset_0
										ingredient_offset_0 = ingredient_offset_1
										ingredient_offset_1 = temp


										ingredient_name_0 = recipe[1]
										ingredient_name_1 = recipe[0]


									#Calculate the number of frames needed to grab the first item
									temp_frames += INV_FRAMES[viable_items][ingredient_loc[0]-ingredient_offset_0]


									#Set this inventory index to null if the item was in the first 10 slots
									#Also determine the frames needed for the 2nd ingredient
									if(ingredient_loc[0] < 10):
										temp_inventory[ingredient_loc[0]] = "NULL"
										temp_frames += INV_FRAMES[viable_items-1][ingredient_loc[1]-ingredient_offset_1-1]
									else:
										temp_frames += INV_FRAMES[viable_items-0][ingredient_loc[1]-ingredient_offset_1-0]


									#Set this inventory index to null if the item was in the first 10 slots
									if(ingredient_loc[1] < 10):
										temp_inventory[ingredient_loc[1]] = "NULL"


									#Describe what items were used
									use_description = "Use {0} in slot {1} and {2} in slot {3} ".format(ingredient_name_0,
																										ingredient_loc[0]+1,
																										ingredient_name_1,
																										ingredient_loc[1]+1)


								#Handle allocation of the OUTPUT variable
								#Options vary by whether there are "NULL"s within the inventory
								try:
									#If there are NULLs in the inventory. The output will always go to 1st NULL in the inventory 
									placed_index = temp_inventory.index("NULL")


									temp_inventory[placed_index] = ITEMS[output_item]["NAME"]


									#Check to see if this state is viable
									if(remainingOutputsCanBeFulfilled(temp_inventory, temp_outputs_fulfilled)):
										#This is a viable state that doesn't increase frames at all (Output was auto-placed)
										#Determine where to insert this legal move into the list of legal moves (Sorted by frames taken)
										insert_index = get_insertion_index(legal_moves, step_index, temp_frames)


										place_description = "to make {0}, auto-placed in slot {1}".format(ITEM_NAMES[output_item-1],placed_index+1)
										legal_moves[step_index].insert(insert_index,[use_description+place_description,output_item,temp_frames,temp_inventory])
								except:
									#There are no NULLs in the inventory. Something must be tossed
									#Total number of frames increased by forcing to toss something
									temp_frames += TOSS_FRAMES
							
									#Evaluate viability of tossing the output item itself
									if(remainingOutputsCanBeFulfilled(temp_inventory, temp_outputs_fulfilled)):
										#Temp frames do not increase as the output item is always at the very top of the list
										insert_index = get_insertion_index(legal_moves, step_index, temp_frames)


										place_description = "to make (and toss) {0}".format(ITEM_NAMES[output_item-1])
										legal_moves[step_index].insert(insert_index,[use_description+place_description,output_item,temp_frames,temp_inventory])


									#Evaluate the viability of tossing all current inventory items
									#Assumed that it is impossible to toss and replace any items in the last 10 positions
									for tossed_index in range(0,10):
										#Only interested in slots that contain an actual item
										if(temp_inventory[tossed_index] == "NULL" or
										   temp_inventory[tossed_index] == "BLOCKED"):
											print("Shouldn't be here!")
											input()
										#Make a copy of the temp_inventory with the replaced item
										replaced_inventory = copy.copy(temp_inventory)
										replaced_inventory[tossed_index] = ITEM_NAMES[output_item-1]
										tossed_item_name = temp_inventory[tossed_index]


										if(remainingOutputsCanBeFulfilled(replaced_inventory, temp_outputs_fulfilled)):
											#Calculate the additional tossed frames. Have to +1 both viable_items and tossed_item as
											#the output is at the top of the list, pushing everything else down one spot
											replaced_frames = temp_frames+INV_FRAMES[viable_items+1][tossed_index+1]
											insert_index = get_insertion_index(legal_moves, step_index, replaced_frames)
										
											place_description = "to make {0}, toss {1} in slot {2}".format(ITEM_NAMES[output_item-1],
																										   tossed_item_name,
																										   tossed_index+1)
											legal_moves[step_index].insert(insert_index,[use_description+place_description,output_item,replaced_frames,replaced_inventory])
								
				#Special handling of the 58th item, which is representative of the Chapter 5 intermission
				#Only want To evaluate when the output hasn't been created
				#Also need to make sure the Mousse Cake is available anywhere
				#Also need to make sure the Hot Dog is in the *last* 10 inventory slots, as it will be needed twice
				if(not output_created[step_index][57] and
				   "Mousse Cake" in inventory[step_index] and
				   "Hot Dog" in inventory[step_index][10:20]):
					#Create an outputs chart but with the Dried Bouquet collected
					temp_outputs_fulfilled = copy.copy(output_created[step_index])
					temp_outputs_fulfilled[57] = True


					#Create a temp inventory
					temp_inventory = copy.copy(inventory[step_index])
					temp_frames_DB = 0 #Dried Bouquet
					temp_frames_CO = 0 #Coconut
					temp_frames_KM = 0 #Keel Mango
					temp_frames_CS = 0 #Courage Shell


					temp_index_DB = 0 #Dried Bouquet
					temp_index_CO = 0 #Coconut
					temp_index_KM = 0 #Keel Mango
					temp_index_CS = 0 #Courage Shell			


					#If the Mousse Cake is in the first 10 spots, change it to a null
					mousse_cake_loc = temp_inventory.index("Mousse Cake")
					if(mousse_cake_loc < 10):
						temp_inventory[mousse_cake_loc] = "NULL"
			
					#Allocate the Dried Bouquet
					if("NULL" in temp_inventory):
						#Dried Bouquet goes in the 1st NULL spot, no frames taken
						temp_frames_DB = 0
						temp_index_DB = temp_inventory.index("NULL")
						temp_inventory[temp_index_DB] = "Dried Bouquet"


						#Allocate the Coconut
						if("NULL" in temp_inventory):
							#Coconut goes in the 2nd NULL spot, no frames taken
							temp_frames_CO = 0
							temp_index_CO = temp_inventory.index("NULL")
							temp_inventory[temp_index_CO] = "Coconut"


							#Allocate the Keel Mango
							if("NULL" in temp_inventory):
								#Keel Mango goes in the 3rd NULL spot, no frames taken
								temp_frames_KM = 0
								temp_index_KM = temp_inventory.index("NULL")
								temp_inventory[temp_index_KM] = "Keel Mango"


								#Allocate the Courage Shell
								if("NULL" in temp_inventory):
									#Courage Shell goes in the 4th NULL spot, no frames taken
									temp_frames_CS = 0
									tmep_index_CS = temp_inventory.index("NULL")
									temp_inventory[temp_index_CS] = "Courage Shell"


									#Check that this state is viable
									if(remainingOutputsCanBeFulfilled(temp_inventory, temp_outputs_fulfilled)):
										#Total Relevant frames that will be taken by this intermission
										temp_frame_total = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS


										#Get the index on where to insert this legal move to
										insert_index = get_insertion_index(legal_moves, step_index, temp_frame_total)


										#Describe how the break should play out
										ch5_description = "Ch.5 Break: DB auto-slot {0}, CO auto-slot {1}, KM auto-slot {2}, CS auto-slot {3}".format(temp_index_DB+1,
																																					  temp_index_CO+1,
																																					  temp_index_KM+1,
																																					  temp_index_CS+1)
										#Append the Legal Move
										legal_moves[step_index].insert(insert_index,[ch5_description,
																					 58,
																					 temp_frame_total,
																					 temp_inventory])
								else:
									#No NULLS to allocate the Courage Shell


									#Determine how many viable locations are available
									viable_items = 20 - (temp_inventory.count("BLOCKED"))
							
									#See which inventory slots can be tossed to accommodate it
									for temp_index_CS in range(0,10):
										#Don't place it anywhere that's blocked or occupied by the other Ch.5 Items
										if(temp_index_CS != temp_index_DB and
										   temp_index_CS != temp_index_CO and
										   temp_index_CS != temp_index_KM):
											#Potentially Viable Inventory, allocate the items
											replaced_inventory = copy.copy(temp_inventory)
											replaced_inventory[temp_index_CS] = "Courage Shell"									   


											#Check that this state is viable
											if(remainingOutputsCanBeFulfilled(replaced_inventory, temp_outputs_fulfilled)):
												#Calculate the temp frames
												temp_frames_CS = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_CS]
										
												#Total Relevant frames that will be taken by this intermission
												temp_frame_total = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS


												#Describe how the break should play out
												ch5_description = "Ch.5 Break: DB auto-slot {0}, CO auto-slot {1}, KM auto-slot {2}, CS put in slot {3}".format(temp_index_DB+1,
																																								temp_index_CO+1,
																																								temp_index_KM+1,
																																								temp_index_CS+1)
												#Append the Legal Move
												legal_moves[step_index].insert(insert_index,[ch5_description,
																							 58,
																							 temp_frame_total,
																							 replaced_inventory])
							else:
								#No NULLS to allocate the Keel Mango or Courage Shell


								#Determine how many viable locations are available
								viable_items = 20 - (temp_inventory.count("BLOCKED"))


								#See which inventory slots can be tossed to accommodate these items
								for temp_index_KM in range(0,10):
									for temp_index_CS in range(0,10):
										#Don't place it anywhere that's blocked or occupied by the other Ch.5 Items
										if(temp_index_KM != temp_index_DB and
										   temp_index_KM != temp_index_CO and
										   temp_index_CS != temp_index_DB and
										   temp_index_CS != temp_index_CO and
										   temp_index_CS != temp_index_KM):
											#Potentially Viable Inventory, allocate the items
											replaced_inventory = copy.copy(temp_inventory)
											replaced_inventory[temp_index_KM] = "Keel Mango"
											replaced_inventory[temp_index_CS] = "Courage Shell"
									
											#Check that this state is viable
											if(remainingOutputsCanBeFulfilled(replaced_inventory, temp_outputs_fulfilled)):


												#Calculate the temp frames
												temp_frames_KM = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_KM]
												temp_frames_CS = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_CS]
										
												#Total Relevant frames that will be taken by this intermission
												temp_frame_total = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS


												#Describe how the break should play out
												ch5_description = "Ch.5 Break: DB auto-slot {0}, CO auto-slot {1}, KM put in slot {2}, CS put in slot {3}".format(temp_index_DB+1,
																																								  temp_index_CO+1,
																																								  temp_index_KM+1,
																																								  temp_index_CS+1)
												#Append the Legal Move
												legal_moves[step_index].insert(insert_index,[ch5_description,
																							 58,
																							 temp_frame_total,
																							 replaced_inventory])
						else:
							#No NULLS to allocate the Coconut, Keel Mango, or Courage Shell
					
							#Determine how many viable locations are available
							viable_items = 20 - (temp_inventory.count("BLOCKED"))


							#See which inventory slots can be tossed to accommodate these items
							for temp_index_CO in range(0,10):
								for temp_index_KM in range(0,10):
									for temp_index_CS in range(0,10):
										#Don't place it anywhere that's blocked or occupied by the other Ch.5 Items
										if(temp_index_CO != temp_index_DB and
										   temp_index_KM != temp_index_DB and
										   temp_index_KM != temp_index_CO and
										   temp_index_CS != temp_index_DB and
										   temp_index_CS != temp_index_CO and
										   temp_index_CS != temp_index_KM):
											#Potentially Viable Inventory, allocate the items
											replaced_inventory = copy.copy(temp_inventory)
											replaced_inventory[temp_index_CO] = "Coconut"
											replaced_inventory[temp_index_KM] = "Keel Mango"
											replaced_inventory[temp_index_CS] = "Courage Shell"


											#Check that this state is viable
											if(remainingOutputsCanBeFulfilled(replaced_inventory, temp_outputs_fulfilled)):


												#Calculate the temp frames
												temp_frames_CO = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_CO]
												temp_frames_KM = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_KM]
												temp_frames_CS = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_CS]
										
												#Total Relevant frames that will be taken by this intermission
												temp_frame_total = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS


												#Describe how the break should play out
												ch5_description = "Ch.5 Break: DB auto-slot {0}, CO put in slot {1}, KM put in slot {2}, CS put in slot {3}".format(temp_index_DB+1,
																																									temp_index_CO+1,
																																									temp_index_KM+1,
																																									temp_index_CS+1)
												#Append the Legal Move
												legal_moves[step_index].insert(insert_index,[ch5_description,
																							 58,
																							 temp_frame_total,
																							 replaced_inventory])
									
									
					else:
						#No NULLS to allocate the Dried Bouquet, Coconut, Keel Mango, or Courage Shell!
					
						#Determine how many viable locations are available
						viable_items = 20 - (temp_inventory.count("BLOCKED"))


						#See which inventory slots can be tossed to accommodate these items
						for temp_index_DB in range(0,10):
							for temp_index_CO in range(0,10):
								for temp_index_KM in range(0,10):
									for temp_index_CS in range(0,10):
										#Don't place it anywhere that's blocked or occupied by the other Ch.5 Items
										if(temp_index_CO != temp_index_DB and
										   temp_index_KM != temp_index_DB and
										   temp_index_KM != temp_index_CO and
										   temp_index_CS != temp_index_DB and
										   temp_index_CS != temp_index_CO and
										   temp_index_CS != temp_index_KM):
											#Potentially Viable Inventory, allocate the items
											replaced_inventory = copy.copy(temp_inventory)
											replaced_inventory[temp_index_DB] = "Dried Bouquet"
											replaced_inventory[temp_index_CO] = "Coconut"
											replaced_inventory[temp_index_KM] = "Keel Mango"
											replaced_inventory[temp_index_CS] = "Courage Shell"


											#Check that this state is viable
											if(remainingOutputsCanBeFulfilled(replaced_inventory, temp_outputs_fulfilled)):


												#Calculate the temp frames
												temp_frames_DB = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_DB]
												temp_frames_CO = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_CO]
												temp_frames_KM = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_KM]
												temp_frames_CS = TOSS_FRAMES + INV_FRAMES[viable_items][temp_index_CS]
										
												#Total Relevant frames that will be taken by this intermission
												temp_frame_total = temp_frames_DB + temp_frames_CO + temp_frames_KM + temp_frames_CS


												#Describe how the break should play out
												ch5_description = "Ch.5 Break: DB put in slot {0}, CO put in slot {1}, KM put in slot {2}, CS put in slot {3}".format(temp_index_DB+1,
																																									  temp_index_CO+1,
																																									  temp_index_KM+1,
																																									  temp_index_CS+1)
												#Append the Legal Move
												legal_moves[step_index].insert(insert_index,[ch5_description,
																							 58,
																							 temp_frame_total,
																							 replaced_inventory])
			
				#Special handling of the 4 sorts
				#Don't sort if the previous move was a sort (Redundant)
				if(written_step[step_index][0:4] != "Sort"):


					total_sorts = 0
					for i in range(0,step_index+1):
						if(written_step[i][0:4] == "Sort"):
							total_sorts += 1


					#Only want max 5 sorts
					if(total_sorts <= 5):
						#Alphabetical Sort
						alpha_inventory = []
						total_BLOCKED = 0


						for i in range(0,len(ALPHABETIC_SORT)):
							for j in range(0,inventory[step_index].count(ALPHABETIC_SORT[i])):
								alpha_inventory.append(ALPHABETIC_SORT[i])


						#Remaining Spaces are "Blocked"
						while(len(alpha_inventory) < 20):
							alpha_inventory.append("BLOCKED")
							total_BLOCKED += 1


						#Only add the legal move if the sort actually changes the inventory
						if(alpha_inventory != inventory[step_index]):
							temp_index = 0
							while(temp_index < len(legal_moves[step_index]) and legal_moves[step_index][temp_index][2] < ALPHA_SORT_FRAMES):
								temp_index += 1


							description = "Sort - Alphabetical"
							#legal_moves[step_index].insert(temp_index,[description,-1,ALPHA_SORT_FRAMES,alpha_inventory])
							legal_moves[step_index].append([description,-1,ALPHA_SORT_FRAMES,alpha_inventory])


						#Reverse Alphabetical Sort
						reverse_alpha_inventory = []
						for i in range(19-total_BLOCKED,-1,-1):
							reverse_alpha_inventory.append(alpha_inventory[i])			 


						#Remaining spaces are "Blocked"
						while(len(reverse_alpha_inventory) < 20):
							reverse_alpha_inventory.append("BLOCKED")


						#Only add the legal move if the sort actually changes the inventory
						if(reverse_alpha_inventory != inventory[step_index]):
							temp_index = 0
							while(temp_index < len(legal_moves[step_index]) and legal_moves[step_index][temp_index][2] < REVERSE_ALPHA_SORT_FRAMES):
								temp_index += 1


							description = "Sort - Reverse Alphabetical"
							#legal_moves[step_index].insert(temp_index,[description,-1,REVERSE_ALPHA_SORT_FRAMES,reverse_alpha_inventory])
							legal_moves[step_index].append([description,-1,REVERSE_ALPHA_SORT_FRAMES,reverse_alpha_inventory])


						#Type Sort
						type_inventory = []


						for i in range(0,len(TYPE_SORT)):
							for j in range(0,inventory[step_index].count(TYPE_SORT[i])):
								type_inventory.append(TYPE_SORT[i])


						#Remaining Spaces are "Blocked"
						while(len(type_inventory) < 20):
							type_inventory.append("BLOCKED")


						#Only add the legal move if the sort actually changes the inventory
						if(type_inventory != inventory[step_index]):
							temp_index = 0
							while(temp_index < len(legal_moves[step_index]) and legal_moves[step_index][temp_index][2] < TYPE_SORT_FRAMES):
								temp_index += 1


							description = "Sort - Type"
							#legal_moves[step_index].insert(temp_index,[description,-1,TYPE_SORT_FRAMES,type_inventory])
							legal_moves[step_index].append([description,-1,TYPE_SORT_FRAMES,type_inventory])


						#Reverse Type Sort
						reverse_type_inventory = []
						for i in range(19-total_BLOCKED,-1,-1):
							reverse_type_inventory.append(type_inventory[i])


						#Remaining spaces are "Blocked"
						while(len(reverse_type_inventory) < 20):
							reverse_type_inventory.append("BLOCKED")


						#Only add the legal move if the sort actually changes the inventory
						if(reverse_type_inventory != inventory[step_index]):
							temp_index = 0
							while(temp_index < len(legal_moves[step_index]) and legal_moves[step_index][temp_index][2] < REVERSE_TYPE_SORT_FRAMES):
								temp_index += 1


							description = "Sort - Reverse Type"
							#legal_moves[step_index].insert(temp_index,[description,-1,REVERSE_TYPE_SORT_FRAMES,reverse_type_inventory])
							legal_moves[step_index].append([description,-1,REVERSE_TYPE_SORT_FRAMES,reverse_type_inventory])


				#Filter out all legal moves that would exceed the current frame limit
				legal_moves[step_index] = list(filter(lambda x: x[2]+total_frames[step_index] < frame_record, legal_moves[step_index]))
			
				#Filter out all legal moves that use 2 ingredients in the very first legal move
				if(step_index == 0):
					legal_moves[step_index] = list(filter(lambda x: not " and " in x[0], legal_moves[step_index]))

				#If there's a loaded_temp_description, remove branches until we fine the last branch we we're evaluating
				if(len(loaded_temp_descriptions) > 0):
					while(legal_moves[step_index][0][0] != loaded_temp_descriptions[0]):
						legal_moves[step_index].pop(0)
					loaded_temp_descriptions.pop(0)


				#Just because, if the step index is sufficiently small, just shuffle!
				if(randomize):
					if(step_index < 20):
						random.shuffle(legal_moves[step_index])


				#Interesting methodology to pick out decent legal moves
				if(select):
					while(len(legal_moves[step_index]) > 1 and random.random() < 0.1):
						legal_moves[step_index].pop(-1)


				if(len(legal_moves[step_index]) == 0):
					#There are no legal moves to iterate on, go back up...
					#Wipe away the current state
					written_step.pop()
					frames_taken.pop()
					total_frames.pop()
					inventory.pop()
					output_created.pop()
					legal_moves.pop()


					#Step back up a level
					step_index -= 1
				else:
					#Once the list is generated, choose the top-most (quickest) path and iterate downward
					written_step.append(legal_moves[step_index][0][0])
					frames_taken.append(legal_moves[step_index][0][2])
					total_frames.append(total_frames[step_index] + legal_moves[step_index][0][2])
					inventory.append(legal_moves[step_index][0][3])
					output_created.append(copy.copy(output_created[step_index]))


					if(legal_moves[step_index][0][1] >= 0):
						output_created[step_index + 1][legal_moves[step_index][0][1]-1] = True


					step_index += 1
			else:
				#Pop the 1st instance of the list, as it has already been recursed down
				legal_moves[step_index].pop(0)


				#Filter out all legal moves that would exceed the current frame limit
				legal_moves[step_index] = list(filter(lambda x: x[2]+total_frames[step_index] < frame_record, legal_moves[step_index]))


				#Just because, if the step index is sufficiently small, just shuffle!
				if(randomize):
					if(step_index < 20):
						random.shuffle(legal_moves[step_index])


				if(len(legal_moves[step_index]) == 0):
					#No legal moves are left to evaluate, go back up...
					#Wipe away the current state
					written_step.pop()
					frames_taken.pop()
					total_frames.pop()
					inventory.pop()
					output_created.pop()
					legal_moves.pop()


					#Step back up a level
					step_index -= 1
				else:
					#Once the list is generated, choose the top-most (quickest) path and iterate downward
					written_step.append(legal_moves[step_index][0][0])
					frames_taken.append(legal_moves[step_index][0][2])
					total_frames.append(total_frames[step_index] + legal_moves[step_index][0][2])
					inventory.append(legal_moves[step_index][0][3])
					output_created.append(copy.copy(output_created[step_index]))


					if(legal_moves[step_index][0][1] >= 0):
						output_created[step_index + 1][legal_moves[step_index][0][1]-1] = True


					step_index += 1
					#logging for progress display
					if(log_calls):
						if(iteration_count % 100000 == 0):
							print("{0} Steps taken using {1} frames; {2}k iterations; call {3}".format(step_index, total_frames[step_index], iteration_count / 1000, call_number))	
					iteration_count += 1
	
	

print('roadmap defined')
import os
from cx_Freeze import setup, Executable

build_exe_options = {"build_exe": ".\\build\\"}

recipesAtHome = Executable(script="start.py", targetName="RecipesAtHome.exe",
						   icon='mistake.ico')

setup(name = "Recipes@Home",
	  description = "Program to find good recipe routes for the 100% TAS",
	  options = {"build_exe": build_exe_options},
	  executables = [recipesAtHome])

directories = ["build/itemSorts", "build/results"]

extra_files = ["config.txt", "inventory.txt", "README.md", "recipes-JP.txt",
			   "itemSorts/alphabetic_sort-JP.txt",
			   "itemSorts/type_sort-JP.txt", "results/readme.md"]

for directory in directories:
	if not os.path.isdir(directory):
		os.mkdir(directory)

for infile in extra_files:
	infile_contents = open(infile, "r").read()
	outfile = infile[:-2] + "txt" if infile.endswith("md") else infile
	with open("build/" + outfile, "w", newline="\r\n") as f:
		f.write(infile_contents)

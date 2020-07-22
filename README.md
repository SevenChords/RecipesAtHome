# hundoRecipeCalculation

Script for calculating the order in which recipes are cooked for the 100% tas

# Requirements

If you wish to run using the source directly, you will need:
0. Python 3. Tested on 3.6.X and 3.8.3.
1. `pip`

# How to run

0. `git clone` or unzip the release to a directory of your choice.
1. Edit `config.txt` to your liking. Pay special attention to `workerCount` and `Username`
2. `pip install requests`
3. `python start.py`

Output goes to the `results` folder, with the number of frames the solution takes. Results are uploaded to a remote server when a new record is determined.
import os
import pathlib
from keys_actions import key_action

path = input("What's your .klang file path?\n")
with open(path) as f:
	lines = f.readlines() #get all the lines of the file in an array

for l in lines:
	keys = l.split(" ") #split all into keywords
	for k in keys:
		print(k)
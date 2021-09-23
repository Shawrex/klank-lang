import keys_actions as ka

path = input("What's your .klang file path?\n")
with open(path) as f:
	lines = f.readlines() #get all the lines of the file in an array

for l in lines:
	keys = l.split(" ") #split all into keywords

	if keys[0] == ka.PRINT:
		print = keys.pop(0)
		keys.append(print)
	
	if keys[0] == ka.VAR:
		var = keys.pop(0)
		name = keys.pop(0)
		keys.extend([var, name])

	index = 0
	for k in keys:
		ka.key_action(key=k.rstrip("\n"), index=index)
		index = index + 1
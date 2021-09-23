####################################
# DICT
####################################
BACKLINE = ';'
QUOTES = '"'

VAR = 'var'
PRINT = 'print:'



####################################
# VARS
####################################
vars = {}
inVar = False

inString = False
currentString = []
lastString = ""



####################################
# ACTIONS
####################################
def key_action(key: str, index: int):
	global vars, inVar
	global inString, currentString, lastString

	if index == 0:
		currentString = []
		lastString = ""

	#REGISTERING VARS
	if key == VAR:
		inVar = True
		return
	elif inVar:
		vars.update({key: lastString})
		inVar = False
		return



	#LITTERAL STRING EDITS
	if key.endswith(QUOTES):
		currentString.append(key.strip(QUOTES))
		inString = False
		lastString = " ".join(currentString)
		currentString = []
		return
	elif key.startswith(QUOTES):
		currentString.append(key.strip(QUOTES))
		inString = True
		return
	elif inString:
		currentString.append(key)
		return
	


	#ACTIONS
	if key in vars:
		lastString = vars[key]
		return

	if key == PRINT:
		print(lastString)
		lastString = ""
		return

	

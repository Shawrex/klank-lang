####################################
# DICT
####################################
BACKLINE = ';'
QUOTES = '"'
TRUE = 'true'
FALSE = 'false'

VAR = 'var'
PRINT = 'print:'



####################################
# VARS
####################################
cacheVar = None

vars = {}
inVar = False

inString = False
currentString = []



####################################
# ACTIONS
####################################
def key_action(key: str, index: int):
	global cacheVar
	global vars, inVar
	global inString, currentString

	if index == 0:
		currentString = []
		cacheVar = None



	#REGISTERING VARS
	if key == VAR:
		inVar = True
		return
	elif inVar:
		vars.update({key: cacheVar})
		inVar = False
		return



	#LITTERAL VARS WRITING
	if key == TRUE:
		cacheVar = True
		return
	elif key == FALSE:
		cacheVar = False
		return

	elif key.isnumeric(): #is an int
		cacheVar = int(key)
		return

	elif key.endswith(QUOTES): #is an string
		currentString.append(key.strip(QUOTES))
		inString = False
		cacheVar = " ".join(currentString)
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
		cacheVar = vars[key]
		return

	if key == PRINT:
		print(cacheVar)
		cacheVar = ""
		return

	

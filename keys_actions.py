####################################
# DICT
####################################
BACKLINE = ';'
QUOTES = '"'

PRINT = 'print:'



####################################
# ACTIONS
####################################
inString = False
currentString = []



####################################
# ACTIONS
####################################
def key_action(key: str):

	if (key.startswith(QUOTES)):
		inString = True
		key.lstrip(QUOTES)
		#will fall and return in the inString check
		
	if (key.endswith(QUOTES)):
		currentString.append(key)
		inString = False
		key.rstrip(QUOTES)
		print(currentString)
		return

	if (inString):
		currentString.append(key)
		return


	

"""
TOKEN TYPES
"""
TT_EOL = 	'EOL'
TT_VAR =	'VARIABLE'
TT_INT =	'INTEGER'
TT_STRING =	'STRING'
TT_OP =		'OPERATOR'
TT_SYMBOL =	'SYMBOL'
TT_METHOD =	'METHOD'



"""
LEXIC
"""
Digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
Quote = '"'
Plus, Minus = '+', '-'
Print = 'Print:'



"""
TOKEN DEFINITION
"""
class Token(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value
	
	def __str__(self):
		return f"Token(t:{self.type}, v:{self.value})"
	

"""
LEXER
"""
class Lexer(object):
	def __init__(self, text):
		self.text = text

		self.pos = 0
		self.current_char = self.text[self.pos]

	def step(self):
		self.pos += 1
		if self.pos >= len(self.text):
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]
		
	def revert(self):
		self.pos += 1
		self.current_char = self.text[self.pos]

	def get_all_tokens(self):
		tokens = []

		while self.current_char is not None:
			ch = self.current_char

			if ch.isspace():
				#skip spaces
				self.skip_spaces()

			if ch in Digits:
				#then character is an int token
				tokens.append(Token(TT_INT, self.build_int()))

			if ch in (Plus, Minus):
				#token is an operator
				self.step()
				tokens.append(Token(TT_OP, ch))

			if ch == Quote:
				#then character is a string token
				tokens.append(Token(TT_STRING, self.build_string()))

			""" METHODS """
			if ch == 'P':
				#might be Print ?
				if (self.build_method_name(Print)):
					#is Print !
					self.step()
					tokens.append(Token(TT_METHOD, Print))
			else:
				self.step()
				
			
		return tokens

	def skip_spaces(self):
		while self.current_char.isspace():
			self.step()
	
	def build_int(self):
		result = ''
		while self.current_char is not None and self.current_char in Digits:
			result += self.current_char
			self.step()
		return int(result)

	def build_string(self):
		result = ''
		self.step() #do not count the first quote
		while self.current_char is not None and self.current_char is not Quote:
			result += self.current_char
			self.step()
		self.step() #skip the last
		return result
	
	def build_method_name(self, target_method_name):
		current = ''
		delta = 0
		while current in target_method_name:
			current += self.current_char
			self.step()
			delta += 1
			if current == target_method_name:
				return True

		#if breaks out then it's not the appropriate method name
		for i in range(0, delta):
			self.revert()
		return False
		




"""
INTERPRETER
"""
class Interpreter(object):
	def __init__(self, lexer):
		self.tokens = lexer.get_all_tokens()
		for t in self.tokens:
			print(t)

	def execute_tokens(self):
		#execute the tokens depending simple rules
		pass
				

Interpreter(Lexer('Print: "355"'))


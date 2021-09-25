"""
TOKEN TYPES
"""
TT_EOL = 		'EOL'
TT_VAR =		'VARIABLE'
TT_INT =		'INTEGER'
TT_STRING =		'STRING'
TT_OP =			'OPERATOR'
TT_KWORD =		'KEYWORD'
TT_SYMBOL =		'SYMBOL'
TT_METHOD =		'METHOD'



"""
LEXIC
"""
Var = 'Var'
Digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
Quote, Comparison, Then = '"', ':=', '>>'
Equal, Plus, Minus = '=', '+', '-'
Print, Test = 'Print:', 'Test:'

vars = {}



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
		self.pos -= 1
		self.current_char = self.text[self.pos]

	def get_all_tokens(self):
		tokens = []

		while self.current_char is not None:
			ch = self.current_char

			if ch.isspace():
				#skip spaces
				self.skip_spaces()

			elif ch in Digits:
				#then character is an int token
				tokens.append(Token(TT_INT, self.build_int()))

			elif ch in (Plus, Minus):
				#token is an operator
				self.step()
				tokens.append(Token(TT_OP, ch))

			elif ch == Quote:
				#then character is a string token
				tokens.append(Token(TT_STRING, self.build_string()))
			
			elif ch == Equal:
				#equal token
				self.step()
				tokens.append(Token(TT_SYMBOL, Equal))
				
			elif ch == 'V':
				#Var ?
				if (self.build_misc_name(Var)):
					self.step()
					tokens.append(Token(TT_KWORD, Var))

			elif ch == 'P':
				#Print?
				if (self.build_misc_name(Print)):
					self.step()
					tokens.append(Token(TT_METHOD, Print))

			elif ch == 'T':
				#Test ?
				if (self.build_misc_name(Test)):
					self.step()
					tokens.append(Token(TT_METHOD, Test))
			
			elif ch == '>':
				#Then ?
				if (self.build_misc_name(Then)):
					self.step()
					tokens.append(Token(TT_SYMBOL, Then))
			
			elif ch == ':':
				#Comparison ?
				if (self.build_misc_name(Comparison)):
					self.step()
					tokens.append(Token(TT_SYMBOL, Comparison))
			
			else: 
				#make a variable name
				tokens.append(Token(TT_VAR, self.build_var_name()))
			
		return tokens



	def skip_spaces(self):
		while self.current_char is not None and self.current_char.isspace():
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
	
	def build_misc_name(self, target_method_name):
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
	
	def build_var_name(self):
		result = ''
		while self.current_char is not None and not self.current_char.isspace():
			result += self.current_char
			self.step()
		return result
		




"""
INTERPRETER
"""
class Interpreter(object):
	def __init__(self, lexer):
		self.lexer = lexer
		self.tokens = self.lexer.get_all_tokens()

		self.pos = 0
		self.current_token = self.tokens[self.pos]
	
	def print_tokens(self):
		for token in self.tokens:
			print(token)

	def error(self):
		raise Exception('Interpreting error')
	
	def step(self):
		self.pos += 1
		if self.pos >= len(self.tokens):
			self.current_token = Token(TT_EOL, None)
		else:
			self.current_token = self.tokens[self.pos]

	def execute_tokens(self):
		while self.current_token is not None and self.current_token.type is not TT_EOL:

			if self.current_token.type == TT_KWORD:
				#Is a keyword like Var
				token = self.current_token

				if token.value == Var:
					self.step()
					self.make_variable()


			if self.current_token.type == TT_METHOD:
				#Is a method, check depending what the method does
				token = self.current_token

				if token.value == Print:
					self.step()
					printable = self.make_string()
					print(printable)
				
				if token.value == Test: 
					self.step()
					if self.make_test():
						self.step() if self.current_token.value == Then else self.error()
					else:
						break
	


	def make_variable(self):
		if self.current_token.type is not TT_VAR:
			self.error()
		name = self.current_token.value
		self.step()

		if self.current_token.value is not Equal:
			self.error()
		self.step()

		if self.current_token.type is TT_INT:
			value = self.make_int()
		elif self.current_token.type is TT_STRING:
			value = self.current_token.value
			self.step()
		else:
			self.error()

		vars.update({name: value})

	def make_string(self):
		result = ''
		while self.current_token.type is not None and self.current_token.type in (TT_INT, TT_STRING, TT_VAR):
			token = self.current_token

			if token.type == TT_INT:
				result += str(self.make_int())
			elif token.type == TT_STRING:
				result += token.value
			else:
				if token.value not in vars:
					self.error()
				result += str(vars[token.value])
			result += ' '
			self.step()

		if result == '':
			self.error()
		else:
			return result
	
	def make_int(self):
		result = self.current_token.value
		self.step()
		while self.current_token.type == TT_OP:
			token = self.current_token
			if token.value == Plus:
				self.step()
				result += self.current_token.value
			else:
				self.step()
				result += self.current_token.value
			self.step()
		return result
	
	def make_test(self):
		#get first value:
		if self.current_token.type == TT_INT:
			left = self.make_int()
		elif self.current_token.type == TT_STRING:
			left = self.current_token.value
			self.step()
		elif self.current_token.type == TT_VAR:
			if self.current_token.value not in vars:
				self.error()
			left = vars[self.current_token.value]
			self.step()
		else:
			self.error()

		#get test:
		if self.current_token.value == Comparison:
			self.step()
		else:
			self.error()

		#get the second value
		if self.current_token.type == TT_INT:
			right = self.make_int()
		elif self.current_token.type == TT_STRING:
			right = self.current_token.value
			self.step()
		elif self.current_token.type == TT_VAR:
			if self.current_token.value not in vars:
				self.error()
			right = vars[self.current_token.value]
			self.step()
		else:
			self.error()

		#do the test
		if left == right:
			return True
		else:
			return False



"""
MAIN LOOP
"""
def main():
	path = input('klank file Path >>> ')
	with open(path) as f:
		lines = f.readlines()

	for text in lines:
		lexer = Lexer(text)
		inter = Interpreter(lexer)
		inter.print_tokens()
		inter.execute_tokens()

	input('\n\nPress enter to finish...')

if __name__ == "__main__":
    main()

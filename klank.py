"""
TOKEN TYPES
"""
TT_EOL = 		'EOL'
TT_VAR =		'VARIABLE'
TT_INT =		'INTEGER'
TT_STRING =		'STRING'
TT_OP =			'OPERATOR'
TT_KWORD =		'KEYWORD'
TT_BRACK =		'BRACKETS'
TT_SYMBOL =		'SYMBOL'
TT_METHOD =		'METHOD'



"""
LEXIC
"""
Eol = ';'
Var = 'var'
Digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
L_Paranth, R_Paranth = '(', ')'
L_Curl, R_Curl = '{', '}'
Quote, Comparison = '"', '=='
Equal, Plus, Minus = '=', '+', '-'
Print, If = 'print', 'if'

vars = {}
BannedChars = (Eol, L_Paranth, R_Paranth, L_Curl, R_Curl, Quote, Equal, Plus, Minus)



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
				continue

			if ch == Eol:
				self.step()
				tokens.append(Token(TT_EOL, Eol))
				continue
				
			if ch == Var[0]:
				#Var ?
				if (self.build_misc_name(Var)):
					tokens.append(Token(TT_KWORD, Var))
					continue

			if ch == Print[0]:
				#Print?
				if (self.build_misc_name(Print)):
					tokens.append(Token(TT_METHOD, Print))
					continue

			if ch == If[0]:
				#Test ?
				if (self.build_misc_name(If)):
					tokens.append(Token(TT_METHOD, If))
					continue
			
			if ch == Comparison[0]:
				#Comparison ?
				if (self.build_misc_name(Comparison)):
					tokens.append(Token(TT_SYMBOL, Comparison))
					continue

			if ch in Digits:
				#then character is an int token
				tokens.append(Token(TT_INT, self.build_int()))
				continue

			if ch in (Plus, Minus):
				#token is an operator
				self.step()
				tokens.append(Token(TT_OP, ch))
				continue

			if ch == Quote:
				#then character is a string token
				tokens.append(Token(TT_STRING, self.build_string()))
				continue
			
			if ch == Equal:
				#equal token
				self.step()
				tokens.append(Token(TT_SYMBOL, Equal))
				continue
			
			if ch == L_Paranth:
				#left parathesis
				self.step()
				tokens.append(Token(TT_BRACK, L_Paranth))
				continue
				
			if ch == R_Paranth:
				#right parathesis
				self.step()
				tokens.append(Token(TT_BRACK, R_Paranth))
				continue
				
			if ch == L_Curl:
				#left curly bracket
				self.step()
				tokens.append(Token(TT_BRACK, L_Curl))
				continue
				
			if ch == R_Curl:
				#right curly bracket
				self.step()
				tokens.append(Token(TT_BRACK, R_Curl))
				continue
			
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
		while self.current_char is not None and not self.current_char.isspace() and not self.current_char in BannedChars:
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

		self.depth = 0 #keep track of the level of { }
		self.memory_depth = 0
	
	def print_tokens(self):
		for token in self.tokens:
			print(token)
		print("\nFinished printing tokens...\n")

	def error(self):
		raise Exception('Interpreting error')
	
	def step(self):
		self.pos += 1
		if self.pos >= len(self.tokens):
			self.current_token = Token(TT_EOL, None)
		else:
			self.current_token = self.tokens[self.pos]
	
	def eat_type(self, type):
		token = self.current_token
		if token.type == type:
			self.step()
			return token
		else:
			self.error()
		
	def eat_value(self, value):
		token = self.current_token
		if token.value == value:
			self.step()
			return token
		else:
			self.error()
	
	def level_down(self):
		while self.current_token.value == R_Curl:
			self.step()
			self.depth -= 1
		if self.depth < 0:
			self.error()

	def execute_tokens(self):
		while self.current_token is not None and self.current_token.value is not None:

			if self.current_token.type == TT_KWORD:
				#Is a keyword like Var
				token = self.current_token

				if token.value == Var: # 'var i = 6;'
					self.step()
					self.make_variable()


			if self.current_token.type == TT_METHOD:
				#Is a method, check depending what the method does
				token = self.current_token

				if token.value == Print: # 'print("something");'
					self.step()
					self.eat_value(L_Paranth)
					printable = self.make_string()
					self.eat_value(R_Paranth)
					self.eat_type(TT_EOL)
					print(printable)
					self.level_down()
				
				if token.value == If: # 'if(1:=1){print("something")};'
					self.step()
					self.eat_value(L_Paranth)
					if self.make_test():
						self.eat_value(R_Paranth)
						self.eat_value(L_Curl)
						self.depth += 1
					else: 								##################### A REVOIR
						self.memory_depth = self.depth
						while self.current_token.value is not R_Curl and self.depth != self.memory_depth:
							if self.current_token.value == L_Curl:
								self.depth += 1
								print(self.depth - self.memory_depth)
							elif self.current_token.value == R_Curl:
								self.depth -= 1
								print(self.depth - self.memory_depth)
							self.step()
					self.level_down()

	


	def make_variable(self): # 'i = 6;'
		name = self.eat_type(TT_VAR).value # = 6;

		self.eat_value(Equal) # 6;

		if self.current_token.type is TT_INT:
			value = self.make_int()
		elif self.current_token.type is TT_STRING:
			value = self.eat_type(TT_STRING).value
		self.eat_type(TT_EOL)

		vars.update({name: value})

	def make_string(self):
		result = ''
		while self.current_token.type is not None and self.current_token.type in (TT_INT, TT_STRING, TT_VAR):
			token = self.current_token

			if token.type == TT_INT:
				result += str(self.make_int())
			elif token.type == TT_STRING:
				result += token.value
				self.step()
			else:
				if str(token.value) not in vars:
					self.error()
				result += str(vars[token.value])
				self.step()
			result += ' '

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
		self.eat_value(Comparison)

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
	text = ' '.join(lines)

	lexer = Lexer(text)
	inter = Interpreter(lexer)
	inter.print_tokens()
	inter.execute_tokens()

	input('\n\nPress enter to finish...')

if __name__ == "__main__":
    main()

from lexic import *



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
	
	def error(self):
		raise Exception('Interpreting error')

	def step(self):
		self.pos += 1
		if self.pos >= len(self.text):
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]
		
	def revert(self):
		self.pos -= 1
		self.current_char = self.text[self.pos]
	
	def peek(self, char):
		self.step()
		if self.current_char == char:
			return char
		else:
			self.revert()
			return None

	def get_all_tokens(self):
		tokens = []

		while self.current_char is not None:
			while self.current_char is not None and self.current_char.isspace():
				self.step()	#skip spaces
			
			token = self.create_token(self.current_char)
			self.step()

			if token.type is not None:
				tokens.append(token)
				continue

			sw = {
				Print: TT_METHOD,
				While: TT_METHOD,
				Var: TT_KWORD,
				If: TT_KWORD,
				EqualTo: TT_COMP, 
				DifferentThan: TT_COMP, 
				MoreThan: TT_COMP, 
				LessThan: TT_COMP, 
				MultipleOf: TT_COMP
			}
			token.type = sw.get(token.value)
			tokens.append(token)
			
		return tokens
	
	def create_token(self, char:str):
		current = char

		if current.isdigit():
			return Token(TT_INT, self.build_int())
		
		if current == Quote:
			return Token(TT_STRING, self.build_string())
		
		for k in Lexic:
			while current in k:
				if current == k:
					return Token(None, current)
				next = self.peek(k[len(current)])
				if next == None:
					break
				current += next
			current = char
		
		return Token(TT_VAR, self.build_var_name())
	
	def build_int(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.step()
		return int(result)

	def build_string(self):
		result = ''
		self.step() #do not count the first quote
		while self.current_char is not None and self.current_char is not Quote:
			result += self.current_char
			self.step()
		return result
	
	def build_var_name(self):
		result = ''
		while self.current_char is not None and not self.current_char.isspace() and not self.current_char in BannedChars:
			result += self.current_char
			self.step()
		self.revert()
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
		print("\nFinished printing tokens...\n")





"""
MAIN LOOP
"""
def main():
	path = input('klank file Path >>> ')
	with open(path) as f:
		lines = f.readlines()
	text = ' '.join(lines)

	lexer = Lexer(text)
	interpeter = Interpreter(lexer)
	interpeter.print_tokens()

	input('\n\nPress enter to finish...')

if __name__ == "__main__":
    main()

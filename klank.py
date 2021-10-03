from lexic import *
from token_execution import Token_Executer



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
			if self.current_char is None:
				break

			token = self.create_token()
			self.step()

			if token.type is not None:
				tokens.append(token)
				continue

			sw = {
				Print: TT_METHOD,
				While: TT_METHOD,
				Else: TT_KWORD,
				Var: TT_KWORD,
				If: TT_KWORD,
				EqualTo: TT_COMP,
				DifferentThan: TT_COMP,
				MoreThan: TT_COMP,
				LessThan: TT_COMP,
				MultipleOf: TT_COMP,
				Equal: TT_SYMBOL,
				Plus: TT_OP,
				Minus: TT_OP,
				L_Paranth: TT_BRACK,
				R_Paranth: TT_BRACK,
				L_Curl: TT_BRACK,
				R_Curl: TT_BRACK
			}
			token.type = sw.get(token.value)
			tokens.append(token)

		return tokens

	def create_token(self):
		char = self.current_char
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
		self.revert()
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

		self.depth = 0

	def error(self, type):
		if type == "eat":
			issue = f"Issue while eating, check upper logs. Issue is : {self.current_token} at position : {self.pos}"
		elif type == "unexpected_token":
			issue = f"No idea what you meant there buddy. Issue is : {self.current_token} at position : {self.pos}"
		else:
			issue = "Unknown issue raised."
		raise Exception(issue)

	def print_tokens(self):
		for token in self.tokens:
			print(token)
		print("\nFinished printing tokens...\n")

	def step(self):
		self.pos += 1
		if self.pos >= len(self.tokens):
			self.current_token = Token(TT_EOF, None)
		else:
			self.current_token = self.tokens[self.pos]

	def revert(self):
		self.pos -= 1
		if self.pos < 0:
			self.current_token = Token(None, None)
		else:
			self.current_token = self.tokens[self.pos]

	def eat(self, comp):
		token = self.current_token
		if comp == TT_VALUE and token.type in TT_VALUE:
			self.step()
			return token
		if comp == token.type or comp == token.value:
			self.step()
			return token
		else:
			print(f"Checked was:{comp}, but it was actually a {token}")
			self.error("eat")
	
	def englobe(self):
		tokens = []
		depth = self.depth
		self.depth += 1
		while self.depth != depth:
			if self.current_token.value == L_Curl:
				self.depth += 1
			elif self.current_token.value == R_Curl:
				self.depth -= 1
			tokens.append(self.current_token)
			self.step()
		self.revert()
		return tokens

	def build_token_list(self, comps):
		tokens = []
		for comp in comps:
			tokens.append(self.eat(comp))
		return tokens

	def execute_tokens(self):
		while self.current_token is not None and self.current_token.type is not TT_EOF:
			"""
			THIS IS AN IMPORTANT PART
			"""
			token = self.current_token

			if token.type == TT_VAR:
				# example = 42;
				expression = self.build_token_list([TT_VAR, Equal, TT_VALUE, Eol])
				Token_Executer("set_var", expression)
				continue

			if token.value == Var:
				# var example = 42;
				expression = self.build_token_list([Var, TT_VAR, Equal, TT_VALUE, Eol])
				Token_Executer("new_var", expression)
				continue
				
			if token.value == Print:
				# print(example);
				expression = self.build_token_list([Print, L_Paranth, TT_VALUE, R_Paranth, Eol])
				Token_Executer("print", expression)
				continue
				
			if token.value == If:
            	# if(example==42) { print("hello"); }
				expression = self.build_token_list([If, L_Paranth, TT_VALUE, TT_COMP, TT_VALUE, R_Paranth, L_Curl])
				expression.append(self.englobe())
				expression.append(self.eat(R_Curl))
				if self.current_token.value == Else:
					expression.extend(self.build_token_list([Else, L_Curl]))
					expression.append(self.englobe())
					expression.append(self.eat(R_Curl))
				Token_Executer("if_statement", expression)

			else:
				self.error("unexpected_token")





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
	#interpeter.print_tokens()
	interpeter.execute_tokens()

	##input('\n\nPress enter to finish...')

if __name__ == "__main__":
    main()

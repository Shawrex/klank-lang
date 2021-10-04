from lexic import *

"""
Token Execution Center
"""
class Token_Executer(object):
    def __init__(self, type, tokens):
        self.tokens = tokens
        self.type = type

        self.expression()

    def error(self):
        raise Exception(f"There was an issue executing '{self.type}'")

    def extract_value(self, token):
        if token.type == TT_INT or token.type == TT_STRING:
            value = token.value
        else:
            value = vars[token.value]
        return value
    
    def run_test(self, a, comp, b):
        if comp == EqualTo:
            return True if a == b else False
        elif comp == DifferentThan:
            return True if a != b else False
        elif comp == MoreThan:
            return True if a > b else False
        elif comp == LessThan:
            return True if a < b else False
        elif comp == MultipleOf:
            return True if a % b == 0 else False

    def expression(self):
        if self.type == "set_var":
            # example = 42;
            name = self.tokens[0].value
            if name in vars:
                vars.update({name: self.extract_value(self.tokens[2])})
            else:
                self.error()
            return

        if self.type == "new_var":
            # var example = 42;
            vars.update({self.tokens[1].value: self.extract_value(self.tokens[3])})
            return

        if self.type == "print":
            # print(example);
            print(self.extract_value(self.tokens[2]))
            return
        
        if self.type == "if_statement":
            # if(example==42) { print("hello"); } else { print("goodbye!"); }
            a = self.extract_value(self.tokens[2])
            comp = self.tokens[3].value
            b = self.extract_value(self.tokens[4])

            from klank import Interpreter, Lexer
            inte = Interpreter(Lexer("("))

            if self.run_test(a, comp, b):
                inte.tokens = self.tokens[7]
            elif len(self.tokens) > 9:
                inte.tokens = self.tokens[11]
            else:
                return

            inte.current_token = inte.tokens[0]
            inte.execute_tokens()
            return
        
        if self.type == "while_loop":
			# while(i==42) { print("hello!"); }
            a = self.extract_value(self.tokens[2])
            comp = self.tokens[3].value
            b = self.extract_value(self.tokens[4])

            from klank import Interpreter, Lexer
            inte = Interpreter(Lexer("("))
            inte.tokens = self.tokens[7]

            while self.run_test(a, comp, b):
                inte.pos = 0
                inte.current_token = inte.tokens[inte.pos]
                inte.execute_tokens()
                
                a = self.extract_value(self.tokens[2])
                b = self.extract_value(self.tokens[4])
            
            return
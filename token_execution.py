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
        else:
            return True if a != b else False

    def expression(self):
        if self.type == "set_var":
            # example = 42;
            name = self.tokens[0].value
            if name in vars:
                vars.update({name: self.tokens[2].value})
            else:
                self.error()

        if self.type == "new_var":
            # var example = 42;
            vars.update({self.tokens[1].value: self.extract_value(self.tokens[3])})

        if self.type == "print":
            # print(example);
            print(self.extract_value(self.tokens[2]))
        
        if self.type == "if_statement":
            # if(example==42) { print("hello"); }
            a = self.extract_value(self.tokens[2])
            comp = self.tokens[3].value
            b = self.extract_value(self.tokens[4])
            if self.run_test(a, comp, b):
                from klank import Interpreter, Lexer
                inte = Interpreter(Lexer("("))
                inte.tokens = self.tokens[7:len(self.tokens)-2]
                #inte.print_tokens()

            

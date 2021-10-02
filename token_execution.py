from lexic import vars

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

    def expression(self):
        if self.type == "set_var":
            name = self.tokens[0].value
            if name in vars:
                vars.update({name: self.tokens[2].value})
            else:
                self.error()

        if self.type == "new_var":
            vars.update({self.tokens[1].value: self.tokens[3].value})

"""
TOKEN TYPES
"""
TT_EOF = 		'EOF'
TT_EOO =		'EOO'
TT_VAR =		'VARIABLE'
TT_INT =		'INTEGER'
TT_STRING =		'STRING'
TT_VALUE =		(TT_VAR, TT_INT, TT_STRING)
TT_OP =			'OPERATOR'
TT_KWORD =		'KEYWORD'
TT_BRACK =		'BRACKETS'
TT_COMP =		'COMPARISON'
TT_SYMBOL =		'SYMBOL'
TT_METHOD =		'METHOD'



"""
LEXIC
"""
Eol = ';'
Var = 'var'
L_Paranth, R_Paranth = '(', ')'
L_Curl, R_Curl = '{', '}'
Quote = '"'
EqualTo, DifferentThan, MoreThan, LessThan, MultipleOf = '==', '!=', '>', '<', '%='
Equal, Plus, Minus = '=', '+', '-'
Print, If, While = 'print', 'if', 'while'

vars = {}
BannedChars = (Eol, L_Paranth, R_Paranth, L_Curl, R_Curl, Quote, Equal, Plus, Minus, '!')

Lexic = [While, Print,																	#5 letters
		Var,																			#3
		EqualTo, DifferentThan, MoreThan, LessThan, MultipleOf, If,						#2
		Eol, L_Paranth, R_Paranth, L_Curl, R_Curl, Quote, Equal, Plus, Minus]			#1


from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal, Union

class TOKEN(Enum):
    PLUS = "+"
    MINUS = "-"
    ASTERISK = "*"
    LPAREN = "("

STR_TO_TOK = {tok.value: tok for tok in TOKEN}

class PRECEDENCE(Enum):
    LOWEST = auto()
    EQUALS = auto()
    LESSGREATER = auto()
    SUM = auto()
    PRODUCT = auto()
    PREFIX = auto()
    CALL = auto()

PRECEDENCES = {
    TOKEN.PLUS: PRECEDENCE.SUM,
    TOKEN.MINUS: PRECEDENCE.SUM,
    TOKEN.ASTERISK: PRECEDENCE.PRODUCT
}

@dataclass
class Expression:
    left: Union[Expression, Literal] = None
    right: Union[Expression, Literal] = None
    operator: TOKEN = None


# @dataclass
# class PrefixExpression():
#     token: TOKEN
#     right: Union[PrefixExpression, InfixExpression]

class StatementParser:

    def __init__(self, input_str):
    
        self.tokens = [STR_TO_TOK.get(str_tok, str_tok) for str_tok in input_str.split(" ")]
        self.cur_token_pos = 0

        self.ast = self.parse_expression(PRECEDENCE.LOWEST)

    def next_token(self): self.cur_token_pos += 1

    def parse_infix_expression(self, left: TOKEN):
        expr = Expression(left=left, operator=self.tokens[self.cur_token_pos])
        cur_precedence = PRECEDENCES[self.tokens[self.cur_token_pos]]
        self.next_token()
        expr.right = self.parse_expression(cur_precedence)
        return expr

    def parse_expression(self, precedence: PRECEDENCE):
        left = self.tokens[self.cur_token_pos]
        self.next_token()
        while (self.cur_token_pos < len(self.tokens)-1) and (PRECEDENCES[self.tokens[self.cur_token_pos]].value > precedence.value):
            left = self.parse_infix_expression(left)
        return left


    def print_statement(self):
        
        def print_ast_node(node: Expression, indent=0):
            if type(node.left) == Expression:
                print_ast_node(node.left, indent+1)
            else:
                print('\t'*indent + node.left)

            print('\t'*indent + node.operator.value)
            
            if type(node.right) == Expression:
                print_ast_node(node.left, indent+1)
            else:
                print('\t'*indent + node.right)
                    
        print_ast_node(self.ast)


if __name__ == "__main__":
    while True:
        str_expression = input("Enter expression: ")
        if str_expression:
            parser = StatementParser(str_expression)
            parser.print_statement()
            
        else:
            break
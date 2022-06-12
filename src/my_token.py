from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    INTEGER = auto()
    REAL = auto()
    OPERATORS = auto()
    KEYWORD = auto()
    ID = auto()
    EOF = auto()
    NOTTERMINAL = auto()
    


@dataclass
class Token(object):
    type: TokenType = TokenType.ID
    value: str = ''
    
    def __str__(self):
        return f'Token({self.type}, \'{self.value}\')'

    def __repr__(self):
        return self.__str__()
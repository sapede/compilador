from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    INT = auto()
    REAL = auto()
    OPERATORS = auto()
    KEYWORD = auto()
    ID = auto()
    EOF = auto()
    NOTTERMINAL = auto()
    


@dataclass()
class Token(object):
    type: TokenType = TokenType.ID
    value: str = ''
    
    def __str__(self) -> str:
        return f'Token({self.type}, \'{self.value}\')'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.value == other.value

    def __hash__(self) -> int:
        return hash(tuple([self.value, str(self.type)]))

    def __lt__(self, other):
        return self.value < other.value
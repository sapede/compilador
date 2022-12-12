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
    NEW_LINE = auto()
    SPACE = auto()
    
class GenereteIds:
    def __init__(self):
        types = [t.name for t in TokenType]
        ids = [0 for t in TokenType]
        self.ids = dict(zip(types, ids))
    
    def generate(self, type):
        self.ids[type.name] += 1
        return self.ids[type.name]

@dataclass()
class Token(object): 
    type: TokenType = TokenType.ID
    value: str = ''
    generator : GenereteIds = GenereteIds()

    def __post_init__(self):
        self.id = self.generator.generate(self.type)
        self.value_id = str(self.value) + str(self.id)

    def __str__(self) -> str:
        return f'Token({self.type}, \'{self.value}\')'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value

    def __hash__(self) -> int:
        return hash(tuple([self.value, str(self.type)]))

    def __lt__(self, other):
        return self.value < other.value


    @staticmethod
    def EOF():
        return Token(TokenType.EOF, '$')

    @staticmethod
    def empty():
        return Token(TokenType.OPERATORS, 'λ')
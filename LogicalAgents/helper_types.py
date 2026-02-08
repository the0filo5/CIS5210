from enum import Enum, auto
from typing import FrozenSet, Tuple, Optional


Room = Tuple[int, int]
PossibleWorld = Tuple[FrozenSet[Room], Optional[Room]]


class Direction(Enum):
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right'


class Action(Enum):
    LEFT = 'left',
    RIGHT = 'right',
    FORWARD = 'forward',
    GRAB = 'grab',
    CLIMB = 'climb',
    SHOOT = 'shoot',


class Percept(Enum):
    STENCH = 'stench',
    BREEZE = 'breeze',
    GASP = 'gasp',
    BUMP = 'bump',
    SCREAM = 'scream',


class KeyboardAction(Enum):
    Up = auto()
    Left = auto()
    Right = auto()
    g = auto()
    c = auto()
    s = auto()
    Return = auto()

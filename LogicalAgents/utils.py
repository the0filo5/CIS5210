from helper_types import Direction, Room
from typing import Optional

orientation_to_delta = {
    Direction.UP: (0, 1),  # (dx, dy)
    Direction.DOWN: (0, -1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0)
}


def flatten(tup):
    if len(tup) == 1:
        return tup[0]
    return tup


def get_direction(degrees: int) -> Direction:
    fraction = (degrees % 360) / 360
    match fraction:
        case 0:
            return Direction.UP
        case 0.25:
            return Direction.RIGHT
        case 0.5:
            return Direction.DOWN
        case 0.75:
            return Direction.LEFT
        case _:
            raise ValueError(f'Invalid direction: {degrees}')


def is_facing_wampa(location: Room, direction: Direction, wampa: Optional[Room]) -> bool:
    """You may wish to use this in all_safe_next_actions"""
    if wampa is None:
        return False
    x, y = location
    wx, wy = wampa
    match direction:
        case Direction.UP:
            return wx == x and wy > y
        case Direction.DOWN:
            return wx == x and wy < y
        case Direction.LEFT:
            return wx < x and wy == y
        case Direction.RIGHT:
            return wx > x and wy == y

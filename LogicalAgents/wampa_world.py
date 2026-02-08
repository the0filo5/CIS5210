import sys
from scenarios import *
from agent import Agent
from helper_types import Action, Direction, Percept
from utils import get_direction, is_facing_wampa
from visualize_world import visualize_world


def fit_grid(grid, item):
    """Used for calculating breeze and stench locationsbased on pit and wampa
    locations."""
    grid_x, grid_y = grid
    x, y = item
    loc = []

    if x < grid_x - 1:
        loc += [[x + 1, y]]
    if x > 0:
        loc += [[x - 1, y]]
    if y < grid_y - 1:
        loc += [[x, y + 1]]
    if y > 0:
        loc += [[x, y - 1]]

    return loc


# ENVIRONMENT
class WampaWorld:
    def __init__(self, worldInit):
        self.gridsize = worldInit['grid']
        self.X = self.gridsize[0]
        self.Y = self.gridsize[1]
        self.wampa = worldInit['wampa']
        self.pits = worldInit['pits']
        self.luke = worldInit['luke']
        self.saved_luke = False
        self.wampa_alive = True
        self.is_playing = True
        self.game_score = 0
        self.agent_loc = (0, 0)
        self.agent_degrees = 0
        self.has_blaster = True

        # calculate breeze and stench locations
        breeze = []
        for pit in self.pits:
            breeze += fit_grid(self.gridsize, pit)
        stench = fit_grid(self.gridsize, self.wampa)

        # prepopulate grid with percepts
        self.grid = [
            [
                [
                    Percept.STENCH if [x, y] in stench else None,
                    Percept.BREEZE if [x, y] in breeze else None,
                    None,  # "gasp" index
                    None,  # "bump" index
                    None  # "scream" index
                ]
                for y in range(self.Y)
            ]
            for x in range(self.X)
        ]

        # set "gasp" percept at Luke's location
        self.grid[self.luke[0]][self.luke[1]][2] = Percept.GASP
        self.agent = Agent(self)

    def get_percepts(self):
        x, y = self.agent_loc
        return self.grid[x][y]

    def agent_orientation(self):
        return get_direction(self.agent_degrees)

    def turn_left(self):
        self.agent_degrees -= 90
        self.agent.direction = self.agent_orientation()

    def turn_right(self):
        self.agent_degrees += 90
        self.agent.direction = self.agent_orientation()

    def handle_forward_action(self):
        x, y = self.agent_loc
        # R2 moves forward from whatever direction he's facing
        moved = True
        orientation = get_direction(self.agent_degrees)
        movements = {
            Direction.UP: (0, 1),
            Direction.DOWN: (0, -1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0)
        }

        dx, dy = movements.get(orientation, (0, 0))
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < len(self.grid) and 0 <= new_y < len(self.grid[0]):
            self.agent_loc = (new_x, new_y)
            self.agent.loc = self.agent_loc
        else:
            moved = False

        if (self.get_location() == self.wampa and self.wampa_alive) or \
                self.get_location() in self.pits:
            self.game_score -= 1000
            self.is_playing = False

        percepts = self.get_percepts()
        percepts[3] = Percept.BUMP if not moved else None  # reset bump = None if no bump

    def handle_left_action(self):
        self.turn_left()
        percepts = self.get_percepts()
        percepts[3] = None  # cannot experience a bump upon a turn

    def handle_right_action(self):
        self.turn_right()
        percepts = self.get_percepts()
        percepts[3] = None  # cannot experience a bump upon a turn

    def handle_shoot_action(self):
        self.game_score -= 10
        if not self.has_blaster:
            raise ValueError("R2-D2 had already used the blaster")

        self.has_blaster = False
        self.agent.blaster = False

        if not is_facing_wampa(self.agent_loc, self.agent_orientation(), self.wampa):
            return

        self.wampa_alive = False
        self.wampa = None
        for x in range(self.gridsize[0]):
            for y in range(self.gridsize[1]):
                self.grid[x][y][4] = Percept.SCREAM  # scream everywhere
                self.grid[x][y][0] = None  # stench is gone

    def handle_grab_action(self):
        if self.get_location() == self.luke and not self.saved_luke:
            self.agent.has_luke = True
            self.saved_luke = True
            self.luke = None

    def handle_climb_action(self):
        if self.saved_luke and self.agent_loc == (0, 0):
            self.game_score += 1000
            self.is_playing = False

    def take_action(self, action):
        self.game_score -= 1

        if self.game_score < -1000:
            self.is_playing = False

        match action:
            case Action.FORWARD:
                return self.handle_forward_action()
            case Action.LEFT:
                return self.handle_left_action()
            case Action.RIGHT:
                return self.handle_right_action()
            case Action.SHOOT:
                return self.handle_shoot_action()
            case Action.GRAB:
                return self.handle_grab_action()
            case Action.CLIMB:
                return self.handle_climb_action()
            case _:
                print(action)
                raise ValueError("R2-D2 can only move Forward, turn Left, turn Right, Shoot, Grab, or Climb.")

    def get_location(self):
        x, y = self.agent_loc
        return [x, y]

    def get_r2d2(self):
        return self.agent.loc, self.agent.direction


# RUN THE GAME
def run_game(scenario):
    w = WampaWorld(scenario)
    while w.is_playing:
        percepts = w.get_percepts()
        w.agent.record_percepts(percepts, w.agent.loc)
        w.agent.inference_algorithm()
        action = w.agent.choose_next_action()
        w.take_action(action)
        # print(action)
        # visualize_world(w, w.agent.loc, w.agent.direction)

    # print(w.agent.score)
    # print(w.agent.KB.safe_rooms)
    # print(w.agent.KB.visited_rooms | w.agent.KB.walls)
    # print(w.agent.KB)
    return w.game_score, w.saved_luke, w.agent_loc


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 wampa_world.py <scenario>")
        quit()

    scenario_name = sys.argv[1]

    try:
        scenario = eval(scenario_name)
    except:
        print(f"Scenario {scenario_name} not found.")
        quit()

    run_game(scenario)


if __name__ == "__main__":
    main()
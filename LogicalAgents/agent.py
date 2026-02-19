import copy
import heapq
import math
from operator import truediv
from random import shuffle
from itertools import combinations
import random
# from numpy.f2py.symbolic import as_numer_denom

from helper_types import Action, Direction, Percept, Room, PossibleWorld
from utils import flatten, get_direction, is_facing_wampa, orientation_to_delta
from typing import List, Dict, Set, Optional
from queue import PriorityQueue


class KB:

    def __init__(self, agent):
        # set of rooms that are known to exist
        self.all_rooms: Set[Room] = {agent.loc}
        # set of rooms that are known to be safe
        self.safe_rooms: Set[Room] = {agent.loc}
        # set of visited rooms (x, y)
        self.visited_rooms: Set[(Direction, Room)] = {(agent.direction,
                                                       agent.loc)}
        self.visited_count: Dict[Room, int] = dict()
        self.visited_count[agent.loc] = 1
        # set of rooms where stench has been perceived
        self.stench: Set[Room] = set()
        # set of rooms where breeze has been perceived
        self.breeze: Set[Room] = set()
        # {loc: direction} where bump has been perceived
        self.bump: Dict[Room, str] = dict()
        self.gasp: bool = False  # True if gasp has been perceived
        self.scream: bool = False  # True if scream has been perceived
        # set of rooms (x, y) that are known to be walls
        self.walls: Set[Room] = set()
        # set of rooms (x, y) that are known to be pits
        self.pits: Set[Room] = set()
        # room (x, y) that is known to be the Wampa
        self.wampa: Optional[Room] = None
        # room (x, y) that is known to be Luke
        self.luke: Optional[Room] = None

        # AGENT


class Agent:
    WORLD = None
    MOVE = {
        (0, 1): Direction.UP,
        (0, -1): Direction.DOWN,
        (-1, 0): Direction.LEFT,
        (1, 0): Direction.RIGHT
    }

    def __init__(self, world):
        self.world = world
        self.loc = (0, 0)
        self.direction = Direction.UP
        self.blaster = True
        self.has_luke = False
        self.KB = KB(self)
        Agent.WORLD = world

    @staticmethod
    def euclidean_distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.hypot(x2 - x1, y2 - y1)

    @staticmethod
    def adjacent_rooms(room):
        """Returns a set of tuples representing all possible adjacent rooms to
        'room' Use this function to update KB.all_rooms."""
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT,
                      Direction.RIGHT]
        adjacent_rooms = set()
        for d in directions:
            off_x, off_y = orientation_to_delta[d]
            # if (room[0] + off_x >= 0) and (
            #    room[1] + off_y >= 0) and (
            #    room[0] + off_x < Agent.WORLD.X) and (
            #    room[1] + off_y < Agent.WORLD.Y):
            adjacent_rooms.add((room[0] + off_x, room[1] + off_y))

        return adjacent_rooms

    def record_percepts(self, sensed_percepts, current_location):
        """Update the percepts in agent's KB with the percepts sensed in the
        current location, and update visited_rooms and all_rooms."""
        self.loc = current_location
        present_percepts = set(p for p in sensed_percepts if p)
        # set of rooms that are known to exist
        self.KB.all_rooms.add(current_location)
        # set of visited rooms (x, y)
        self.KB.visited_rooms.add((self.direction, current_location))
        self.KB.visited_count[current_location] = self.KB.visited_count.get(
            current_location, 0) + 1
        # set in safe rooms (x, y)
        self.KB.safe_rooms.add(current_location)
        safe_neighbors = True
        for percept in present_percepts:
            # set of rooms where stench has been perceived
            if percept == Percept.STENCH:
                self.KB.stench.add(current_location)
                safe_neighbors = False
            # set of rooms where breeze has been perceived
            if percept == Percept.BREEZE:
                self.KB.breeze.add(current_location)
                safe_neighbors = False
            # {loc: direction} where bump has been perceived
            if percept == Percept.BUMP:
                self.KB.bump[current_location] = self.direction
                self.infer_wall_locations()
                for wall in self.KB.walls:
                    if wall in self.KB.safe_rooms:
                        self.KB.safe_rooms.remove(wall)
            if percept == Percept.GASP:
                self.KB.gasp = True  # True if gasp has been perceived
            if percept == Percept.SCREAM:
                self.KB.scream = True  # True if scream has been perceived
        # add adjacent rooms - dont check if they are walls
        adj = Agent.adjacent_rooms(current_location)
        # adj = {r for r in adj if r not in self.KB.walls}
        self.KB.all_rooms.update(adj)
        # if no stench and no breeze then current and adjacent rooms safe
        if safe_neighbors:
            # adj_no_walls = {r for r in adj if r not in self.KB.walls}
            for neighbor in adj:
                if neighbor not in self.KB.walls:
                    self.KB.safe_rooms.add(neighbor)
        print("*" * 80)
        print("Current Position:", self.loc)
        print("ALL PERCEPTS:\n", sensed_percepts)
        print("ALL ROOMS:\n", self.KB.all_rooms)
        print("ALL WALLS:\n", self.KB.walls)
        print("ALL STENCH:\n", self.KB.stench)
        print("ALL BREEZE:\n", self.KB.breeze)
        print("ALL SAFE:\n", self.KB.safe_rooms)

    @staticmethod
    def enumerate_possible_worlds(
            all_rooms: Set[Room], safe_rooms: Set[Room], walls: Set[Room],
    ) -> Set[PossibleWorld]:
        """Return the set of all possible worlds, where a possible world is a
        tuple of (pit_rooms, wampa_room), pit_rooms is a tuple of tuples
        representing possible pit rooms, and wampa_room is a tuple
        representing a possible wampa room.

        Since the goal is to combinatorially enumerate all the possible worlds
        (pit and wampa locations) over the set of rooms that could potentially
        have a pit or a wampa, we first want to find that set.
        To do that, subtract the set of rooms that you know cannot
        have a pit or wampa from the set of all rooms.
        For example, a room with a wall cannot have a pit or wampa.

        Then use itertools.combinations to return the set of possible worlds,
        or all combinations of possible pit and wampa locations.

        You may find the utils.flatten(tup) method useful here for flattening
        wampa_room from a tuple of tuples into a tuple.

        The output of this function will be queried to find the model of the
        query, and will be checked for consistency with the KB
        to find the model of the KB."""

        # rooms that could contain a pit or a wampa
        potential = set(all_rooms)
        potential.difference_update(safe_rooms)
        potential.difference_update(walls)

        possible_worlds: Set[PossibleWorld] = set()

        # Wampa: choose 0 or 1 location
        for w in [None] + list(potential):

            # pits cannot overlap wampa
            pit_rooms = potential - ({w} if w is not None else set())

            m = len(pit_rooms)
            max_pits = min(m, len(all_rooms) - 2)

            # Pits: choose k locations for k in [0, m-2]
            for k in range(0, max_pits + 1):
                for pits in combinations(pit_rooms, k):
                    possible_worlds.add((frozenset(pits), w))
        if not possible_worlds:
            possible_worlds = {(frozenset(), None)}
        print("POSSIBLE WORLDS:\n", possible_worlds)
        return possible_worlds

    def pit_room_is_consistent_with_KB(self, pit_room: Optional[Room]) -> bool:
        """Return True if the room could be a pit given breeze in KB, False
        otherwise. A room could be a pit if all adjacent rooms that have been
        visited have had breeze perceived in them.
        A room cannot be a pit if any adjacent rooms that have been visited
        have not had breeze perceived in them.
        This will be used to find the model of the KB."""
        if pit_room is None:  # It is possible that there are no pits
            return not self.KB.breeze  # if no breeze has been perceived yet
        # TODO:
        breeze_in_visited_neighbor = False
        for adjacent_room in Agent.adjacent_rooms(pit_room):
            # skip walls
            if adjacent_room in self.KB.walls:
                continue
            # if room visited and has no breeze then not a pit
            visited_rooms = [r for d, r in self.KB.visited_rooms]
            if adjacent_room in visited_rooms:
                if adjacent_room not in self.KB.breeze:
                    return False
                else:
                    breeze_in_visited_neighbor = True
        return breeze_in_visited_neighbor

    def wampa_room_is_consistent_with_KB(self,
                                         wampa_room: Optional[Room]) -> bool:
        """Return True if the room could be a wampa given stench in KB, False
        otherwise. A room could be a wampa if all adjacent rooms that have
        been visited have had stench perceived in them.
        A room cannot be a wampa if any adjacent rooms that have been
        visited have not had stench perceived in them.
        This will be used to find the model of the KB."""
        if wampa_room is None:  # It is possible that there is no Wampa
            return not self.KB.stench  # if no stench has been perceived yet
        # TODO:
        stench_in_visited_neighbor = False
        for adjacent_room in Agent.adjacent_rooms(wampa_room):
            # skip walls
            if adjacent_room in self.KB.walls:
                continue
            # if room visited and has no stench then not a wampa
            visited_rooms = [r for d, r in self.KB.visited_rooms]
            if adjacent_room in visited_rooms:
                if adjacent_room not in self.KB.stench:
                    return False
                else:
                    stench_in_visited_neighbor = True
        return stench_in_visited_neighbor

    def find_model_of_KB(self, possible_worlds: Set[PossibleWorld]) -> Set[
        PossibleWorld]:
        """Return the subset of all possible worlds consistent with KB.
        possible_worlds is a set of tuples (pit_rooms, wampa_room),
        pit_rooms is a set of tuples of possible pit rooms,
        and wampa_room is a tuple representing a possible wampa room.
        A world is consistent with the KB if wampa_room is consistent
        and all pit rooms are consistent with the KB."""
        # TODO:
        consistent_worlds = set()
        for pit_rooms, wampa_room in possible_worlds:
            if not self.wampa_room_is_consistent_with_KB(wampa_room):
                continue

            ok = True
            if not pit_rooms:
                if not self.pit_room_is_consistent_with_KB(None):
                    ok = False

            for pit_room in pit_rooms:
                if not self.pit_room_is_consistent_with_KB(pit_room):
                    ok = False
                    break

            if ok:
                consistent_worlds.add((pit_rooms, wampa_room))

        print("-" * 80)
        print("Test KB Worlds:\n", consistent_worlds)
        return consistent_worlds

    @staticmethod
    def find_model_of_query(
            query: str, room: Room, possible_worlds: Set[PossibleWorld]
    ) -> Set[PossibleWorld]:
        """Where query can be "pit_in_room", "wampa_in_room", "no_pit_in_room"
        or "no_wampa_in_room",filter the set of worlds
        according to the query and room."""
        # TODO:
        filtered_worlds = set()
        q = query.lower()
        for pit_rooms, wampa_room in possible_worlds:
            if q == 'pit_in_room':
                if room in pit_rooms:
                    filtered_worlds.add((pit_rooms, wampa_room))
            elif q == 'no_pit_in_room':
                if room not in pit_rooms:
                    filtered_worlds.add((pit_rooms, wampa_room))
            elif q == 'wampa_in_room':
                if wampa_room == room:
                    filtered_worlds.add((pit_rooms, wampa_room))
            elif q == 'no_wampa_in_room':
                if wampa_room is None or room != wampa_room:
                    filtered_worlds.add((pit_rooms, wampa_room))

        return filtered_worlds

    def infer_wall_locations(self):
        """If a bump is perceived, infer wall locations along the entire known
        length of the room."""
        min_x = min(self.KB.all_rooms, key=lambda x: x[0])[0]
        max_x = max(self.KB.all_rooms, key=lambda x: x[0])[0]
        min_y = min(self.KB.all_rooms, key=lambda x: x[1])[1]
        max_y = max(self.KB.all_rooms, key=lambda x: x[1])[1]
        for room, orientation in self.KB.bump.items():
            if orientation == Direction.UP:
                for x in range(min_x, max_x + 1, 1):
                    self.KB.walls.add((x, room[1] + 1))
            elif orientation == Direction.DOWN:
                for x in range(min_x, max_x + 1, 1):
                    self.KB.walls.add((x, room[1] - 1))
            elif orientation == Direction.LEFT:
                for y in range(min_y, max_y + 1, 1):
                    self.KB.walls.add((room[0] - 1, y))
            elif orientation == Direction.RIGHT:
                for y in range(min_y, max_y + 1, 1):
                    self.KB.walls.add((room[0] + 1, y))

    def basic_forward_chaining(self):
        """First, make some simple inferences using forward chaining:
        1. If there is no breeze or stench in current location,
        infer that the adjacent rooms are safe.
        2. Infer wall locations given bump percept.
        3. Infer Luke's location given gasp percept.
        4. Infer whether the Wampa is alive given scream percept.
        Clear stench from the KB if Wampa is dead.
        """
        #  If there is no breeze or stench in current location,
        #  infer that the adjacent rooms are safe.
        sensed_percepts = self.world.get_percepts()
        print("Sensed percepts @ ", self.loc, self.direction, "ARE:",
              sensed_percepts)
        if Percept.STENCH not in sensed_percepts and \
                Percept.BREEZE not in sensed_percepts:
            for neighbor in Agent.adjacent_rooms(self.loc):
                self.KB.safe_rooms.add(neighbor)
        # Infer wall locations given bump percept.
        if Percept.BUMP in sensed_percepts:
            self.KB.bump[self.loc] = self.direction
            self.infer_wall_locations()
            for wall in self.KB.walls:
                if wall in self.KB.safe_rooms:
                    self.KB.safe_rooms.remove(wall)
        # Infer Luke's location given gasp percept.
        if Percept.GASP in sensed_percepts:
            self.KB.gasp = True  # True if gasp has been perceived
            self.KB.luke = self.loc
        # Infer whether the Wampa is alive given scream percept.
        if Percept.SCREAM in sensed_percepts:
            self.KB.scream = True  # True if scream has been perceived

    def backward_chaining_resolution(self):
        """
        Infer whether each adjacent room is safe, pit or wampa by
        following the backward-chaining resolution algorithm:
        1. Enumerate possible worlds.
        2. Find the model of the KB, i.e. the subset of possible worlds
        consistent with the KB.
        3. For each adjacent room and each query, find the model of the query.
        4. If the model of the KB is a subset of the model of the query, the
        query is entailed by the KB.
        5. Update KB.pits, KB.wampa, and KB.safe_rooms based on any newly
        derived knowledge.
        """

        worlds = self.enumerate_possible_worlds(self.KB.all_rooms,
                                                self.KB.safe_rooms,
                                                self.KB.walls)
        model_worlds = self.find_model_of_KB(worlds)
        adj_rooms = Agent.adjacent_rooms(self.loc)

        for room in adj_rooms:
            change_made = False
            for qry in ['pit_in_room', 'no_pit_in_room',
                        'wampa_in_room']:
                model_query = Agent.find_model_of_query(qry, room, worlds)
                if model_worlds.issubset(model_query):
                    if qry == 'pit_in_room':
                        if room in self.KB.pits:
                            continue
                        self.KB.pits.add(room)
                        change_made = True
                    elif qry == 'wampa_in_room':
                        if self.KB.wampa == room:
                            continue
                        self.KB.wampa = room
                        change_made = True
                    elif qry == 'no_pit_in_room':
                        model_qry_w = Agent.find_model_of_query(
                            'no_wampa_in_room', room, worlds)
                        if model_worlds.issubset(
                                model_query.intersection(model_qry_w)):
                            if room in self.KB.safe_rooms or \
                                    room in self.KB.walls:
                                continue
                            self.KB.safe_rooms.add(room)
                            change_made = True
            # if change_made:
            # break

    def inference_algorithm(self):
        """First, make some basic inferences
        Then, infer whether each adjacent room is safe, pit or wampa by
        following the backward-chaining resolution algorithm
        """
        self.basic_forward_chaining()
        self.backward_chaining_resolution()

    def all_safe_next_actions(self) -> List[Action]:
        """Define R2D2's valid and safe next actions based on his current
        location and knowledge of the environment."""
        safe_actions = []
        left_right_actions = [Action.LEFT, Action.RIGHT]
        random.shuffle(left_right_actions)
        x, y = self.loc
        dx, dy = orientation_to_delta[self.direction]
        forward_room = (x + dx, y + dy)
        # TODO:
        # perform an 180 degree turn and move forward
        if self.has_luke:
            if self.loc == (0, 0):
                safe_actions.append(Action.CLIMB)  # exit
        if self.KB.luke is not None and self.loc == self.KB.luke:
            if not self.has_luke:
                safe_actions.append(Action.GRAB)
        if self.KB.wampa is not None and forward_room == self.KB.wampa and \
                self.blaster:
            safe_actions.append(Action.SHOOT)
        sensed_percepts = self.world.get_percepts()
        if Percept.STENCH not in sensed_percepts and \
                Percept.BREEZE not in sensed_percepts and \
                Percept.BUMP not in sensed_percepts:
            safe_actions.append(Action.FORWARD)
        elif forward_room in self.KB.safe_rooms:
            safe_actions.append(Action.FORWARD)
        safe_actions.append(left_right_actions[0])
        safe_actions.append(left_right_actions[1])
        return safe_actions

    def choose_next_action(self) -> Action:
        """Choose next action from all safe next actions. You may want to
        prioritize some actions based on current state. For example, if R2D2
        knows Luke's location and is in the same room as Luke, you may want
        to prioritize 'grab' over all other actions. Similarly, if R2D2 has
        Luke, you may want to prioritize moving toward the exit. You can
        implement this as basically (randomly choosing between safe actions)
        or as sophisticated (optimizing exploration of unvisited states,
        finding shortest paths, etc.) as you like."""
        actions = self.all_safe_next_actions()
        print("actions:", actions)
        print("position", self.loc, self.direction)

        # if first action to grab, climb or shoot then execute immediately
        if actions[0] == Action.GRAB or actions[0] == Action.CLIMB or\
                actions[0] == Action.SHOOT:
            return actions[0]

        # put safe neighbors in priority queue based on number of prior visits
        # if luke not at hand.  if luke at hand head for neighbor with closest
        # euclidean distance to (0,0)
        pq = PriorityQueue()
        for neighbor in Agent.adjacent_rooms(self.loc):
            # skip out of bounce neighbors that are never visited
            if (neighbor[0] < 0) or (neighbor[1] < 0) or\
                (neighbor[0] >= Agent.WORLD.X) or\
                (neighbor[1] >= Agent.WORLD.Y):
                continue
            if neighbor in self.KB.safe_rooms:
                if not self.has_luke:
                    pq.put((self.KB.visited_count.get(neighbor, 0), neighbor))
                else:
                    pq.put((Agent.euclidean_distance(neighbor, (0, 0)),
                            neighbor))

        # if no luke, pick neighbor with lowest visits and direct R2D2 there
        x, y = self.loc
        if not pq.empty():
            visits, (n_x, n_y) = pq.get()
            direct = Agent.MOVE[n_x - x, n_y - y]
            if direct == self.direction:
                return Action.FORWARD
            elif self.direction == Direction.DOWN:
                if direct == Direction.LEFT:
                    return Action.RIGHT
                elif direct == Direction.RIGHT or direct == Direction.UP:
                    return Action.LEFT
            elif self.direction == Direction.UP:
                if direct == Direction.LEFT or direct == Direction.DOWN:
                    return Action.LEFT
                elif direct == Direction.RIGHT:
                    return Action.RIGHT
            elif self.direction == Direction.LEFT:
                if direct == Direction.UP:
                    return Action.RIGHT
                elif direct == Direction.DOWN:
                    return Action.LEFT
                elif direct == Direction.RIGHT:
                    return Action.RIGHT
            elif self.direction == Direction.RIGHT:
                if direct == Direction.UP:
                    return Action.LEFT
                elif direct == Direction.DOWN:
                    return Action.RIGHT
                elif direct == Direction.LEFT:
                    return Action.LEFT

        return actions[0]


# Approximately how many hours did you spend on this assignment?
feedback_question_1 = """
50 hours
"""

# Which aspects of this assignment did you find most challenging?
# Were there any significant stumbling blocks?
feedback_question_2 = """
the forward and backward inference
getting the logic to work
"""

# Which aspects of this assignment did you like?
# Is there anything you would have changed?
feedback_question_3 = """
found it very confusing without adequate explanation
"""

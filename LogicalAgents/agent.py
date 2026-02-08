import copy
import heapq
from random import shuffle
from itertools import combinations

from numpy.f2py.symbolic import as_numer_denom

from helper_types import Action, Direction, Percept, Room, PossibleWorld
from utils import flatten, get_direction, is_facing_wampa, orientation_to_delta
from typing import List, Dict, Set, Optional


# KNOWLEDGE BASE
class KB:
    def __init__(self, agent):
        # set of rooms that are known to exist
        self.all_rooms: Set[Room] = {agent.loc}
        # set of rooms that are known to be safe
        self.safe_rooms: Set[Room] = {agent.loc}
        # set of visited rooms (x, y)
        self.visited_rooms: Set[Room] = {agent.loc}
        #
        # set of rooms where stench has been perceived
        self.stench: Set[Room] = set()
        # set of rooms where breeze has been perceived
        self.breeze: Set[Room] = set()
        # {loc: direction} where bump has been perceived
        self.bump: Dict[Room, str] = dict()
        self.gasp: bool = False  # True if gasp has been perceived
        self.scream: bool = False  # True if scream has been perceived
        #
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

        def __init__(self, world):
            self.world = world
            self.loc = (0, 0)
            self.direction = Direction.UP
            self.blaster = True
            self.has_luke = False
            self.KB = KB(self)
            Agent.WORLD = world

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
            self.KB.visited_rooms.add(current_location)
            for percept in present_percepts:
                # set of rooms where stench has been perceived
                if percept == Percept.STENCH:
                    self.KB.stench.add(current_location)
                # set of rooms where breeze has been perceived
                if percept == Percept.BREEZE:
                    self.KB.breeze.add(current_location)
                # {loc: direction} where bump has been perceived
                if percept == Percept.BUMP:
                    self.KB.bump[current_location] = self.direction
                    self.infer_wall_locations()
                if percept == Percept.GASP:
                    self.KB.gasp = True  # True if gasp has been perceived
                if percept == Percept.SCREAM:
                    self.KB.scream = True  # True if gasp has been perceived
            # add adjacent rooms - dont check if they are walls
            adj = Agent.adjacent_rooms(current_location)
            # adj = {r for r in adj if r not in self.KB.walls}
            self.KB.all_rooms.update(adj)
            print("ALL PERCEPTS:\n", sensed_percepts)
            print("ALL ROOMS:\n", self.KB.all_rooms)
            print("ALL WALLS:\n", self.KB.walls)
            print("ALL STENCH:\n", self.KB.stench)
            print("ALL STENCH:\n", self.KB.breeze)

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
                max_pits = max(0, m - 2)  # allow 0 pits even if small

                # Pits: choose k locations for k in [0, m-2]
                for k in range(0, max_pits + 1):
                    for pits in combinations(pit_rooms, k):
                        possible_worlds.add((frozenset(pits), w))
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
                if adjacent_room in self.KB.visited_rooms:
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
                if adjacent_room in self.KB.visited_rooms:
                    if adjacent_room not in self.KB.breeze:
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
                for pit_room in pit_rooms:
                    if not self.pit_room_is_consistent_with_KB(pit_room):
                        ok = False
                        break

                if ok:
                    consistent_worlds.add((pit_rooms, wampa_room))

            return consistent_worlds

        @staticmethod
        def find_model_of_query(
                query: str, room: Room, possible_worlds: Set[PossibleWorld]
        ) -> Set[PossibleWorld]:
            """Where query can be "pit_in_room", "wampa_in_room", "no_pit_in_room"
            or "no_wampa_in_room",filter the set of worlds
            according to the query and room."""
            # TODO:
            ...
            pass
            return set()

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
            1. If there is no breeze or stench in current location, infer that the
            adjacent rooms are safe.
            2. Infer wall locations given bump percept.
            3. Infer Luke's location given gasp percept.
            4. Infer whether the Wampa is alive given scream percept. Clear stench
            from the KB if Wampa is dead.
            """
            # TODO:
            pass

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
            # TODO:
            pass

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
            safe_actions = [Action.GRAB]
            x, y = self.loc
            dx, dy = orientation_to_delta[self.direction]
            forward_room = (x + dx, y + dy)
            # TODO:
            ...
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
            # TODO:
            ...
            return actions[0]


# Approximately how many hours did you spend on this assignment?
feedback_question_1 = """..."""

# Which aspects of this assignment did you find most challenging?
# Were there any significant stumbling blocks?
feedback_question_2 = """..."""

# Which aspects of this assignment did you like?
# Is there anything you would have changed?
feedback_question_3 = """..."""

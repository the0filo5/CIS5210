import argparse
import tkinter as tk
import tkinter.font as tk_font
from functools import lru_cache
from typing import *
from scenarios import SCENARIOS
from wampa_world import WampaWorld
from helper_types import KeyboardAction, Action, Direction

WAMPA_IMAGE = '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'
LUKE_IMAGE = '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'


@lru_cache(maxsize=None)
def get_start_point(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                return i, j


class WampaGame:
    def __init__(self,  grid: Tuple[Tuple[Any, ...], ...], scenario):
        self.__grid = grid
        self.__n = len(grid)
        self.__m = len(grid[0])
        self.scenario = scenario
        self.wampa = WampaWorld(scenario)
        self.position = get_start_point(grid)
        self.facing = Direction.UP

    def wampa_xy_to_ij(self, x, y):
        j = x + 1
        i = self.__n - 2 - y
        return i, j

    def ij_to_wampa_xy(self, i, j):
        x = j - 1
        y = self.__n - 2 - i
        return x, y

    def get_action_from_key(self, key: KeyboardAction):
        match key:
            case  KeyboardAction.Up:
                return Action.FORWARD
            case KeyboardAction.Left:
                return Action.LEFT
            case KeyboardAction.Right:
                return Action.RIGHT
            case KeyboardAction.g:
                return Action.GRAB
            case KeyboardAction.c:
                return Action.CLIMB
            case KeyboardAction.s:
                return Action.SHOOT
            case KeyboardAction.Return:
                action = self.wampa.agent.choose_next_action()
                print(action)
                return action
        return None

    def __act(self, key: KeyboardAction):
        action = self.get_action_from_key(key)
        self.wampa.take_action(action)

        percepts = self.wampa.get_percepts()
        self.wampa.agent.record_percepts(percepts, self.wampa.agent.loc)
        self.wampa.agent.inference_algorithm()

        (x, y), facing = self.wampa.get_r2d2()
        (i, j) = self.wampa_xy_to_ij(x, y)
        self.position = (i, j)
        self.facing = facing

    def iterate(self, action: KeyboardAction) -> bool:
        if isinstance(self.__grid[self.position[0]][self.position[1]], float):
            self.position = get_start_point(self.__grid)
            return True
        self.__act(action)
        return False


class GUI(tk.Tk):
    SQUARE_SIZE = 60
    ANIMATION_SPEED = 0.1

    def __init__(self, env: WampaGame, grid, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__grid = grid
        self.__rows = len(grid)
        self.__cols = len(grid[0])
        self.__env = env
        self.__episode_counter = 1
        self.__iter_backup = []
        self.__cache_env()
        self.__wampa_image = tk.PhotoImage(data=WAMPA_IMAGE)
        self.__luke_image = tk.PhotoImage(data=LUKE_IMAGE)

        width, height = GUI.SQUARE_SIZE * self.__cols, GUI.SQUARE_SIZE * self.__rows

        tk.Label(self, text="Wampa World").pack(side=tk.TOP)
        epi_frame = tk.Frame(self)

        self.__episode = tk.Label(epi_frame)
        self.__episode.grid(row=0, column=0)

        epi_frame.pack(side=tk.TOP)

        frame = tk.LabelFrame(self, text='Display type')

        self.__display_type = tk.IntVar(frame, value=1)
        self.__display_type.trace_add('write', self.__display_mode_changed)

        tk.Radiobutton(frame, text='Partial', variable=self.__display_type,
                       value=1).grid(row=1, column=0)
        tk.Radiobutton(frame, text='Full', variable=self.__display_type,
                       value=0).grid(row=1, column=1)


        frame.pack(side=tk.BOTTOM)
        self.__canvas = tk.Canvas(
            self, width=width + 1, height=height + 1, highlightthickness=0)

        for i in range(self.__rows + 1):
            self.__canvas.create_line(
                0, i * GUI.SQUARE_SIZE, width, i * GUI.SQUARE_SIZE)
        for i in range(self.__cols + 1):
            self.__canvas.create_line(
                i * GUI.SQUARE_SIZE, 0, i * GUI.SQUARE_SIZE, height)

        frame = tk.Frame(self)
        self.__iteration = tk.IntVar(frame, value=len(self.__iter_backup) - 1)

        self.title('Wampa Game - CIS 5210')
        self.__draw_grid()
        self.__redraw_aux()
        self.__canvas.focus_set()
        self.__canvas.bind('<Key>', self.__pressed_key)
        self.__canvas.bind('<Button-1>', lambda _: self.__canvas.focus_set())

    def __pressed_key(self, event):
        if not self.__env.wampa.is_playing:
            print('game over')
            return
        action = getattr(KeyboardAction, event.keysym, None)
        if action is None:
            return
        cur_view = int(self.__iteration.get())
        cur_iter = len(self.__iter_backup) - 1
        self.__iteration.set(cur_iter)
        if cur_view < cur_iter:
            return
        if self.__env.iterate(action):
            self.__episode_counter += 1
        self.__cache_env()
        self.__iteration.set(cur_iter + 1)
        self.__redraw_aux()
        self.__display_mode_changed()

    def __draw_wampa(self):
        self.__canvas.delete('wampa')
        wampa_loc = self.__env.scenario['wampa']
        if self.__display_type.get() and self.__env.wampa.is_playing:
            wampa_loc = self.__env.wampa.agent.KB.wampa
        if not wampa_loc:
            return
        x, y = wampa_loc

        i, j = self.__env.wampa_xy_to_ij(x, y)
        if not self.__env.wampa.wampa_alive:
            return

        self.__canvas.create_image(
            (j * GUI.SQUARE_SIZE + 5, i * GUI.SQUARE_SIZE + 5),
            image=self.__wampa_image, anchor=tk.NW, tags="wampa")

    def __draw_luke(self):
        self.__canvas.delete('luke')
        has_luke = self.__env.wampa.saved_luke
        luke_loc = self.__env.scenario['luke']
        if self.__display_type.get():
            luke_loc = self.__env.wampa.agent.KB.luke
        if has_luke:
            pass
        if not luke_loc:
            return
        x, y = luke_loc

        i, j = self.__env.wampa_xy_to_ij(x, y)
        if self.__env.wampa.saved_luke:
            i, j = self.__env.position

        self.__canvas.create_image(
            (j * GUI.SQUARE_SIZE + 5, i * GUI.SQUARE_SIZE + 5),
            image=self.__luke_image, anchor=tk.NW, tags="luke")

    def __draw_win(self):
        i, j = self.__env.wampa_xy_to_ij(0, 0)
        if not self.__env.wampa.saved_luke or not self.__env.wampa.agent_loc == (0, 0):
            return
        if not self.__env.wampa.is_playing and self.__env.wampa.game_score > 0:
            font = tk_font.Font(size=self.SQUARE_SIZE, weight='bold')
            self.__draw_rectangle(i, j, fill='green')
            self.__canvas.create_text(
                (self.__cols // 2) * GUI.SQUARE_SIZE, (self.__rows // 2) * GUI.SQUARE_SIZE,
                text="YOU WIN", font=font, fill='green')

    def __draw_lost(self):
        if self.__env.wampa.is_playing:
            return
        if self.__env.wampa.saved_luke and self.__env.wampa.agent_loc == (0, 0) and self.__env.wampa.game_score > 0:
            return

        font = tk_font.Font(size=self.SQUARE_SIZE, weight='bold')
        self.__canvas.create_text(
            (self.__cols // 2) * GUI.SQUARE_SIZE, (self.__rows // 2) * GUI.SQUARE_SIZE,
            text="YOU LOSE", font=font, fill='red')

    def __draw_pit(self, i, j, **kwargs):
        self.__canvas.create_oval(
            j * GUI.SQUARE_SIZE, i * GUI.SQUARE_SIZE,
            (j + 1) * GUI.SQUARE_SIZE, (i + 1) * GUI.SQUARE_SIZE, kwargs)

    def __draw_rectangle(self, i, j, **kwargs):
        self.__canvas.create_rectangle(
            j * GUI.SQUARE_SIZE, i * GUI.SQUARE_SIZE,
            (j + 1) * GUI.SQUARE_SIZE, (i + 1) * GUI.SQUARE_SIZE, kwargs)

    def __draw_pits(self):
        if self.__display_type.get() and self.__env.wampa.is_playing:
            pits_xy = self.__env.wampa.agent.KB.pits
        else:
            pits_xy = self.__env.scenario['pits']
        pits_ij = {
            self.__env.wampa_xy_to_ij(x, y)
            for (x, y) in pits_xy
        }
        for (i, j) in pits_ij:
            self.__draw_pit(i, j, fill='black', tags='display')

    def __draw_grid(self):
        font = tk_font.Font(size=self.SQUARE_SIZE // 6, weight='bold')

        for i in range(self.__rows):
            for j in range(self.__cols):
                cell = self.__grid[i][j]
                if cell == '#':
                    self.__draw_rectangle(i, j, fill='black')
                elif isinstance(cell, float):
                    if cell > 0:
                        self.__draw_rectangle(i, j, fill='green')
                    elif cell < 0:
                        self.__draw_rectangle(i, j, fill='red')
                    self.__canvas.create_text(
                        (j + .5) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        text=format(cell, '.2f'), font=font)
        self.__canvas.pack()

    def __draw_percepts(self):
        font = tk_font.Font(size=self.SQUARE_SIZE // 10)

        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__has_stench(i, j):
                    self.__canvas.create_text(
                        (j + .5) * GUI.SQUARE_SIZE, (i + .15) * GUI.SQUARE_SIZE,
                        text="STENCH", font=font, tags='display')
                if self.__has_breeze(i, j):
                    self.__canvas.create_text(
                        (j + .5) * GUI.SQUARE_SIZE, (i + .85) * GUI.SQUARE_SIZE,
                        text="BREEZE", font=font, tags='display')

    def __is_known(self, i, j):
        return (i, j) in {
            self.__env.wampa_xy_to_ij(x, y)
            for (x, y) in self.__env.wampa.agent.KB.all_rooms
        }

    def __is_safe(self, i, j):
        return (i, j) in {
            self.__env.wampa_xy_to_ij(x, y)
            for (x, y) in self.__env.wampa.agent.KB.safe_rooms
        }

    def __is_wall(self, i, j):
        if self.__display_type.get():
            return (i, j) in {
                self.__env.wampa_xy_to_ij(x, y)
                for (x, y) in self.__env.wampa.agent.KB.walls
            }
        return i == 0 or i == self.__rows - 1 or j == 0 or j == self.__cols - 1

    def __has_stench(self, i, j):
        return (i, j) in {
            self.__env.wampa_xy_to_ij(x, y)
            for (x, y) in self.__env.wampa.agent.KB.stench
        }

    def __has_breeze(self, i, j):
        return (i, j) in {
            self.__env.wampa_xy_to_ij(x, y)
            for (x, y) in self.__env.wampa.agent.KB.breeze
        }

    def __draw_walls(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__display_type.get() and not self.__is_known(i, j):
                    continue
                if not self.__is_wall(i, j):
                    continue

                self.__canvas.create_line(
                    j * GUI.SQUARE_SIZE, i * GUI.SQUARE_SIZE,
                    (j + 1) * GUI.SQUARE_SIZE, (i + 1) * GUI.SQUARE_SIZE,
                    tags='display')
                self.__canvas.create_line(
                    (j + 1) * GUI.SQUARE_SIZE, i * GUI.SQUARE_SIZE,
                    j * GUI.SQUARE_SIZE, (i + 1) * GUI.SQUARE_SIZE,
                    tags='display')

    def __draw_r2d2(self):
        options = {
            'width': GUI.SQUARE_SIZE // 10,
            'arrow': tk.FIRST,
            'arrowshape': (GUI.SQUARE_SIZE // 5, GUI.SQUARE_SIZE // 5, GUI.SQUARE_SIZE // 10),
            'tags': 'display'
        }
        i, j = self.__env.position
        match self.__env.facing:
            case Direction.UP:
                return self.__canvas.create_line(
                    (j + .5) * GUI.SQUARE_SIZE, (i + .2) * GUI.SQUARE_SIZE,
                    (j + .5) * GUI.SQUARE_SIZE, (i + .8) * GUI.SQUARE_SIZE,
                    **options)
            case Direction.DOWN:
                return self.__canvas.create_line(
                    (j + .5) * GUI.SQUARE_SIZE, (i + .8) * GUI.SQUARE_SIZE,
                    (j + .5) * GUI.SQUARE_SIZE, (i + .2) * GUI.SQUARE_SIZE,
                    **options)
            case Direction.RIGHT:
                return self.__canvas.create_line(
                    (j + .8) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                    (j + .2) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                    **options)
            case Direction.LEFT:
                return self.__canvas.create_line(
                    (j + .2) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                    (j + .8) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                    **options)

    def __draw_policy(self):
        options = {
            'width': GUI.SQUARE_SIZE // 10,
            'arrow': tk.FIRST,
            'arrowshape': (GUI.SQUARE_SIZE // 5, GUI.SQUARE_SIZE // 5, GUI.SQUARE_SIZE // 10),
            'tags': 'display'
        }
        backup = self.__iter_backup[self.__iteration.get()][0]
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__grid[i][j] not in (' ', 'S'):
                    continue
                policy = backup[i, j][2]
                if policy == KeyboardAction.Up:
                    self.__canvas.create_line(
                        (j + .5) * GUI.SQUARE_SIZE, (i + .2) * GUI.SQUARE_SIZE,
                        (j + .5) * GUI.SQUARE_SIZE, (i + .8) * GUI.SQUARE_SIZE,
                        **options)
                elif policy == KeyboardAction.Down:
                    self.__canvas.create_line(
                        (j + .5) * GUI.SQUARE_SIZE, (i + .8) * GUI.SQUARE_SIZE,
                        (j + .5) * GUI.SQUARE_SIZE, (i + .2) * GUI.SQUARE_SIZE,
                        **options)
                elif policy == KeyboardAction.Right:
                    self.__canvas.create_line(
                        (j + .8) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        (j + .2) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        **options)
                elif policy == KeyboardAction.Left:
                    self.__canvas.create_line(
                        (j + .2) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        (j + .8) * GUI.SQUARE_SIZE, (i + .5) * GUI.SQUARE_SIZE,
                        **options)

    def __draw_visible(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                if not self.__display_type.get():
                    continue
                elif not self.__is_known(i, j):
                    self.__draw_rectangle(i, j, fill='black', tags='display')
                elif not self.__is_safe(i, j):
                    self.__draw_rectangle(i, j, fill='red', tags='display')

    def __redraw_aux(self):
        (i, j), score = self.__iter_backup[self.__iteration.get()][1:]
        score = self.__env.wampa.game_score
        has_luke = self.__env.wampa.saved_luke
        has_blaster = self.__env.wampa.has_blaster

        self.__episode.configure(text='Score: %d \n Has Blaster: %s \n Has Luke: %s' % (score,  has_blaster,  has_luke))
        self.__canvas.delete('agent')
        self.__draw_r2d2()
        blaster_color = 'cyan' if has_blaster else 'black'
        self.__canvas.create_oval((j + .4) * GUI.SQUARE_SIZE, (i + .4) * GUI.SQUARE_SIZE,
                                  (j + .6) * GUI.SQUARE_SIZE, (i + .6) * GUI.SQUARE_SIZE,
                                  tags='agent', fill=blaster_color)
        self.__draw_visible()
        self.__draw_walls()
        self.__draw_luke()
        self.__draw_r2d2()
        self.__draw_pits()
        self.__draw_wampa()
        self.__draw_win()
        self.__draw_lost()

    def __display_mode_changed(self, *_):
        self.__canvas.delete('display')
        self.__draw_r2d2()
        self.__draw_walls()
        self.__redraw_aux()
        self.__draw_percepts()

    def __cache_env(self):
        cache = dict()
        self.__iter_backup.append((
            cache,
            self.__env.position,
            self.__episode_counter))


def main():
    def argtype(arg):
        try:
            f = int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError('must be a number between 1 and 6')
        if 0 <= f < 7:
            return f
        raise argparse.ArgumentTypeError('must be a number between 1 and 6')

    def scenario_to_grid(scenario):
        x, y = scenario['grid']
        grid = list(
            list(' ' for _ in range(-1, x+1))
            for _ in range(-1, y+1)
        )
        grid[-2][1] = 'S'
        return tuple(tuple(row) for row in grid)

    parser = argparse.ArgumentParser(
        description='Wampa World GUI for CIS 5210, Artificial Intelligence',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-s', '--scenario', help='scenario number',
                        type=argtype, default=0)

    args = parser.parse_args()
    scenario = SCENARIOS[1] #args.scenario]
    grid = scenario_to_grid(scenario)
    env = WampaGame(grid, scenario)
    GUI(env, grid).mainloop()


if __name__ == '__main__':
    main()

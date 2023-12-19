from enum import Enum

import pygame

from constants import *


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Agent:
    def __init__(self) -> None:
        self.score = 0
        self.gold = 0
        self.cell = None
        self.map_size = None
        self.direction = Direction.RIGHT

    def move_forward(self, grid_cells: list):
        if self.direction == Direction.UP:
            self.move_up(grid_cells)
        elif self.direction == Direction.DOWN:
            self.move_down(grid_cells)
        elif self.direction == Direction.LEFT:
            self.move_left(grid_cells)
        elif self.direction == Direction.RIGHT:
            self.move_right(grid_cells)

    def move_up(self, grid_cells: list):
        prev_cell = self.cell
        prev_cell.type = prev_cell.type.replace("A", "")

        self.cell = self.cell.check_cell(self.cell.x, self.cell.y - 1, grid_cells)
        self.cell.type = "A" + self.cell.type

        self.cell.img_list["agent"] = prev_cell.img_list["agent"]
        prev_cell.img_list["agent"] = None

        self.score -= 10

    def move_down(self, grid_cells: list):
        prev_cell = self.cell
        prev_cell.type = prev_cell.type.replace("A", "")

        self.cell = self.cell.check_cell(self.cell.x, self.cell.y + 1, grid_cells)
        self.cell.type = "A" + self.cell.type

        self.cell.img_list["agent"] = prev_cell.img_list["agent"]
        prev_cell.img_list["agent"] = None

        self.score -= 10

    def move_left(self, grid_cells: list):
        prev_cell = self.cell
        prev_cell.type = prev_cell.type.replace("A", "")

        self.cell = self.cell.check_cell(self.cell.x - 1, self.cell.y, grid_cells)
        self.cell.type = "A" + self.cell.type

        self.cell.img_list["agent"] = prev_cell.img_list["agent"]
        prev_cell.img_list["agent"] = None

        self.score -= 10

    def move_right(self, grid_cells: list):
        prev_cell = self.cell
        prev_cell.type = prev_cell.type.replace("A", "")

        self.cell = self.cell.check_cell(self.cell.x + 1, self.cell.y, grid_cells)
        self.cell.type = "A" + self.cell.type

        self.cell.img_list["agent"] = prev_cell.img_list["agent"]
        prev_cell.img_list["agent"] = None

        self.score -= 10

    def turn_up(self):
        self.cell.img_list["agent"] = pygame.image.load(AGENT_UP_IMG).convert_alpha()
        self.direction = Direction.UP

    def turn_down(self):
        self.cell.img_list["agent"] = pygame.image.load(AGENT_DOWN_IMG).convert_alpha()
        self.direction = Direction.DOWN

    def turn_left(self):
        self.cell.img_list["agent"] = pygame.image.load(AGENT_LEFT_IMG).convert_alpha()
        self.direction = Direction.LEFT

    def turn_right(self):
        self.cell.img_list["agent"] = pygame.image.load(AGENT_RIGHT_IMG).convert_alpha()
        self.direction = Direction.RIGHT

    def shoot_arrow(self, grid_cells: list):
        if self.direction == Direction.UP:
            arrow_cell = self.cell.check_cell(self.cell.x, self.cell.y - 1, grid_cells)
            arrow_cell.img_list["arrow"] = pygame.image.load(
                ARROW_UP_IMG
            ).convert_alpha()
        elif self.direction == Direction.DOWN:
            arrow_cell = self.cell.check_cell(self.cell.x, self.cell.y + 1, grid_cells)
            arrow_cell.img_list["arrow"] = pygame.image.load(
                ARROW_DOWN_IMG
            ).convert_alpha()
        elif self.direction == Direction.LEFT:
            arrow_cell = self.cell.check_cell(self.cell.x - 1, self.cell.y, grid_cells)
            arrow_cell.img_list["arrow"] = pygame.image.load(
                ARROW_LEFT_IMG
            ).convert_alpha()
        elif self.direction == Direction.RIGHT:
            arrow_cell = self.cell.check_cell(self.cell.x + 1, self.cell.y, grid_cells)
            arrow_cell.img_list["arrow"] = pygame.image.load(
                ARROW_RIGHT_IMG
            ).convert_alpha()

        self.score -= 100

        return arrow_cell

    def check_collide_pit_or_wumpus(self):
        if "W" in self.cell.type or "P" in self.cell.type:
            self.score -= 10000
            return True

    def collect_gold(self):
        self.cell.type = self.cell.type.replace("G", "")
        self.cell.img_list["gold"] = None
        self.gold += 1
        self.score += 1000

    def climb_out(self):
        self.score += 10

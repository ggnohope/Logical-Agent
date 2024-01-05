import pygame
from const import *
from solver import *

class Agent:
    def __init__(self) -> None:
        self.score = 0
        self.gold = 0
        self.current_cell = None
        self.direction = TURN_RIGHT

    def move_forward(self, map):
        if self.direction == TURN_UP:
            self.move_up(map)
        elif self.direction == TURN_DOWN:
            self.move_down(map)
        elif self.direction == TURN_LEFT:
            self.move_left(map)
        elif self.direction == TURN_RIGHT:
            self.move_right(map)

    def move_up(self, map):
        i = self.current_cell.get_converted_pos()
        map.map[i - 10].attribute_imgs["agent"] = map.map[i].attribute_imgs["agent"]
        map.map[i].attribute_imgs["agent"] = None
        self.current_cell = map.map[i - 10]
        self.current_cell.visited = True
        self.score -= 10

    def move_down(self, map):
        i = self.current_cell.get_converted_pos()
        map.map[i + 10].attribute_imgs["agent"] = map.map[i].attribute_imgs["agent"]
        map.map[i].attribute_imgs["agent"] = None
        self.current_cell = map.map[i + 10]
        self.current_cell.visited = True
        self.score -= 10

    def move_right(self, map):
        i = self.current_cell.get_converted_pos()
        map.map[i + 1].attribute_imgs["agent"] = map.map[i].attribute_imgs["agent"]
        map.map[i].attribute_imgs["agent"] = None
        self.current_cell = map.map[i + 1]
        self.current_cell.visited = True
        self.score -= 10

    def move_left(self, map):
        i = self.current_cell.get_converted_pos()
        map.map[i - 1].attribute_imgs["agent"] = map.map[i].attribute_imgs["agent"]
        map.map[i].attribute_imgs["agent"] = None
        self.current_cell = map.map[i - 1]
        self.current_cell.visited = True
        self.score -= 10

    def turn_up(self):
        self.current_cell.attribute_imgs["agent"] = pygame.image.load(AGENT_UP_IMG).convert_alpha()
        self.direction = TURN_UP

    def turn_down(self):
        self.current_cell.attribute_imgs["agent"] = pygame.image.load(AGENT_DOWN_IMG).convert_alpha()
        self.direction = TURN_DOWN

    def turn_left(self):
        self.current_cell.attribute_imgs["agent"] = pygame.image.load(AGENT_LEFT_IMG).convert_alpha()
        self.direction = TURN_LEFT

    def turn_right(self):
        self.current_cell.attribute_imgs["agent"] = pygame.image.load(AGENT_RIGHT_IMG).convert_alpha()
        self.direction = TURN_RIGHT

    def shoot_arrow(self, grid_cells: list):
        if self.direction == TURN_DOWN:
            arrow_cell = self.current_cell.valid_cell(self.current_cell.x, self.current_cell.y - 1, grid_cells)
            arrow_cell.attribute_imgs["arrow"] = pygame.image.load(
                ARROW_DOWN_IMG
            ).convert_alpha()
        elif self.direction == TURN_UP:
            arrow_cell = self.current_cell.valid_cell(self.current_cell.x, self.current_cell.y + 1, grid_cells)
            arrow_cell.attribute_imgs["arrow"] = pygame.image.load(
                ARROW_UP_IMG
            ).convert_alpha()
        elif self.direction == TURN_LEFT:
            arrow_cell = self.current_cell.valid_cell(self.current_cell.x - 1, self.current_cell.y, grid_cells)
            arrow_cell.attribute_imgs["arrow"] = pygame.image.load(
                ARROW_LEFT_IMG
            ).convert_alpha()
        elif self.direction == TURN_RIGHT:
            arrow_cell = self.current_cell.valid_cell(self.current_cell.x + 1, self.current_cell.y, grid_cells)
            arrow_cell.attribute_imgs["arrow"] = pygame.image.load(
                ARROW_RIGHT_IMG
            ).convert_alpha()

        self.score -= 100

        return arrow_cell

    def collect_gold(self):
        self.current_cell.content = self.current_cell.content.replace("G", "")
        self.current_cell.attribute_imgs["gold"] = None
        self.gold += 1
        self.score += 1000

    def climb_out_cave(self):
        self.score += 10
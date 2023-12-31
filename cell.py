import math
import pygame
from const import *

class Cell_UI:
    def __init__(self, x, y, content: str) -> None:
        self.x, self.y = x, y
        self.map_size = 10
        self.visited = False
        self.content = content
        self.attribute_imgs = { #use for render ui
            "arrow": None,
            "gold": None,
            "wumpus": None,
            "pit": None,
            "agent": None,
            "breeze": None,
            "stench": None,
            "wall": pygame.image.load(WALL_IMG).convert_alpha(),
            "wall_outline": pygame.image.load(WALL_OUTLINE_IMG).convert_alpha(),
        }
    
    def get_converted_pos(self):
        return (self.x - 1) + 10 * (10 - self.y)

    def init_attribute_imgs(self):
        if self.content == "-":
            return
        for c in self.content:
            if c == "A":
                img = pygame.image.load(AGENT_RIGHT_IMG).convert_alpha()
                self.attribute_imgs["agent"] = img
            elif c == "G":
                img = pygame.image.load(CHEST_IMG).convert_alpha()
                self.attribute_imgs["gold"] = img
            elif c == "P":
                img = pygame.image.load(PIT_IMG).convert_alpha()
                self.attribute_imgs["pit"] = img
            elif c == "W":
                img = pygame.image.load(WUMPUS_IMG).convert_alpha()
                self.attribute_imgs["wumpus"] = img
            elif c == "S":
                img = pygame.image.load(STENCH_IMG).convert_alpha()
                self.attribute_imgs["stench"] = img
            elif c == "B":
                img = pygame.image.load(BREEZE_IMG).convert_alpha()
                self.attribute_imgs["breeze"] = img

    def valid_cell(self, x, y, grid_cells: list):
        if not self.map_size:
            self.map_size = int(math.sqrt(len(grid_cells)))
        find_index = lambda x, y: x-1 + (10-y) * 10

        if x < 0 or y < 0 or x > self.map_size or y > self.map_size:
            return False
        return grid_cells[find_index(x, y)]

    def draw(self, screen):
        x, y = self.x* CELL_SIZE, (11 - self.y) * CELL_SIZE
        if not self.attribute_imgs["arrow"] and not self.visited:
            pygame.draw.rect(
                screen, pygame.Color(173, 116, 96), (x, y, CELL_SIZE, CELL_SIZE)
            )
            self.attribute_imgs["wall_outline"] = pygame.transform.scale(
                self.attribute_imgs["wall_outline"], (CELL_SIZE , CELL_SIZE )
            )
            screen.blit(self.attribute_imgs["wall_outline"],(x,y,),)
        elif self.attribute_imgs["arrow"] and not self.visited:
            pygame.draw.rect(
                screen, pygame.Color(173, 116, 96), (x, y, CELL_SIZE, CELL_SIZE)
            )
            self.attribute_imgs["wall_outline"] = pygame.transform.scale(
                self.attribute_imgs["wall_outline"], (CELL_SIZE , CELL_SIZE )
            )
            screen.blit(self.attribute_imgs["wall_outline"],(x,y,),)
            self.attribute_imgs["arrow"] = pygame.transform.scale(
                self.attribute_imgs["arrow"], (CELL_SIZE, CELL_SIZE)
            )
            screen.blit(self.attribute_imgs["arrow"],(x,y,),)
            self.visited = True
            self.attribute_imgs["arrow"] = None
        elif self.attribute_imgs["arrow"] and self.visited:
            if self.attribute_imgs["wumpus"]:
                self.attribute_imgs["wumpus"] = pygame.transform.scale(
                    self.attribute_imgs["wumpus"], (CELL_SIZE // 1.5, CELL_SIZE // 1.5)
                )
                screen.blit(self.attribute_imgs["wumpus"],(x + CELL_SIZE // 6,y + CELL_SIZE // 6,),)

            self.attribute_imgs["arrow"] = pygame.transform.scale(
                self.attribute_imgs["arrow"], (CELL_SIZE, CELL_SIZE)
            )
            screen.blit(self.attribute_imgs["arrow"],(x,y,),)
            self.visited = True
            self.attribute_imgs["arrow"] = None
        elif self.visited:
            if self.attribute_imgs["wall"]:
                self.attribute_imgs["wall"] = pygame.transform.scale(
                    self.attribute_imgs["wall"], (CELL_SIZE, CELL_SIZE)
                )
                screen.blit(self.attribute_imgs["wall"],(x,y,),)
            self.draw_image_cell(screen)
        if self.attribute_imgs["agent"]: 
            self.attribute_imgs["agent"] = pygame.transform.scale(
                self.attribute_imgs["agent"], (CELL_SIZE, CELL_SIZE)
            )
            screen.blit(self.attribute_imgs["agent"],(x,y,),)

        pygame.draw.line(screen, pygame.Color(0, 0, 0), (x, y), (x + CELL_SIZE, y), 2)
        pygame.draw.line(screen,pygame.Color(0, 0, 0),(x + CELL_SIZE, y),(x + CELL_SIZE, y + CELL_SIZE),2,)
        pygame.draw.line(screen, pygame.Color(0, 0, 0), (x, y + CELL_SIZE), (x, y), 2)
        if self.x != 1 and self.y == 1:
            pygame.draw.line(screen,pygame.Color(0, 0, 0),(x + CELL_SIZE, y + CELL_SIZE),(x, y + CELL_SIZE),2,)
        else:
            exit_sc = pygame.font.Font(FONT_STYLE, 15).render("EXIT", True, (0, 0, 0))
            exit_rect = exit_sc.get_rect()
            exit_rect.center = pygame.Rect(
                x, y + CELL_SIZE, CELL_SIZE, CELL_SIZE // 2
            ).center
            screen.blit(exit_sc, exit_rect)

    def draw_image_cell(self, screen):
        x, y = self.x * CELL_SIZE, (11 - self.y) * CELL_SIZE
        if self.content == "-":
            return

        if self.attribute_imgs["gold"]:
            self.attribute_imgs["gold"] = pygame.transform.scale(
                self.attribute_imgs["gold"], (CELL_SIZE // 1.5, CELL_SIZE // 1.5)
            )
            screen.blit(self.attribute_imgs["gold"],(x + CELL_SIZE // 6, y + CELL_SIZE // 6,),)

        if self.attribute_imgs["wumpus"]:
            self.attribute_imgs["wumpus"] = pygame.transform.scale(
                self.attribute_imgs["wumpus"], (CELL_SIZE // 1.5, CELL_SIZE // 1.5)
            )
            screen.blit(self.attribute_imgs["wumpus"],(x + CELL_SIZE // 6, y + CELL_SIZE // 6,),)

        if self.attribute_imgs["pit"]:
            self.attribute_imgs["pit"] = pygame.transform.scale(
                self.attribute_imgs["pit"], (CELL_SIZE // 1.5, CELL_SIZE // 1.5)
            )
            screen.blit(self.attribute_imgs["pit"],(x + CELL_SIZE // 6, y + CELL_SIZE // 6,),)

        if self.attribute_imgs["agent"]:
            self.attribute_imgs["agent"] = pygame.transform.scale(
                self.attribute_imgs["agent"], (CELL_SIZE, CELL_SIZE)
            )
            screen.blit(self.attribute_imgs["agent"],(x,y,),)

        if "B" in self.content and "S" not in self.content:
            self.attribute_imgs["breeze"] = pygame.transform.scale(
                self.attribute_imgs["breeze"], (CELL_SIZE // 1.5, CELL_SIZE // 1.5)
            )
            screen.blit(
                self.attribute_imgs["breeze"],
                (
                    x + CELL_SIZE // 6,
                    y + CELL_SIZE // 6,
                ),
            )

        if "S" in self.content and "B" not in self.content:
            self.attribute_imgs["stench"] = pygame.transform.scale(
                self.attribute_imgs["stench"], (CELL_SIZE // 1.5, CELL_SIZE // 1.5),
            )
            screen.blit(
                self.attribute_imgs["stench"],
                (
                    x + (CELL_SIZE // 6),
                    y + (CELL_SIZE // 6),
                ),
            )
        
        if "S" in self.content and "B" in self.content:
            self.attribute_imgs["breeze"] = pygame.transform.scale(
                self.attribute_imgs["breeze"], (CELL_SIZE / 2, CELL_SIZE / 2)
            )
            screen.blit(
                self.attribute_imgs["breeze"],
                (
                    x,
                    y + (CELL_SIZE / 4),
                ),
            )

            self.attribute_imgs["stench"] = pygame.transform.scale(
                self.attribute_imgs["stench"], (CELL_SIZE / 2, CELL_SIZE / 2),
            )
            screen.blit(
                self.attribute_imgs["stench"],
                (
                    x + (CELL_SIZE / 2),
                    y + (CELL_SIZE / 4),
                ),
            )

class Cell_ALGO:
    def __init__(self, x, y, content: str) -> None:
        self.x = x
        self.y = y
        self.map_size = 10
        self.visited = False
        self.content = content
        self.parent = None
        self.is_safe = False
        self.attributes = { #use for run algorithms
            "arrow": False,
            "gold": False,
            "wumpus": False,
            "pit": False,
            "agent": False,
            "breeze": False,
            "stench": False,
        } 
    
    def get_converted_pos(self):
        return (self.x - 1) + 10 * (10 - self.y)

    def init_attribute_imgs(self):
        if self.content == "-":
            return
        for c in self.content:
            if c == "A":
                self.attributes["agent"] = True
            elif c == "G":
                self.attributes["gold"] = True
            elif c == "P":
                self.attributes["pit"] = True
            elif c == "W":
                self.attributes["wumpus"] = True
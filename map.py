from cell import *
from const import *
import pygame

class Map_UI:
    def __init__(self, file_name) -> None:
        self.map_size = 10
        self.file_name = file_name
        self.map = []

        self.init_map()

    def init_map(self):
        with open(self.file_name, "r") as file:
            self.map_size = int(file.readline())
            for i in range(self.map_size):
                line = file.readline()
                line.strip()
                cells = line.split(".")
                for j, cell in enumerate(cells):
                    # print(cell)
                    if cell == "A":
                        cell = Cell_UI(j + 1, self.map_size - i, "A") # since (1, 1) is the coord of bottom left
                    elif cell == "P":
                        cell = Cell_UI(j + 1, self.map_size - i, "P")
                    elif cell == "W":
                        cell = Cell_UI(j + 1, self.map_size - i, "W")
                    elif cell == "G":
                        cell = Cell_UI(j + 1, self.map_size - i, "G")
                    else:
                        cell = Cell_UI(j + 1, self.map_size - i, "-")

                    self.map.append(cell)

        self.infer_cell_attribute()
    
    def get_neighbors(self, cell):
        neighbors = []
        i = self.map_size * (self.map_size - cell.y) + cell.x - 1
        if cell.x > 1:
            neighbors.append(self.map[i - 1])
        if cell.x < 10:
            neighbors.append(self.map[i + 1])
        if cell.y > 1:
            neighbors.append(self.map[i + 10])
        if cell.y < 10:
            neighbors.append(self.map[i - 10])

        return neighbors
    
    def infer_cell_attribute(self):
        for cell in self.map:
            cell.init_attribute_imgs()

        for cell in self.map:
            neighbors = self.get_neighbors(cell)
            for neighbor in neighbors:
                if neighbor.attribute_imgs["wumpus"] != None:
                    img = pygame.image.load(STENCH_IMG).convert_alpha()
                    cell.attribute_imgs["stench"] = img
                    cell.content = cell.content.replace('-','')
                    cell.content += 'S'
  
                if neighbor.attribute_imgs["pit"] != None:
                    img = pygame.image.load(BREEZE_IMG).convert_alpha()
                    cell.attribute_imgs["breeze"] = img
                    cell.content = cell.content.replace('-','')
                    cell.content += 'B'
            
    def draw(self, screen):
        [cell.draw(screen) for cell in self.map]

    def get_agent_cell(self):
        for cell in self.map:
            if cell.content == "A":
                return cell
            
class Map_ALGO:
    def __init__(self, file_name) -> None:
        self.map_size = 10
        self.file_name = file_name
        self.map = []

        self.init_map()

    def init_map(self):
        with open(self.file_name, "r") as file:
            self.map_size = int(file.readline())
            for i in range(self.map_size):
                line = file.readline()
                line.strip()
                cells = line.split(".")
                for j, cell in enumerate(cells):
                    if cell == "A":
                        cell = Cell_ALGO(j + 1, self.map_size - i, "A") # since (1, 1) is the coord of bottom left
                    elif cell == "P":
                        cell = Cell_ALGO(j + 1, self.map_size - i, "P")
                    elif cell == "W":
                        cell = Cell_ALGO(j + 1, self.map_size - i, "W")
                    elif cell == "G":
                        cell = Cell_ALGO(j + 1, self.map_size - i, "G")
                    else:
                        cell = Cell_ALGO(j + 1, self.map_size - i, "-")

                    self.map.append(cell)

        self.infer_cell_attribute()

    def get_neighbors(self, cell):
        neighbors = []
        i = self.map_size * (self.map_size - cell.y) + cell.x - 1
        if cell.x > 1:
            neighbors.append(self.map[i - 1])
        if cell.x < 10:
            neighbors.append(self.map[i + 1])
        if cell.y > 1:
            neighbors.append(self.map[i + 10])
        if cell.y < 10:
            neighbors.append(self.map[i - 10])

        return neighbors

    def infer_cell_attribute(self):
        for cell in self.map:
            cell.init_attribute_imgs()

        for cell in self.map:
            neighbors = self.get_neighbors(cell)
            for neighbor in neighbors:
                if neighbor.attributes["wumpus"] != False:
                    cell.attributes["stench"] = True
                if neighbor.attributes["pit"] != False:
                    cell.attributes["breeze"] = True

    def get_agent_cell(self):
        for cell in self.map:
            if cell.content == "A":
                return cell
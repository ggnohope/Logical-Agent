from cell import Cell
from const import *


class Map:
    def __init__(self, file_name) -> None:
        self.map_size = 10  # 10x10
        self.cell_size = CELL_SIZE
        self.pit_discovered = []
        self.cell_discovered = []
        self.file_name = file_name
        self.grid_cells = []

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
                        cell = Cell(j, i, "A")
                    elif cell == "P":
                        cell = Cell(j, i, "P")
                    elif cell == "W":
                        cell = Cell(j, i, "W")
                    elif cell == "G":
                        cell = Cell(j, i, "G")
                    else:
                        cell = Cell(j, i, "-")

                    self.grid_cells.append(cell)

        self.init_breeze_stench()
        for cell in self.grid_cells:
            cell.init_img_list()

    def init_breeze_stench(self):
        for cell in self.grid_cells:
            neighbors = cell.get_neighbors(self.grid_cells)
            neighbor_types = {"P": False, "W": False}
            if any("P" in neighbor.type for neighbor in neighbors):
                neighbor_types["P"] = True
            if any("W" in neighbor.type for neighbor in neighbors):
                neighbor_types["W"] = True

            if (
                cell.type == "A"
                or cell.type == "G"
                or cell.type == "P"
                or cell.type == "W"
            ):
                cell.type += "B" if neighbor_types["P"] == True else ""
                cell.type += "S" if neighbor_types["W"] == True else ""
            elif cell.type == "-":
                cell.type = ""
                cell.type += "B" if neighbor_types["P"] == True else ""
                cell.type += "S" if neighbor_types["W"] == True else ""
                if cell.type == "":
                    cell.type = "-"

        # After this function, a type of any cell can be: (A,P,W,G,-,B,S,AB,AS,ABS,GB,GS,GBS,PB,PS,PBS,WB,WS,WBS,BS)

    def draw(self, screen):
        [cell.draw(screen) for cell in self.grid_cells]

    def get_agent_cell(self):
        for cell in self.grid_cells:
            if "A" in cell.type:
                return cell

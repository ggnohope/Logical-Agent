import pygame
from const import *
from solver import *

class Agent:
    def __init__(self) -> None:
        self.score = 0
        self.gold = 0
        self.current_cell = None
        self.direction = TURN_RIGHT

    def make_moves(self, map, kb, action_list):

        remove_list = []
        converted_pos_neighbors = []
        current_converted_pos = self.current_cell.get_converted_pos()

        left = current_converted_pos - 1
        right = current_converted_pos + 1
        top = current_converted_pos - 10
        bottom = current_converted_pos + 10

        neighbors = map.get_neighbors(self.current_cell)

        for neighbor in neighbors:
            converted_pos_neighbors.append(neighbor.get_converted_pos())

        if self.current_cell.attributes["breeze"] == True:
            for converted_pos_neighbor in converted_pos_neighbors:
                temp_kb = kb.get_clauses()
                temp_kb.append([(-1) * (PIT + converted_pos_neighbor)])
                solver = SATSolver(temp_kb)
                if solver.solve() == False:
                    action_list.append(DETECT_PIT)
                    kb.add_clause([PIT + converted_pos_neighbor])
                    if converted_pos_neighbor not in remove_list:
                        remove_list.append(converted_pos_neighbor)
                else:
                    temp_kb = kb.get_clauses()
                    temp_kb.append([PIT + converted_pos_neighbor])
                    solver = SATSolver(temp_kb)
                    if solver.solve() == False:
                        action_list.append(DETECT_NO_PIT)
                        kb.add_clause([(-1) * (PIT + converted_pos_neighbor)])
                    else:
                        action_list.append(FAIL_TO_INFER_PIT)
                        remove_list.append(converted_pos_neighbor)

        if self.current_cell.attributes["stench"] == True:
            for converted_pos_neighbor in converted_pos_neighbors:
                temp_kb = kb.get_clauses()
                temp_kb.append([(WUMPUS + converted_pos_neighbor) * (-1)])
                solver = SATSolver(temp_kb)
                if solver.solve() == False:
                    action_list.append(DETECT_WUMPUS)

                    if converted_pos_neighbor == left and self.direction != TURN_LEFT:
                        action_list.append(TURN_LEFT)
                        self.direction = TURN_LEFT
                    if converted_pos_neighbor == right and self.direction != TURN_RIGHT:
                        action_list.append(TURN_RIGHT)
                        self.direction = TURN_RIGHT
                    if converted_pos_neighbor == top and self.direction != TURN_UP:
                        action_list.append(TURN_UP)
                        self.direction = TURN_UP
                    if converted_pos_neighbor == bottom and self.direction != TURN_DOWN:
                        action_list.append(TURN_DOWN)
                        self.direction = TURN_DOWN
                    action_list.append(SHOOT_ARROW)
                    action_list.append(KILL_WUMPUS)

                    # remove wumpus and stench of neighbors
                    map.remove_wumpus(converted_pos_neighbor)

                    #update knowledge base
                    symbol = WUMPUS + converted_pos_neighbor

                    kb.clauses = [clause for clause in kb.clauses if symbol in clause or -symbol in clause]

                    # wumpus and pit can not be the same cell
                    kb.add_clause([(PIT + converted_pos_neighbor) * (-1)])
                else:
                    temp_kb = kb.get_clauses()
                    temp_kb.append([WUMPUS + converted_pos_neighbor])
                    solver = SATSolver(temp_kb)
                    if solver.solve() == False:
                        action_list.append(DETECT_NO_WUMPUS)
                        kb.add_clause([(WUMPUS + converted_pos_neighbor) * (-1)])
                    else: # cant infer whether this neighbor cell has wumpus or not, we dont move to this cell
                        action_list.append(FAIL_TO_INFER_WUMPUS)
                        if converted_pos_neighbor not in remove_list:
                            remove_list.append(converted_pos_neighbor)
            
            if self.current_cell.attributes["stench"] != True:
                if [STENCH + self.current_cell.get_converted_pos()] in kb.clauses:
                    kb.clauses.remove([STENCH + self.current_cell.get_converted_pos()])
                kb.add_clause([(STENCH + self.current_cell.get_converted_pos()) * (-1)])

        for neighbor in remove_list:
            converted_pos_neighbors.remove(neighbor)

        result = []
        for converted_pos_neighbor in converted_pos_neighbors:
            if map.map[converted_pos_neighbor].visited == False:
                result.append(map.map[converted_pos_neighbor])

        return result

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

        map.map[i].attributes["agent"] = False
        map.map[i - 10].attributes["agent"] = True
        self.current_cell = map.map[i - 10]

    def move_down(self, map):
        i = self.current_cell.get_converted_pos()

        map.map[i].attributes["agent"] = False
        map.map[i + 10].attributes["agent"] = True
        self.current_cell = map.map[i + 10]

    def move_right(self, map):
        i = self.current_cell.get_converted_pos()

        map.map[i].attributes["agent"] = False
        map.map[i + 1].attributes["agent"] = True
        self.current_cell = map.map[i + 1]

    def move_left(self, map):
        i = self.current_cell.get_converted_pos()

        map.map[i].attributes["agent"] = False
        map.map[i - 1].attributes["agent"] = True
        self.current_cell = map.map[i - 1]

    def move_backward(self, map, action_list):
        if self.direction == TURN_UP:
            self.back_up(map)
            action_list.append(TURN_DOWN)
            action_list.append(MOVE_FORWARD)
        elif self.direction == TURN_DOWN:
            self.back_down(map)
            action_list.append(TURN_UP)
            action_list.append(MOVE_FORWARD)
        elif self.direction == TURN_LEFT:
            self.back_left(map)
            action_list.append(TURN_RIGHT)
            action_list.append(MOVE_FORWARD)
        elif self.direction == TURN_RIGHT:
            self.back_right(map)
            action_list.append(TURN_LEFT)
            action_list.append(MOVE_FORWARD)

    def back_up(self, map):
        i = self.current_cell.get_converted_pos()

        map.map[i].attributes["agent"] = False
        map.map[i + 10].attributes["agent"] = True
        self.current_cell = map.map[i + 10]

    def back_down(self, map):
        i = self.current_cell.get_converted_pos()

        map.map[i].attributes["agent"] = False
        map.map[i - 10].attributes["agent"] = True
        self.current_cell = map.map[i - 10]

    def back_right(self, map):
        i = self.current_cell.get_converted_pos()

        map.map[i].attributes["agent"] = False
        map.map[i - 1].attributes["agent"] = True
        self.current_cell = map.map[i - 1]

    def back_left(self, map):
        i = self.current_cell.get_converted_pos()

        map.map[i].attributes["agent"] = False
        map.map[i + 1].attributes["agent"] = True
        self.current_cell = map.map[i + 1]

    # def turn_up(self):
    #     self.cell.img_list["agent"] = pygame.image.load(AGENT_UP_IMG).convert_alpha()
    #     self.direction = TURN_UP

    # def turn_down(self):
    #     self.cell.img_list["agent"] = pygame.image.load(AGENT_DOWN_IMG).convert_alpha()
    #     self.direction = TURN_DOWN

    # def turn_left(self):
    #     self.cell.img_list["agent"] = pygame.image.load(AGENT_LEFT_IMG).convert_alpha()
    #     self.direction = TURN_LEFT

    # def turn_right(self):
    #     self.cell.img_list["agent"] = pygame.image.load(AGENT_RIGHT_IMG).convert_alpha()
    #     self.direction = TURN_RIGHT

    # def shoot_arrow(self, grid_cells: list):
    #     if self.direction == TURN_UP:
    #         arrow_cell = self.cell.check_cell(self.cell.x, self.cell.y - 1, grid_cells)
    #         arrow_cell.img_list["arrow"] = pygame.image.load(
    #             ARROW_UP_IMG
    #         ).convert_alpha()
    #     elif self.direction == TURN_DOWN:
    #         arrow_cell = self.cell.check_cell(self.cell.x, self.cell.y + 1, grid_cells)
    #         arrow_cell.img_list["arrow"] = pygame.image.load(
    #             ARROW_DOWN_IMG
    #         ).convert_alpha()
    #     elif self.direction == TURN_LEFT:
    #         arrow_cell = self.cell.check_cell(self.cell.x - 1, self.cell.y, grid_cells)
    #         arrow_cell.img_list["arrow"] = pygame.image.load(
    #             ARROW_LEFT_IMG
    #         ).convert_alpha()
    #     elif self.direction == TURN_RIGHT:
    #         arrow_cell = self.cell.check_cell(self.cell.x + 1, self.cell.y, grid_cells)
    #         arrow_cell.img_list["arrow"] = pygame.image.load(
    #             ARROW_RIGHT_IMG
    #         ).convert_alpha()

    #     self.score -= 100

    #     return arrow_cell

    # def check_collide_pit_or_wumpus(self):
    #     if "W" in self.cell.type or "P" in self.cell.type:
    #         self.score -= 10000
    #         return True

    # def collect_gold(self):
    #     self.cell.type = self.cell.type.replace("G", "")
    #     self.cell.img_list["gold"] = None
    #     self.gold += 1
    #     self.score += 1000

    # def climb_out(self):
    #     self.score += 10

from agent import Agent
from map import *
from solver import *
from const import *

class Controller:
    def __init__(self, map, current_cell):
        self.current_cell = current_cell
        self.grid_cells = map
        self.kb = KnowledgeBase()
        self.action_list = []
        self.remain_cells = []
        self.direction = TURN_RIGHT

    def get_neighbors(self, cell):
        neighbors = []
        i = 10 * (10 - cell.y) + cell.x - 1
        if cell.x > 1:
            neighbors.append(self.grid_cells[i - 1])
        if cell.x < 10:
            neighbors.append(self.grid_cells[i + 1])
        if cell.y > 1:
            neighbors.append(self.grid_cells[i + 10])
        if cell.y < 10:
            neighbors.append(self.grid_cells[i - 10])

        return neighbors
    
    def indicate_turn(self, current_cell, neighbor):
        current_converted_pos = current_cell.get_converted_pos()
        converted_pos_neighbor = neighbor.get_converted_pos()
        left = current_converted_pos - 1
        right = current_converted_pos + 1
        top = current_converted_pos - 10
        bottom = current_converted_pos + 10

        if converted_pos_neighbor == left and self.direction != TURN_LEFT:
            self.action_list.append(TURN_LEFT)
            self.direction = TURN_LEFT
        if converted_pos_neighbor == right and self.direction != TURN_RIGHT:
            self.action_list.append(TURN_RIGHT)
            self.direction = TURN_RIGHT
        if converted_pos_neighbor == top and self.direction != TURN_UP:
            self.action_list.append(TURN_UP)
            self.direction = TURN_UP
        if converted_pos_neighbor == bottom and self.direction != TURN_DOWN:
            self.action_list.append(TURN_DOWN)
            self.direction = TURN_DOWN

    def remove_wumpus(self, cell):
        if cell.attributes["wumpus"] == False:
            return
        
        cell.attributes["wumpus"] = False

        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            is_delete_stench = True
            neighbors_of_neighbor = self.get_neighbors(neighbor)
            if self.current_cell in neighbors_of_neighbor:
                neighbors_of_neighbor.remove(cell)
            for cell in neighbors_of_neighbor:
                if cell.attributes["wumpus"] == True:
                    is_delete_stench = False
                    break
            if is_delete_stench:
                neighbor.attributes["stench"] = False

    def make_moves(self, neighbors):
        remove_list = []
        if self.current_cell.attributes["breeze"] == True:
            for neighbor in neighbors:
                self.indicate_turn(self.current_cell, neighbor)
                temp_kb = self.kb.get_clauses()
                temp_kb.append([(-1) * (PIT + neighbor.get_converted_pos())])
                solver = Solver(temp_kb)
                if solver.is_satisfiable() == False:
                    neighbor.infered = True
                    self.action_list.append(DETECT_PIT)
                    self.kb.add_clause([PIT + neighbor.get_converted_pos()])
                    if neighbor not in remove_list:
                        remove_list.append(neighbor)
                else:
                    temp_kb = self.kb.get_clauses()
                    temp_kb.append([PIT + neighbor.get_converted_pos()])
                    solver = Solver(temp_kb)
                    if solver.is_satisfiable() == False:
                        neighbor.infered = True
                        self.action_list.append(DETECT_NO_PIT)
                        self.kb.add_clause([(-1) * (PIT + neighbor.get_converted_pos())])
                    else:
                        self.action_list.append(FAIL_TO_INFER_PIT)
                        if neighbor not in remove_list:
                            remove_list.append(neighbor)

        if self.current_cell.attributes["stench"] == True:
            for neighbor in neighbors:
                self.indicate_turn(self.current_cell, neighbor)
                temp_kb = self.kb.get_clauses()
                temp_kb.append([(WUMPUS + neighbor.get_converted_pos()) * (-1)])
                solver = Solver(temp_kb)
                if solver.is_satisfiable() == False:
                    self.action_list.append(DETECT_WUMPUS)
                    self.action_list.append(SHOOT_ARROW)
                    self.action_list.append(KILL_WUMPUS)

                    # remove wumpus and stench of neighbors
                    self.remove_wumpus(neighbor)

                    #update knowledge base
                    symbol = WUMPUS + neighbor.get_converted_pos()
                    self.kb.clauses = [clause for clause in self.kb.clauses if symbol not in clause or -symbol not in clause]

                    # wumpus and pit can not be the same cell
                    self.kb.add_clause([(PIT + neighbor.get_converted_pos()) * (-1)])
                else:
                    temp_kb = self.kb.get_clauses()
                    temp_kb.append([WUMPUS + neighbor.get_converted_pos()])
                    solver = Solver(temp_kb)
                    if solver.is_satisfiable() == False:
                        neighbor.infered = True
                        self.action_list.append(DETECT_NO_WUMPUS)
                        self.kb.add_clause([(WUMPUS + neighbor.get_converted_pos()) * (-1)])
                    else: # cant infer whether this neighbor cell has wumpus or not, we dont move to this cell
                        self.action_list.append(FAIL_TO_INFER_WUMPUS)
                        if neighbor not in remove_list:
                            remove_list.append(neighbor)
            
            if self.current_cell.attributes["stench"] != True:
                if [STENCH + self.current_cell.get_converted_pos()] in self.kb.clauses:
                    self.kb.clauses.remove([STENCH + self.current_cell.get_converted_pos()])
                self.kb.add_clause([(STENCH + self.current_cell.get_converted_pos()) * (-1)])

        for neighbor in remove_list:
            neighbors.remove(neighbor)

        return neighbors

    def explore_world(self):
        if self.current_cell.attributes["pit"] == True:
            self.action_list.append(KILLED_BY_PIT)
            return False
        
        if self.current_cell.attributes["wumpus"] == True:
            self.action_list.append(KILLED_BY_WUMPUS)
            return False
        
        if self.current_cell.attributes["gold"] == True:
            self.action_list.append(COLLECT_GOLD)

        neighbors = self.get_neighbors(self.current_cell)

        if self.current_cell.attributes["stench"] == True:
            self.action_list.append(PERCEIVE_STENCH)
            self.kb.add_clause([STENCH + self.current_cell.get_converted_pos()])
            clause = [-1 * (STENCH + self.current_cell.get_converted_pos())]
            for neighbor in neighbors:
                clause.append(WUMPUS + neighbor.get_converted_pos())
            self.kb.add_clause(clause)
            for neighbor in neighbors:
                self.kb.add_clause([STENCH + self.current_cell.get_converted_pos(), -1 * (WUMPUS + neighbor.get_converted_pos())])
        else:
            self.kb.add_clause([-1 * (STENCH + self.current_cell.get_converted_pos())])
            for neighbor in neighbors:
                self.kb.add_clause([-1*(WUMPUS + neighbor.get_converted_pos())])

        if self.current_cell.attributes["breeze"] == True:
            self.action_list.append(PERCEIVE_BREEZE)
            self.kb.add_clause([BREEZE + self.current_cell.get_converted_pos()])
            clause = [-1 * (BREEZE + self.current_cell.get_converted_pos())]
            for neighbor in neighbors:
                clause.append(PIT + neighbor.get_converted_pos())
            self.kb.add_clause(clause)
            for neighbor in neighbors:
                self.kb.add_clause([BREEZE + self.current_cell.get_converted_pos(), -1 * (PIT + neighbor.get_converted_pos())])
        else:
            self.kb.add_clause([-1 * (BREEZE + self.current_cell.get_converted_pos())])
            for neighbor in neighbors:
                self.kb.add_clause([-1*(PIT + neighbor.get_converted_pos())])

        remove_list = []
        for neighbor in neighbors:
            if neighbor == self.current_cell.parent:
                remove_list.append(neighbor)
            elif neighbor.visited == True:
                remove_list.append(neighbor)
            elif neighbor.infered == True:
                remove_list.append(neighbor)
        
        for cell in remove_list:
            neighbors.remove(cell)

        next_moves = self.make_moves(neighbors)

        current_cell = self.current_cell

        for move in next_moves:
            if move not in self.remain_cells and move.visited == False:
                self.remain_cells.append(move)

        for move in next_moves:
            if move in self.remain_cells:
                self.remain_cells.remove(move)
            if move.visited == False:
                move.visited = True
                self.indicate_turn(self.current_cell, move)
                self.action_list.append(MOVE_FORWARD)
                self.current_cell = move
                self.current_cell.parent = current_cell

                result = self.explore_world()
                if result == False:
                    return False

                if len(self.remain_cells) == 0:
                    return True

                self.indicate_turn(self.current_cell, current_cell)
                self.action_list.append(MOVE_FORWARD)
                self.current_cell = current_cell
            
        return True
        
    def backtrace_path(self, cell):
        if cell.parent == None:
            return
        self.backtrace_path(cell.parent)
        self.indicate_turn(cell.parent, cell)
        self.action_list.append(MOVE_FORWARD)

    
    def find_exit(self):
        exit_pos = 90
        if self.grid_cells[exit_pos].visited == False:
            return False
        
        for cell in self.grid_cells:
            cell.parent = None
        
        frontier = []
        expanded_set = set()
        frontier.append(self.current_cell)
        while len(frontier) != 0:
            current_cell = frontier.pop()
            expanded_set.add((current_cell.x, current_cell.y))

            if current_cell.x == 1 and current_cell.y == 1:
                self.backtrace_path(current_cell)
                return True

            neighbors = self.get_neighbors(current_cell)

            neighbors = [neighbor for neighbor in neighbors if neighbor.visited and (neighbor.x, neighbor.y) not in expanded_set]

            for neighbor in neighbors:
                frontier.append(neighbor)
                neighbor.parent = current_cell
        
        return False

import pygame
pygame.init()
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

map = Map_ALGO(MAP_3)
agent = Agent()

agent.current_cell = map.get_agent_cell()
agent.current_cell.visited = True
controller = Controller(map.map, agent.current_cell)
if controller.explore_world():
    if controller.find_exit():
        controller.action_list.append(ESCAPE_SUCCESS)
print(controller.action_list)
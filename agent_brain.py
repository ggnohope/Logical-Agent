class AgentBrain:
    def __init__(self, current_cell, grid_cells):
        self.current_cell = current_cell
        self.grid_cells = grid_cells
        self.action_list = []
        self.action_cells = {}
        self.found_exit = False
        self.remain_cells = []
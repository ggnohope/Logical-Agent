import random
import sys

import pygame

from agent import *
from const import *
from map import *
from noti import Noti
from buttons import *
from action import *
# from test import action_list

from controller import *
# controller = Controller(map.map, agent.current_cell)
# controller.explore_world()
# print(controller.action_list)

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.caption = pygame.display.set_caption(TITLE)
        self.font = pygame.font.Font(FONT_STYLE, 15)
        self.font_score = pygame.font.Font(FONT_STYLE, 15)
        self.font_title = pygame.font.Font(FONT_STYLE, 30)

        self.map = None
        self.mapName = 0
        self.map_size = None

        self.state = "menu"

        self.agent = Agent()
        
        self.agent_brain = None
        self.action_list = None

        self.current_step = 0
        
        self.length_header = MAIN_BUTTON_LENGTH/3*2
        x_header = (CELL_SIZE*10 - 4*self.length_header) / 6
        self.posx_level = [x_header + CELL_SIZE, 2*x_header+self.length_header + CELL_SIZE, 3*x_header+2*self.length_header + CELL_SIZE, 4*x_header+3*self.length_header + CELL_SIZE]
        self.posy = WINDOW_HEIGHT*0
        self.button_reset = Buttons(self, WHITE, self.posx_level[0], self.posy, self.length_header, MAIN_BUTTON_HEIGHT, 'Reset')
        self.button_step = Buttons(self, WHITE, self.posx_level[1], self.posy, self.length_header, MAIN_BUTTON_HEIGHT, 'Step')
        self.button_play = Buttons(self, WHITE, self.posx_level[2], self.posy, self.length_header, MAIN_BUTTON_HEIGHT, 'Play')
        self.button_pause = Buttons(self, WHITE, self.posx_level[3], self.posy, self.length_header, MAIN_BUTTON_HEIGHT, 'Pause')
        
        self.is_reset = False
        self.is_step = False
        self.is_playing = True
        
        x_map = WINDOW_WIDTH/2 + CELL_SIZE*4
        y_map = WINDOW_HEIGHT/10 
        posy_map = [WINDOW_HEIGHT/2.8 + y_map,WINDOW_HEIGHT/2.8 + y_map*2,WINDOW_HEIGHT/2.8 + y_map*3,WINDOW_HEIGHT/2.8 + y_map*4, WINDOW_HEIGHT/2.8 + y_map*5]
        self.map1 = Buttons(self, WHITE, x_map , posy_map[0], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 1')
        self.map2 = Buttons(self, WHITE, x_map , posy_map[1], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 2')
        self.map3 = Buttons(self, WHITE, x_map , posy_map[2], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 3')
        self.map4 = Buttons(self, WHITE, x_map , posy_map[3], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 4')
        self.map5 = Buttons(self, WHITE, x_map , posy_map[4], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 5')
        
    def run(self):
        # self.sketch_main_screen()
        self.sketch_main_screen()
        while True:
            self.sketch_layout()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.event_mouse_motion(event, pos)
                self.event_mouse_click(event, pos)
                
            if self.state == "running":
                if self.is_playing == True:
                    self.show_result()
                elif self.is_step == True:
                    self.show_result()
                    self.is_step = False
                else: 
                    self.sketch_running_screen()
            elif self.state == "success":
                self.sketch_success_screen()
            elif self.state == "failed":
                self.sketch_failed_screen()

    def sketch_main_screen(self):
        self.sketch_layout()
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.event_mouse_motion(event, pos)
            self.event_mouse_click(event, pos)

    def sketch_running_screen(self, noti_type: Noti = None):
        # Draw filter
        pygame.draw.rect(self.screen, pygame.Color('White'), (CELL_SIZE*12, CELL_SIZE*2, WINDOW_WIDTH - CELL_SIZE*12, WINDOW_HEIGHT/4))

        # draw score and gold collected
        self.sketch_score()
        self.sketch_gold()
        
        self.map.draw(self.screen)
        
        # draw Noti
        if noti_type:
            self.sketch_noti(noti_type)

        pygame.display.update()
        # pygame.time.delay(1000)
        
    def show_result(self):
        self.sketch_running_screen()

        # return if finish the action`` list
        if self.current_step == len(self.action_list):
            if self.action_list[-1] == ESCAPE_SUCCESS:
                self.state = "success"
                self.reset(None)
            else:
                self.state = "failed"
                self.reset(None)
            return

        i = self.agent.current_cell.get_converted_pos()
        if self.agent.direction == TURN_UP and i-10 > 0:
                cell_ahead = self.map.map[i-10]
        elif self.agent.direction == TURN_LEFT and i-1 > 0:
            cell_ahead = self.map.map[i-1]
        elif self.agent.direction == TURN_DOWN and i+10 < 100:
            cell_ahead = self.map.map[i+10]
        elif self.agent.direction == TURN_RIGHT and i+1 < 100:
            cell_ahead = self.map.map[i+1]
                
        # get action
        action = self.action_list[self.current_step]
        action2 = None
        if(self.current_step + 1 < len(self.action_list)):
            action2 = self.action_list[self.current_step+1]
            
        # increase the step
        if len(self.action_list) > self.current_step:
            self.current_step += 1

        # print(action)
        if action == Action.TURN_LEFT.value and not action2 == Action.FAIL_TO_INFER_PIT.value:
            self.agent.turn_left()
        elif action == Action.TURN_RIGHT.value and not action2 == Action.FAIL_TO_INFER_PIT.value:
            self.agent.turn_right()
        elif action == Action.TURN_UP.value and not action2 == Action.FAIL_TO_INFER_PIT.value:
            self.agent.turn_up()
        elif action == Action.TURN_DOWN.value and not action2 == Action.FAIL_TO_INFER_PIT.value:
            self.agent.turn_down()
        elif action == Action.MOVE_FORWARD.value:
            self.agent.move_forward(self.map)
        elif action == Action.COLLECT_GOLD.value:
            self.sketch_running_screen(Noti.COLLECT_GOLD)
            self.agent.collect_gold()
        elif action == Action.PERCEIVE_BREEZE.value:
            self.sketch_running_screen(Noti.PERCEIVE_BREEZE)
        elif action == Action.PERCEIVE_STENCH.value:
            self.sketch_running_screen(Noti.PERCEIVE_STENCH)
        elif action == Action.SHOOT.value:
            arrow_cell = self.agent.shoot_arrow(self.map.map)
            self.sketch_running_screen(Noti.SHOOT_ARROW)
            arrow_cell.content = arrow_cell.content.replace("W", "")
            arrow_cell.attribute_imgs["wumpus"] = None
            arrow_cell.visited = True
            adjacents = arrow_cell.get_neighbors(self.map.map)
            for adjacent in adjacents:
                adjacent.attribute_imgs["stench"] = None
                adjacent.content = adjacent.content.replace('S', '')
        elif action == Action.KILL_WUMPUS.value:
            self.sketch_running_screen(Noti.KILL_WUMPUS)
        elif action == Action.KILL_NO_WUMPUS.value:
            self.sketch_running_screen(Noti.KILL_NO_WUMPUS)
        elif action == Action.KILL_BY_WUMPUS.value:
            self.sketch_running_screen(Noti.KILL_BY_WUMPUS)
        elif action == Action.KILL_BY_PIT.value:
            self.sketch_running_screen(Noti.KILL_BY_PIT)
        elif action == Action.CLIMB_OUT_OF_THE_CAVE.value:
            self.sketch_running_screen(Noti.CLIMB_OUT_OF_THE_CAVE)
        elif action == Action.DETECT_PIT.value:
            cell_ahead.visited = True
            self.sketch_running_screen(Noti.DETECT_PIT)
        elif action == Action.DETECT_WUMPUS.value:
            print('Detect wumpus')
            cell_ahead.visited = True
            self.sketch_running_screen(Noti.DETECT_WUMPUS)
        elif action == Action.DETECT_NO_PIT.value:
            cell_ahead.visited = True
        elif action == Action.DETECT_NO_WUMPUS.value:
            cell_ahead.visited = True
        elif action == Action.INFER_PIT.value:
            self.sketch_running_screen(Noti.INFER_PIT)
        elif action == Action.INFER_WUMPUS.value:
            self.sketch_running_screen(Noti.INFER_WUMPUS)
        elif action == Action.REMOVE_KNOWLEDGE_RELATED_TO_WUMPUS.value:
            print("Remove knowledge related to killed wumpus")
        elif action == Action.SHOOT_RANDOMLY.value:
            print("Start shooting randomly")
        elif action == Action.FAIL_TO_INFER_PIT.value:
            # infer_cell = self.agent_brain.action_cells[self.current_step - 1]
            # infer_cell_x, infer_cell_y = infer_cell.x, infer_cell.y
            print("Fail to infer cell:")
            # self.sketch_running_screen(Noti.FAIL_TO_INFER_PIT)
        elif action == Action.FAIL_TO_ESCAPE.value:
            print("Agent fail to find way out")
        else:
            print("Unknown action")
        
        self.sketch_running_screen()
        delay_time = 30
        # if self.map.file_name == MAP_5:
        #     delay_time = 50
        pygame.time.delay(delay_time)

    def solve(self, map, agent_current_cell):
        controller = Controller(map, agent_current_cell)
        if controller.explore_world():
            if controller.find_exit():
                controller.action_list.append(ESCAPE_SUCCESS)
        self.action_list = controller.action_list

    def sketch_map_select(self):
        self.screen.fill(pygame.Color('White'))
        self.map1.sketch_button(STEELBLUE)
        self.map2.sketch_button(STEELBLUE)
        self.map3.sketch_button(STEELBLUE)
        self.map4.sketch_button(STEELBLUE)
        self.map5.sketch_button(STEELBLUE)
        
    def sketch_footer_select(self):
        self.button_reset.sketch_button(STEELBLUE)
        self.button_step.sketch_button(STEELBLUE)
        self.button_play.sketch_button(STEELBLUE)
        self.button_pause.sketch_button(STEELBLUE)
    
    def sketch_title(self):
        text = self.font_title.render("Wumpus World", True, (23, 127, 117))
        text_rect = text.get_rect()
        text_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 6,
            WINDOW_HEIGHT // 12,
        )
        self.screen.blit(text, text_rect)
        
    def sketch_layout(self):
        pygame.display.update()
        self.screen.fill(pygame.Color('White'))
        self.sketch_map_select()
        self.sketch_footer_select()
        self.sketch_title()
        pygame.draw.line(self.screen, pygame.Color('Black'), (CELL_SIZE*11.5, 0), (CELL_SIZE*11.5, WINDOW_HEIGHT), 2)
    
    def sketch_score(self):
        score = self.agent.score
        score_text = self.font_score.render(
            "YOUR SCORE: " + str(score), True, (0, 0, 0)
        )
        score_rect = score_text.get_rect()
        score_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 6,
            WINDOW_HEIGHT // 5,
        )
        self.screen.blit(score_text, score_rect)
        
    def sketch_gold(self):
        gold = self.agent.gold
        gold_text = self.font.render("Gold collected: " + str(gold), True, (0, 0, 0))
        gold_rect = gold_text.get_rect()
        gold_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 6,
            WINDOW_HEIGHT // 4,
        )
        self.screen.blit(gold_text, gold_rect)
        
    def event_mouse_motion(self, event, pos):
        self.map1.colour, self.map2.colour, self.map3.colour, self.map4.colour, self.map5.colour = WHITE, WHITE, WHITE, WHITE, WHITE
        self.button_reset.colour, self.button_step.colour, self.button_play.colour, self.button_pause.colour = WHITE, WHITE, WHITE, WHITE
        # if event.type == pygame.MOUSEMOTION:
        if self.map1.isOver(pos):
            self.map1.colour = (23, 127, 117)
        elif self.map2.isOver(pos):
            self.map2.colour = (23, 127, 117)
        elif self.map3.isOver(pos):
            self.map3.colour = (23, 127, 117)
        elif self.map4.isOver(pos):
            self.map4.colour = (23, 127, 117)
        elif self.map5.isOver(pos):
            self.map5.colour = (23, 127, 117)
        elif self.button_reset.isOver(pos):
            self.button_reset.colour = (23, 127, 117)
        elif self.button_step.isOver(pos):
            self.button_step.colour = (23, 127, 117)
        elif self.button_play.isOver(pos):
            self.button_play.colour = (23, 127, 117)
        elif self.button_pause.isOver(pos):
            self.button_pause.colour = (23, 127, 117)
        
    def event_mouse_click(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.map1.colour, self.map2.colour, self.map3.colour, self.map4.colour, self.map5.colour, self.button_reset.colour,self.button_step.colour,self.button_play.colour, self.button_pause.colour = WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE
            if self.map1.isOver(pos):
                self.mapName = MAP_1
                self.map = Map_UI(MAP_1)      
                map = Map_ALGO(MAP_1)
                self.map_size = self.map.map_size
                self.agent.current_cell = self.map.get_agent_cell()
                self.agent.current_cell.visited = True
                self.agent.map_size = self.map.map_size
                self.solve(map.map, map.get_agent_cell())
                self.state = "running"
                
            elif self.map2.isOver(pos):
                self.mapName = MAP_2
                self.map = Map_UI(MAP_2)      
                map = Map_ALGO(MAP_2)
                self.map_size = self.map.map_size
                self.agent.current_cell = self.map.get_agent_cell()
                self.agent.current_cell.visited = True
                self.agent.map_size = self.map.map_size
                self.solve(map.map, map.get_agent_cell())
                self.state = "running"
            elif self.map3.isOver(pos):
                self.mapName = MAP_3
                self.map = Map_UI(MAP_3)      
                map = Map_ALGO(MAP_3)
                self.map_size = self.map.map_size
                self.agent.current_cell = self.map.get_agent_cell()
                self.agent.current_cell.visited = True
                self.agent.map_size = self.map.map_size
                self.solve(map.map, map.get_agent_cell())
                self.state = "running"
            elif self.map4.isOver(pos):
                self.mapName = MAP_4
                self.map = Map_UI(MAP_4)      
                map = Map_ALGO(MAP_4)
                self.map_size = self.map.map_size
                self.agent.current_cell = self.map.get_agent_cell()
                self.agent.current_cell.visited = True
                self.agent.map_size = self.map.map_size
                self.solve(map.map, map.get_agent_cell())
                self.state = "running"
            elif self.map5.isOver(pos):
                self.mapName = MAP_5
                self.map = Map_UI(MAP_5)      
                map = Map_ALGO(MAP_5)
                self.map_size = self.map.map_size
                self.agent.current_cell = self.map.get_agent_cell()
                self.agent.current_cell.visited = True
                self.agent.map_size = self.map.map_size
                self.solve(map.map, map.get_agent_cell())
                self.state = "running"
            elif self.button_reset.isOver(pos):
                self.is_reset == True
                self.map == None
                self.map_size = None
                self.agent = Agent()
                self.action_list = None
                self.current_step = 0
                if self.map:
                    self.is_playing= False
                    self.map = Map_UI(self.mapName)      
                    map = Map_ALGO(self.mapName)
                    self.map_size = self.map.map_size
                    self.agent.current_cell = self.map.get_agent_cell()
                    self.agent.current_cell.visited = True
                    self.agent.map_size = self.map.map_size
                    self.solve(map.map, map.get_agent_cell())
                    self.state = "running"
                    
            elif self.button_step.isOver(pos):
                self.is_playing = False
                self.is_step = True
            elif self.button_play.isOver(pos):
                self.is_playing = not (self.is_playing)
                self.is_step = False
            elif self.button_pause.isOver(pos):
                self.is_playing = False 
                self.is_step = False    
    
    def sketch_noti(self, noti_type: Noti):
        if noti_type == Noti.KILL_WUMPUS:
            text = self.font.render("KILL WUMPUS !", True, (23, 127, 117))
            img = pygame.image.load(WUMPUS_IMG).convert_alpha()
        elif noti_type == Noti.DETECT_PIT:
            text = self.font.render("DETECT PIT !", True, (23, 127, 117))
            img = pygame.image.load(PIT_IMG).convert_alpha()
        elif noti_type == Noti.COLLECT_GOLD:
            text = self.font.render("COLLECT GOLD !: +1000", True, (23, 127, 117))
            img = pygame.image.load(CHEST_IMG).convert_alpha()
        elif noti_type == Noti.SHOOT_ARROW:
            text = self.font.render("SHOOT ARROW !: -100", True, (23, 127, 117))
            img = pygame.image.load(ARROW_RIGHT_IMG).convert_alpha()
        elif noti_type == Noti.PERCEIVE_BREEZE:
            text = self.font.render("PERCEIVE BREEZE !", True, (23, 127, 117))
            img = pygame.image.load(BREEZE_IMG).convert_alpha()
        elif noti_type == Noti.PERCEIVE_STENCH:
            text = self.font.render("PERCEIVE STENCH !", True, (23, 127, 117))
            img = pygame.image.load(STENCH_IMG).convert_alpha()
        elif noti_type == Noti.DETECT_WUMPUS:
            text = self.font.render("DETECT WUMPUS !", True, (23, 127, 117))
            img = pygame.image.load(WUMPUS_IMG).convert_alpha()
        elif noti_type == Noti.KILL_BY_PIT:
            text = self.font.render("KILLED BY PIT !", True, (217, 30, 24))
            img = pygame.image.load(PIT).convert_alpha()
        elif noti_type == Noti.CLIMB_OUT_OF_THE_CAVE:
            text = self.font.render("CLIMB OUT OF THE CAVE !", True, (23, 127, 117))
            img = pygame.image.load(STENCH_IMG).convert_alpha()
            
        # Show text Noti
        text_rect = text.get_rect()
        text_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 6,
            WINDOW_HEIGHT // 3.5,
        )
        self.screen.blit(text, text_rect)
        # Show image
        img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
        self.screen.blit(
            img,
            (
                WINDOW_WIDTH // 2 + CELL_SIZE * 5.5,
                WINDOW_HEIGHT // 3,
            ),
        )
        pygame.display.update()
        pygame.time.delay(1000)

    def sketch_success_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        background = pygame.image.load(SUCCESS_IMAGE).convert()
        background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(background, (0, 0))

        text = self.font_title.render("SUCCESSFUL!!!", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, 50)
        self.screen.blit(text, text_rect)

        score = self.agent.score
        text = self.font_score.render("Your score: " + str(score), True, (0, 0, 0))
        text_rect.center = (WINDOW_WIDTH // 2 + 80, 150)
        self.screen.blit(text, text_rect)

        pygame.display.update()
        pygame.time.delay(3000)
        self.state = "menu"

    def sketch_failed_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        background = pygame.image.load(FAILED_IMAGE).convert()
        background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(background, (0, 0))

        text = self.font_title.render("FAILED !!!", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, 50)
        self.screen.blit(text, text_rect)

        text = self.font.render("Try to solve again :(", True, (255, 255, 255))
        text_rect.center = (WINDOW_WIDTH // 2, 150)
        self.screen.blit(text, text_rect)

        pygame.display.update()
        pygame.time.delay(3000)
        self.state = "menu"
    
    def reset(self, map):
        self.map == None
        self.map_size = None
        self.agent = Agent()
        self.action_list = None
        self.current_step = 0
                
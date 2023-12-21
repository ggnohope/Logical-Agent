import random
import sys

import pygame

from agent import *
from const import *
from map import Map
from notfication import Notification
from buttons import *


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
        self.map_size = None

        self.state = "menu"

        self.agent = Agent()
        
        length_header = MAIN_BUTTON_LENGTH/3*2
        x_header = (CELL_SIZE*10 - 3*length_header) / 5
        posx_level = [x_header, 2*x_header+length_header, 3*x_header+2*length_header]
        posy = WINDOW_HEIGHT/10*9
        self.button_reset = Buttons(self, WHITE, posx_level[0], posy, length_header, MAIN_BUTTON_HEIGHT, 'Reset')
        self.button_step = Buttons(self, WHITE, posx_level[1], posy, length_header, MAIN_BUTTON_HEIGHT, 'Step')
        self.button_play = Buttons(self, WHITE, posx_level[2], posy, length_header, MAIN_BUTTON_HEIGHT, 'Play')
        
        x_map = WINDOW_WIDTH/2 + CELL_SIZE*3.2
        y_map = WINDOW_HEIGHT/10 
        posy_map = [WINDOW_HEIGHT/2.8 + y_map,WINDOW_HEIGHT/2.8 + y_map*2,WINDOW_HEIGHT/2.8 + y_map*3,WINDOW_HEIGHT/2.8 + y_map*4, WINDOW_HEIGHT/2.8 + y_map*5]
        self.map1 = Buttons(self, WHITE, x_map , posy_map[0], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 1')
        self.map2 = Buttons(self, WHITE, x_map , posy_map[1], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 2')
        self.map3 = Buttons(self, WHITE, x_map , posy_map[2], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 3')
        self.map4 = Buttons(self, WHITE, x_map , posy_map[3], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 4')
        self.map5 = Buttons(self, WHITE, x_map , posy_map[4], MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Map 5')
        
    def run(self):
        while True:
            if self.state == "menu":
                self.draw_main_screen()
            elif self.state == "running":
                self.test_ui()
            elif self.state == "success":
                self.draw_success_screen()
            elif self.state == "failed":
                self.draw_failed_screen()

    def draw_main_screen(self):
        self.draw_layout()
        
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.event_mouse_motion(event, pos)
            self.event_mouse_click(event, pos)

    def draw_running_screen(self, noti_type: Notification = None):
        # Draw filter
        pygame.draw.rect(self.screen, pygame.Color('White'), (CELL_SIZE*12, CELL_SIZE*2, WINDOW_WIDTH - CELL_SIZE*12, WINDOW_HEIGHT/4))

        # draw score and gold collected
        self.draw_score()
        self.draw_gold()
        
        self.map.draw(self.screen)
        
        # draw notification
        if noti_type:
            self.draw_notification(noti_type)

        pygame.display.update()

    def draw_notification(self, noti_type: Notification):
        if noti_type == Notification.KILL_WUMPUS:
            text = self.font.render("KILL WUMPUS !", True, (23, 127, 117))
            img = pygame.image.load(WUMPUS_IMG).convert_alpha()
        elif noti_type == Notification.DETECT_PIT:
            text = self.font.render("DETECT PIT !", True, (23, 127, 117))
            img = pygame.image.load(PIT_IMG).convert_alpha()
        elif noti_type == Notification.COLLECT_GOLD:
            text = self.font.render("COLLECT GOLD !: +1000", True, (23, 127, 117))
            img = pygame.image.load(CHEST_IMG).convert_alpha()
        elif noti_type == Notification.SHOOT_ARROW:
            text = self.font.render("SHOOT ARROW !: -100", True, (23, 127, 117))
            img = pygame.image.load(ARROW_RIGHT_IMG).convert_alpha()

        # Show text notification
        text_rect = text.get_rect()
        text_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 5,
            WINDOW_HEIGHT // 3.5,
        )
        self.screen.blit(text, text_rect)
        # Show image
        img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
        self.screen.blit(
            img,
            (
                WINDOW_WIDTH // 2 + CELL_SIZE * 4.5,
                WINDOW_HEIGHT // 3,
            ),
        )

        pygame.display.update()
        pygame.time.delay(500)

    def draw_success_screen(self):
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
        text_rect.center = (WINDOW_WIDTH // 2 + 70, 150)
        self.screen.blit(text, text_rect)

        pygame.display.update()
        pygame.time.delay(3000)
        self.state = "menu"

    def draw_failed_screen(self):
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
    

    def test_ui(self):
        self.agent.cell.visited = True
        self.draw_running_screen()
        
        # self.draw_layout()
        # pos = pygame.mouse.get_pos()
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     self.event_mouse_motion(event, pos)
        #     self.event_mouse_click(event, pos)

        if (
            (self.agent.direction == Direction.UP and self.agent.cell.y > 0)
            or (self.agent.direction == Direction.DOWN and self.agent.cell.y < 9)
            or (self.agent.direction == Direction.LEFT and self.agent.cell.x > 0)
            or (self.agent.direction == Direction.RIGHT and self.agent.cell.x < 9)
        ):
            arrow_cell = self.agent.shoot_arrow(self.map.grid_cells)
            self.draw_running_screen(Notification.SHOOT_ARROW)

        if "G" in self.agent.cell.type:
            self.draw_running_screen()
            self.draw_running_screen(Notification.COLLECT_GOLD)
            self.agent.collect_gold()

        direc = random.choice(list(Direction))
        if (
            (direc == Direction.UP and self.agent.cell.y > 0)
            or (direc == Direction.DOWN and self.agent.cell.y < 9)
            or (direc == Direction.LEFT and self.agent.cell.x > 0)
            or (direc == Direction.RIGHT and self.agent.cell.y < 9)
        ):
            if direc == Direction.UP:
                self.agent.turn_up()
                self.draw_running_screen()
                self.agent.move_forward(self.map.grid_cells)
            if direc == Direction.DOWN:
                self.agent.turn_down()
                self.draw_running_screen()
                self.agent.move_forward(self.map.grid_cells)
            if direc == Direction.LEFT:
                self.agent.turn_left()
                self.draw_running_screen()
                self.agent.move_forward(self.map.grid_cells)
            if direc == Direction.RIGHT:
                self.agent.turn_right()
                self.draw_running_screen()
                self.agent.move_forward(self.map.grid_cells)

        pygame.time.delay(500)

    def sketch_map_select(self):
        self.screen.fill(pygame.Color('White'))
        self.map1.draw_button(STEELBLUE)
        self.map2.draw_button(STEELBLUE)
        self.map3.draw_button(STEELBLUE)
        self.map4.draw_button(STEELBLUE)
        self.map5.draw_button(STEELBLUE)
        
    def sketch_footer_select(self):
        # self.screen.fill(pygame.Color('White'))
        self.button_reset.draw_button(STEELBLUE)
        self.button_step.draw_button(STEELBLUE)
        self.button_play.draw_button(STEELBLUE)
        
    def draw_button(self, sc, rect, button_color, text, text_color):
        # draw button
        pygame.draw.rect(sc, button_color, rect)
        # draw text inside button
        text_sc = self.font.render(text, True, text_color)
        text_rect = text_sc.get_rect()
        text_rect.center = rect.center
        self.screen.blit(text_sc, text_rect)
    
    def draw_title(self):
        text = self.font_title.render("Wumpus World", True, (23, 127, 117))
        text_rect = text.get_rect()
        text_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 5,
            WINDOW_HEIGHT // 12,
        )
        self.screen.blit(text, text_rect)
        
    def draw_layout(self):
        pygame.display.update()
        self.screen.fill(pygame.Color('White'))
        self.sketch_map_select()
        self.sketch_footer_select()
        self.draw_title()
        pygame.draw.line(self.screen, pygame.Color('Black'), (CELL_SIZE*10.5, 0), (CELL_SIZE*10.5, WINDOW_HEIGHT), 2)
        pygame.draw.line(self.screen, pygame.Color('Black'), (CELL_SIZE*10.5, 0), (CELL_SIZE*10.5, WINDOW_HEIGHT), 2)
    
    def draw_score(self):
        score = self.agent.score
        score_text = self.font_score.render(
            "YOUR SCORE: " + str(score), True, (0, 0, 0)
        )
        score_rect = score_text.get_rect()
        score_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 5,
            WINDOW_HEIGHT // 5,
        )
        self.screen.blit(score_text, score_rect)
        
    def draw_gold(self):
        gold = self.agent.gold
        gold_text = self.font.render("Gold collected: " + str(gold), True, (0, 0, 0))
        gold_rect = gold_text.get_rect()
        gold_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 5,
            WINDOW_HEIGHT // 4,
        )
        self.screen.blit(gold_text, gold_rect)
        
    def event_mouse_motion(self, event, pos):
        if event.type == pygame.MOUSEMOTION:
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
                else:
                    self.map1.colour, self.map2.colour, self.map3.colour, self.map4.colour, self.map5.colour, self.button_reset.colour,self.button_step.colour,self.button_play.colour = WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE
        
    def event_mouse_click(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
                if self.map1.isOver(pos):
                    self.map = Map(MAP_1)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                    self.state = "running"
                elif self.map2.isOver(pos):
                    self.map = Map(MAP_2)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                    self.state = "running"
                elif self.map3.isOver(pos):
                    self.map = Map(MAP_3)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                    self.state = "running"
                elif self.map4.isOver(pos):
                    self.map = Map(MAP_4)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                    self.state = "running"
                elif self.map5.isOver(pos):
                    self.map = Map(MAP_5)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                    self.state = "running"
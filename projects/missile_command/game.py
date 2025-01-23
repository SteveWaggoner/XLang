#!/usr/bin/python3.9

from object import Object
from bitmap import Window
from playsound import playsound
from c6502 import Byte

from game_levels import Game_Levels
from game_board import Game_Board, Game_Input

class UI(Object):

    def set_fields(self, level, score, game_over, debug):
        self.level = level
        self.score = score
        self.game_over = game_over
        self.debug = debug

    def render(self,win):
        self.add_text(Byte(60), Byte(20), str(self.debug))
        self.add_text(Byte(180), Byte(10), "level: "+str(self.level)+"   score:" + str(self.score))
        if self.game_over.get():
            self.add_text(Byte(180), Byte(100), "GAME OVER")




class Game:

    def __init__(self):

        self.board = Game_Board()
        self.input = Game_Input(self.board)

        self.board.on_load_level       = lambda: playsound("sounds/alert.mp3", False)
        self.board.on_launch_missile   = lambda: playsound("sounds/missile-fire.mp3", False)
        self.board.on_explode_enemy    = lambda: playsound("sounds/explosions.mp3", False)
        self.board.on_explode_friendly = lambda: playsound("sounds/city-blow-up.mp3", False)

        self.ui  = UI()
        self.win = Window() # create a window



    def game_input(self):

        if self.board.level_index == 0:
            self.game_user_input()
        else:
            self.game_auto_input()


    def game_user_input(self):

        pnt = self.win.checkMouse()
        if not pnt is None:
            self.input.launch_missile(int(pnt.x), int(pnt.y))

        key = self.win.checkKey()
        if key == "1":
            self.input.select_battery(0)
        if key == "2":
            self.input.select_battery(1)
        if key == "3":
            self.input.select_battery(2)

    def game_auto_input(self):
        self.input.play_move()



    def draw_items(self, collection):
        for game_obj in collection.items:
            if game_obj.active == True:
                if game_obj.actions:
                    game_obj.action_tick()
                    if game_obj.active == True: #if still active after action
                        game_obj.draw_to(self.win)
                else:
                    game_obj.draw_to(self.win)


    def game_draw(self):

        if self.board.clock.ticks % 8 == 0:
            self.win.draw_background()

        self.draw_items(self.board.land)
        self.draw_items(self.board.city)
        self.draw_items(self.board.battery)
        self.draw_items(self.board.missile)
        self.draw_items(self.board.bomb)
        self.draw_items(self.board.smartbomb)
        self.draw_items(self.board.mario)
        self.draw_items(self.board.plane)
        self.draw_items(self.board.alien)
        self.draw_items(self.board.explosion)

        self.ui.set_fields(level=self.board.level_index+1, score=self.board.score, game_over=self.board.game_over, debug=f"fps: {self.board.clock.fps:.4f}, extracities: {self.board.extra_cities}")
        self.ui.draw_to(self.win)

        self.win.flush()
        self.win.redraw()


    def run_game(self):

        self.board.load_level(0)
        while self.board.is_game_active():
            self.game_input()
            self.board.game_action()
            self.game_draw()



xgame = Game()
xgame.run_game()
xgame.win.getKey()


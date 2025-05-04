#!/usr/bin/python3.8

from game_board import Game_Board, Game_Input
from game_display import Display, Sound

import window_sdl2


class Game:

    def __init__(self):

        self.board = Game_Board()
        self.input = Game_Input(self.board)

        self.board.on_load_level       = lambda: Sound.play("load_level")
        self.board.on_launch_missile   = lambda: Sound.play("launch_missile")
        self.board.on_explode_enemy    = lambda: Sound.play("explode_enemy")
        self.board.on_explode_friendly = lambda: Sound.play("explode_friendly")

      #  self.board.on_load_level       = None
      #  self.board.on_launch_missile   = None
      #  self.board.on_explode_enemy    = None
      #  self.board.on_explode_friendly = None

        self.display = Display(window_sdl2.Window("Missile Command", mode="VGA"))


    def game_input(self):

        if self.board.level_index == 0:
            self.game_user_input()
        else:
            self.game_auto_input()


    def game_user_input(self):

        pnt = self.display.check_mouse()
        if pnt:
            self.input.launch_missile(pnt.x, pnt.y)

        key = self.display.check_key()
        if key == 49: #"1"
            self.input.select_battery(0)
        if key == 50: #"2"
            self.input.select_battery(1)
        if key == 51: #"3"
            self.input.select_battery(2)

    def game_auto_input(self):
        self.input.play_move()



    def draw_items(self, collection):
        for game_obj in collection.items:
            if game_obj.active == True:
                if game_obj.actions:
                    game_obj.action_tick()
                    if game_obj.active == True: #if still active after action
                        self.display.draw_obj(game_obj)
                else:
                    self.display.draw_obj(game_obj)


    def game_draw(self):

        self.display.start_draw()

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

        self.display.draw_score(self.board)

        self.display.finish_draw()


    def run_game(self):

        self.board.load_level(0)
        while self.board.is_game_active():
            self.game_input()
            self.board.game_action()
            self.game_draw()



xgame = Game()
xgame.run_game()
xgame.win.getKey()


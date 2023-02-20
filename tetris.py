from settings import *
import math
from tetrimino import Tetrimino
import pygame.freetype as ft

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_DIR)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02), 
                            text = "TETRIS", fgcolor = "white", 
                            size = TILE_SIZE * 1.65, bgcolor = "black")
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22), 
                            text = "Next", fgcolor = "orange", 
                            size = TILE_SIZE * 1.4, bgcolor = "black")
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67), 
                            text = "Score", fgcolor = "orange", 
                            size = TILE_SIZE * 1.4, bgcolor = "black")
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.8), 
                            text = f'{self.app.tetris.score}', fgcolor = "white", 
                            size = TILE_SIZE * 1.8)

class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field = self.get_field()
        self.tetrimino = Tetrimino(self)
        self.next = Tetrimino(self, current = False)
        self.speed_up = False
        self.score = 0
        self.get_full_lines = 0
        self.points_per_line = {0 : 0, 1 : 40, 2 : 100, 3 : 300, 4 : 1200}

    def get_score(self):
        self.score += self.points_per_line[self.get_full_lines]
        self.get_full_lines = 0

    def full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H -1, -1, -1):
            for x in range(FIELD_W):
                self.field[row][x] = self.field[y][x]

                if self.field[y][x]:
                    self.field[row][x].pos = v(x, y)

            if sum(map(bool, self.field[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field[row][x].alive = False
                    self.field[row][x] = 0

                self.get_full_lines += 1

    def track_tetrimino(self):
        for block in self.tetrimino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field[y][x] = block

    def get_field(self):
        return [[0 for i in range(FIELD_W)] for j in range(FIELD_H)]

    def game_over(self):
        if self.tetrimino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True

    def check_land(self):
        if self.tetrimino.land:
            if self.game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.track_tetrimino()
                self.next.current = True
                self.tetrimino = self.next
                self.next = Tetrimino(self, current = False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetrimino.move(direction = 'left')
        elif pressed_key == pg.K_RIGHT:
            self.tetrimino.move(direction = 'right')
        elif pressed_key == pg.K_UP:
            self.tetrimino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

        
    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.full_lines()
            self.tetrimino.update()
            self.check_land()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)
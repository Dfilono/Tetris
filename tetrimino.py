from settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetrimino, pos):
        self.tetrimino = tetrimino
        self.pos = v(pos) + INIT_POS_OFFSET
        self.next_pos = v(pos) + NEXT_POS_OFFSET
        self.alive = True

        super().__init__(tetrimino.tetris.sprite_group)
        self.image = tetrimino.image
        #self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        #self.image.fill('orange', (1, 1, TILE_SIZE -2, TILE_SIZE - 2), border_radius = 8)
        self.rect = self.image.get_rect()
        
    def is_alive(self):
        if not self.alive:
            self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetrimino.current]
        self.rect.topleft = pos * TILE_SIZE

    def update(self):
        self.is_alive()
        self.rect_pos()

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        
        if 0 <= x < FIELD_W and y < FIELD_H and (y < 0 or not self.tetrimino.tetris.field[y][x]):
            return False
        return True

class Tetrimino:
    def __init__(self, tetris, current = True):
        self.tetris = tetris
        self.shape = random.choice(list(TETRIMINOES.keys()))
        self.image = random.choice(tetris.app.images)
        self.blocks = [Block(self, pos) for pos in TETRIMINOES[self.shape]]
        self.land = False
        self.current = current

    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_pos = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_pos):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_pos[i]

    def is_collide(self, block_pos):
        return any(map(Block.is_collide, self.blocks, block_pos))

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_pos = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_pos)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.land = True

    def update(self):
        self.move(direction = 'down')
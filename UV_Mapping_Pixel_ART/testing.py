import pygame as pg
from PIL import Image

vec = pg.Vector2
from settings import *


class Testing:
    def __init__(self, game, pos, image):
        self.game = game

        self.pos = vec(pos)
        self.vel = vec(0, 0)
        surf = pg.Surface((50, 50))
        surf.fill(YELLOW)
        self.image = surf
        self.rect = self.image.get_rect()
        pg.draw.rect(self.image, BLACK, self.rect, 1)
        self.speed = 300

        self.hit_rect = self.rect.copy()
        self.hit_rect.height = self.rect.height / 2
        self._layer = self.hit_rect.bottom
        self.dir_vec = vec(0, 0)
        self.rect.center = self.pos
        self.hit_rect.bottom = self.rect.bottom
        self.hit_rect.centerx = self.rect.centerx
        self.colors, self.mapping = self.create_UV_mapping(image)
        self.origin_width = image.get_width()
        self.origin_height = image.get_height()
        self.mapping_img = pg.Surface((image.get_width() * TILESIZE, image.get_height() * TILESIZE))
        self.result = pg.Surface((image.get_width() * TILESIZE, image.get_height() * TILESIZE))

    def get_keys(self):
        self.vel = vec(0, 0)
        # if not self.eat and self.game.cutscene_manager.cut_scene==None and self.game.current_character==self.name:
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -self.speed
            self.dir_vec = vec(-1, 0)
        if keys[pg.K_RIGHT]:
            self.vel.x = self.speed
            self.dir_vec = vec(1, 0)
        if keys[pg.K_UP]:
            self.vel.y = -self.speed
            self.dir_vec = vec(0, -1)
        if keys[pg.K_DOWN]:
            self.vel.y = self.speed
            self.dir_vec = vec(0, 1)

    def surf_to_image(self, image):
        raw_str = pg.image.tostring(image, "RGBA", False)
        img = Image.frombytes("RGBA", image.get_size(), raw_str)
        return img

    def create_UV_mapping(self, surf):
        im = self.surf_to_image(surf)
        pixels = list(im.getdata())
        width, height = im.size
        colors = [[pixels[i + j * width] for i in range(width)] for j in range(height)]
        mapping = [[(i, j, 0) for i in range(width)] for j in range(height)]
        return colors, mapping

    def update(self):
        # creating images

        # mapping
        for i in range(self.origin_width):
            for j in range(self.origin_height):
                pg.draw.rect(self.mapping_img, self.mapping[i][j], (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))

        # result of mapping
        for i in range(self.origin_width):
            for j in range(self.origin_height):
                pg.draw.rect(self.result, self.colors[self.mapping[i][j][0]][self.mapping[i][j][1]],
                             (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))

        self.get_keys()

        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.hit_rect.bottom = self.rect.bottom
        self.hit_rect.centerx = self.rect.centerx

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def draw_mapping(self, surf):
        surf.blit(self.mapping_img, self.rect)

    def draw_mapping_result(self, surf):
        surf.blit(self.result, self.rect)

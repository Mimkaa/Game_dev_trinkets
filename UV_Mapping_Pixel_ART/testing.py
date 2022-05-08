import pygame as pg
from PIL import Image

vec = pg.Vector2
from settings import *


class Testing:
    def __init__(self, game, pos, image_origin, image_to_map):
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

        self.image_to_map = image_to_map
        self.colors, self.mapping = self.create_UV_mapping(image_origin, image_to_map)
        self.image_width = image_to_map.get_width()
        self.image_height = image_to_map.get_height()
        self.mapping_img = pg.Surface((image_to_map.get_width() * TILESIZE, image_to_map.get_height() * TILESIZE),pg.SRCALPHA)
        self.result = pg.Surface((image_to_map.get_width() * TILESIZE, image_to_map.get_height() * TILESIZE),pg.SRCALPHA)

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

    def create_UV_mapping(self, or_surf, frame):
        im_or = self.surf_to_image(or_surf)
        pixels_or = list(im_or.getdata())

        im_frame = self.surf_to_image(frame)
        pixels_frame = list(im_frame.getdata())

        width_or, height_or = im_or.size
        colors_origin = [[pixels_or[i + j * width_or] for i in range(width_or)] for j in range(height_or)]
        mapping_1d = [(0, 0, 0, 0)] * len(pixels_frame)

        for n, p in enumerate(pixels_frame):
            for m, p_o in enumerate(pixels_or):
                x = m % width_or
                y = m // width_or
                if p == p_o:
                    # I had to switch them because they somehow are getting switched during the iteration
                    mapping_1d[n] = (y, x, 0, 255)


        width_frame, height_frame = im_frame.size
        mapping_2d = [[mapping_1d[i + j * width_frame] for i in range(width_frame)] for j in range(height_frame)]
        # width, height = im_or.size

        # mapping = [[(i, j, 0) for i in range(width)] for j in range(height)]
        return colors_origin, mapping_2d

    def update(self):
        # creating images

        # mapping
        for i in range(self.image_width):
            for j in range(self.image_height):
                pg.draw.rect(self.mapping_img, self.mapping[i][j], (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))

        # result of mapping
        for i in range(self.image_width):
            for j in range(self.image_height):
                color=self.colors[self.mapping[i][j][0]][self.mapping[i][j][1]]
                if self.mapping[i][j][3]>0:
                    pg.draw.rect(self.result, color,
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

import pygame as pg
import sys
from settings import *
from os import path
from testing import Testing


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.font = path.join("PixelatedRegular-aLKm.ttf")
        self.lookup = pg.image.load(path.join("lookup.png")).convert_alpha()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()

        self.surfaces = [pg.Surface((WIDTH // 3 - 10, HEIGHT)) for i in range(3)]
        for s in self.surfaces:
            s.fill(LIGHTGREY)
        lookup = pg.transform.scale(self.lookup,
                                    (self.lookup.get_width() * TILESIZE, self.lookup.get_height() * TILESIZE))
        self.surfaces[0].blit(lookup, (self.surfaces[0].get_width() / 2 - lookup.get_width() / 2,
                                       self.surfaces[0].get_height() / 2 - lookup.get_height() / 2))

        self.agent = Testing(self, (self.surfaces[0].get_width() // 2, self.surfaces[0].get_height() // 2), self.lookup)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.agent.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        txts = ["lookup", "mapping", "result"]
        for n, surf in enumerate(self.surfaces):
            self.screen.blit(surf, (WIDTH // 3 * n, 0))
            self.draw_text(txts[n], self.font, 40, WHITE,
                           self.surfaces[n].get_width() * n + self.surfaces[n].get_width() / 2, 50, align="center")
            if n == 1:
                self.surfaces[n].fill(LIGHTGREY)
                self.agent.draw_mapping(self.surfaces[n])
            elif n == 2:
                self.surfaces[n].fill(LIGHTGREY)
                self.agent.draw_mapping_result(self.surfaces[n])
        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


# create the game object
g = Game()
g.new()
g.run()

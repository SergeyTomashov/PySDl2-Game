import sys
import sdl2.ext
from random import randint
sdl2.ext.init()

WHITE = sdl2.ext.Color(255, 255, 255)
ORANGE = sdl2.ext.Color(255, 165, 0)


class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0


class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(128, 128, 128))
        super(SoftwareRenderer, self).render(components)


class Entity(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()


class DrawLines(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx, posy):
        self.sprite = sprite
        self.sprite.position = posx, posy


def run():
    window = sdl2.ext.Window("PySDL2 Game", size=(800, 800))
    window.show()

    spriterenderer = SoftwareRenderer(window)
    movement = MovementSystem(0, 0, 800, 800)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    sp_paddle = factory.from_color(WHITE, size=(38, 38))

    maze1 = [[10, 400, 20, 0], [10, 370, 20, 440], [200, 10, 20, 0]]
    maze2 = [[10, 400, 20, 0], [10, 370, 20, 440], [200, 10, 20, 0]]
    random = randint(1, 3)
    maze = maze1
    if random == 2:
        maze = maze2
    world = sdl2.ext.World()
    world.add_system(spriterenderer)
    world.add_system(movement)
    for line in maze:
        line1 = factory.from_color(ORANGE, size=(line[0], line[1]))
        line_ = DrawLines(world, line1, line[2], line[3])

    player = Entity(world, sp_paddle, 0, 390)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_w:
                    player.velocity.vy = -3
                if event.key.keysym.sym == sdl2.SDLK_s:
                    player.velocity.vy = 3
                if event.key.keysym.sym == sdl2.SDLK_a:
                    player.velocity.vx = -3
                if event.key.keysym.sym == sdl2.SDLK_d:
                    player.velocity.vx = 3
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.SDLK_w, sdl2.SDLK_s):
                    player.velocity.vy = 0
                elif event.key.keysym.sym in (sdl2.SDLK_a, sdl2.SDLK_d):
                    player.velocity.vx = 0
        sdl2.SDL_Delay(10)
        world.process()


if __name__ == "__main__":
    sys.exit(run())



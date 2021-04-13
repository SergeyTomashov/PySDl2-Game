import sys
import maze
import sdl2.ext
sdl2.ext.init()

WHITE = sdl2.ext.Color(255, 255, 255)
GREY = sdl2.ext.Color(165, 165, 165)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLACK = sdl2.ext.Color(0, 0, 0)


class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Speed, sdl2.ext.Sprite
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


class Speed(object):
    def __init__(self):
        super(Speed, self).__init__()
        self.vx = 0
        self.vy = 0


class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(255, 255, 255))
        super(SoftwareRenderer, self).render(components)


class Entity(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.speed = Speed()


class DrawLines(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx, posy):
        self.sprite = sprite
        self.sprite.position = posx, posy


def run():
    window = sdl2.ext.Window("Maze", size=(800, 800))
    window.show()

    spriterenderer = SoftwareRenderer(window)
    movement = MovementSystem(70, 70, 730, 730)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    sp_paddle = factory.from_color(BLACK, size=(24, 24))
    start = factory.from_color(GREEN, size=(57, 57))
    finish = factory.from_color(RED, size=(57, 57))

    maze_ = maze.RandomMaze()
    world = sdl2.ext.World()
    world.add_system(spriterenderer)
    world.add_system(movement)

    bg = factory.from_color(GREY, size=(680, 680))
    bg_ = DrawLines(world, bg, 60, 60)

    for line in maze_:
        line1 = factory.from_color(WHITE, size=(line[2], line[3]))
        line_ = DrawLines(world, line1, line[0], line[1])

    start_ = DrawLines(world, start, 70, 70)
    finish_ = DrawLines(world, finish, 673, 673)
    player = Entity(world, sp_paddle, 86, 86)
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_w:
                    player.speed.vy = -1
                if event.key.keysym.sym == sdl2.SDLK_s:
                    player.speed.vy = 1
                if event.key.keysym.sym == sdl2.SDLK_a:
                    player.speed.vx = -1
                if event.key.keysym.sym == sdl2.SDLK_d:
                    player.speed.vx = 1
            else:
                if event.key.keysym.sym in (sdl2.SDLK_w, sdl2.SDLK_s):
                    player.speed.vy = 0
                elif event.key.keysym.sym in (sdl2.SDLK_a, sdl2.SDLK_d):
                    player.speed.vx = 0
        sdl2.SDL_Delay(10)
        world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())



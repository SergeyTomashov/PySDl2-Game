import sys
from sdl2 import SDL_RenderDrawPoint
import maze
import sdl2.ext
sdl2.ext.init()

WHITE = sdl2.ext.Color(255, 255, 255)
GREY = sdl2.ext.Color(165, 165, 165)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLACK = sdl2.ext.Color(0, 0, 0)


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


class DrawLines(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx, posy):
        self.sprite = sprite
        self.sprite.position = posx, posy


def run():
    window = sdl2.ext.Window("Maze", size=(800, 800))
    window.show()

    spriterenderer = SoftwareRenderer(window)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp_paddle = factory.from_color(BLACK, size=(25, 25))
    start = factory.from_color(GREEN, size=(57, 57))
    finish = factory.from_color(RED, size=(57, 57))

    maze_ = maze.RandomMaze()
    world = sdl2.ext.World()
    world.add_system(spriterenderer)

    bg = factory.from_color(GREY, size=(680, 680))
    bg_ = DrawLines(world, bg, 60, 60)
    borders = [[] for i in range(58)]
    i = 0
    for line in maze_:
        line1 = factory.from_color(WHITE, size=(line[2], line[3]))
        line_ = DrawLines(world, line1, line[0], line[1])
        for j in range(4):
            borders[i].append(int(line_.sprite.area[j]))
        i += 1
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
                left, top, right, bottom = player.sprite.area
                if event.key.keysym.sym == sdl2.SDLK_w or event.key.keysym.sym == sdl2.SDLK_s:
                    for each in borders:
                        if each[0] < int(left) and each[2] > int(right) and each[1] < int(top) and each[3] > int(bottom):
                            coll_area = each
                            break
                    speed = 6
                    if top - coll_area[1] < 6:
                        speed = top - coll_area[1] - 1
                    if top - speed - 1 >= coll_area[1] and event.key.keysym.sym == sdl2.SDLK_w:
                        player = Entity(world, sp_paddle, left, top - speed)
                    else:
                        player = Entity(world, sp_paddle, left, top)
                if event.key.keysym.sym == sdl2.SDLK_s:
                    for each in borders:
                        if each[0] < int(left) and each[2] > int(right) and each[1] < int(top) and each[3] > int(bottom):
                            coll_area = each
                            break
                    speed = 6
                    if coll_area[3] - bottom < 6:
                        speed = coll_area[3] - bottom - 1
                    if bottom + speed + 1 <= coll_area[3] and event.key.keysym.sym == sdl2.SDLK_s:
                        player = Entity(world, sp_paddle, left, top + speed)
                    else:
                        player = Entity(world, sp_paddle, left, top)
                if event.key.keysym.sym == sdl2.SDLK_a:
                    for each in borders:
                        if each[0] < int(left) and each[2] > int(right) and each[1] < int(top) and each[3] > int(bottom):
                            coll_area = each
                    speed = 6
                    if left - coll_area[0] < 6:
                        speed = left - coll_area[0] - 1
                    if left - speed - 1 >= coll_area[0] and event.key.keysym.sym == sdl2.SDLK_a:
                        player = Entity(world, sp_paddle, left - speed, top)
                    else:
                        player = Entity(world, sp_paddle, left, top)
                if event.key.keysym.sym == sdl2.SDLK_d:
                    for each in borders:
                        if each[0] < int(left) and each[2] > int(right) and each[1] < int(top) and each[3] > int(bottom):
                            coll_area = each
                    speed = 6
                    if coll_area[2] - right < 6:
                        speed = coll_area[2] - right - 1
                    if right + speed + 1 <= coll_area[2] and event.key.keysym.sym == sdl2.SDLK_d:
                        player = Entity(world, sp_paddle, left + speed, top)
                    else:
                        player = Entity(world, sp_paddle, left, top)
        sdl2.SDL_Delay(1)
        world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())



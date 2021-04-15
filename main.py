import sys
import maze
import sdl2.ext
sdl2.ext.init()
import ctypes

WHITE = sdl2.ext.Color(255, 255, 255)

YANTARNIJ = sdl2.ext.Color(245,230,191)
GOLD = sdl2.ext.Color(245,218,42)

RED = sdl2.ext.Color(244,83,41)

SALAT = sdl2.ext.Color(190,245,116)
SHARTREZ = sdl2.ext.Color(127, 255, 0)
EZ_GREEN = sdl2.ext.Color(154,244,102)
DARK_EMERALD = sdl2.ext.Color(38, 153, 128)

DARK_GREY = sdl2.ext.Color(80, 80, 80)
EX_BLACK = sdl2.ext.Color(35, 35, 35)
BLACK = sdl2.ext.Color(0, 0, 0)
BROWN = sdl2.ext.Color(143,71,36)


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

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    spriterendrer = SoftwareRenderer(window)

    sp_paddle = factory.from_color(YANTARNIJ, size=(25, 25))
    shadow = factory.from_color(BLACK, size=(25, 25))
    start = factory.from_color(GOLD, size=(57, 57))
    finish = factory.from_color(RED, size=(57, 57))

    maze_ = maze.RandomMaze()
    world = sdl2.ext.World()
    world.add_system(spriterendrer)
    bg = factory.from_color(BROWN, size=(680, 680))
    bg_ = DrawLines(world, bg, 60, 60)

    running = True
    level_selection = False
    skin_selection = False
    first_maze = False
    second_maze = False
    main_menu = True
    draw = True

    spawx = 86
    spawy = 86
    sspawnx = 84
    sspawny = 88
    while running:
        if main_menu:
            x, y = ctypes.c_int(0), ctypes.c_int(0)
            if draw:
                skin_button = factory.from_color(EX_BLACK, size=(200, 80))
                level_selection_button = factory.from_color(EX_BLACK, size=(200, 80))
                skin_button_ = DrawLines(world, skin_button, 150, 600)
                level_selection_button_ = DrawLines(world, level_selection_button, 450, 600)
                draw = False
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
                if event.type == sdl2.SDL_MOUSEBUTTONUP:
                    state = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
                    if 150 <= x.value <= 350 and 600 <= y.value <= 680:
                        level_selection = True
                        first_maze = True
                        main_menu = False
                        draw = True
            window.refresh()
        elif first_maze:
            shadow_ = Entity(world, shadow, sspawnx, sspawny)
            player = Entity(world, sp_paddle, spawx, spawy)
            if draw:
                borders = [[] for i in range(58)]
                i = 0
                for line in maze_:
                    line1 = factory.from_color(SALAT, size=(line[2], line[3]))
                    line_ = DrawLines(world, line1, line[0], line[1])
                    for j in range(4):
                        borders[i].append(int(line_.sprite.area[j]))
                    i += 1
                start_ = DrawLines(world, start, 70, 70)
                finish_ = DrawLines(world, finish, 673, 673)
                draw = False
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
                            spawx = left
                            spawy = top - speed
                            sspawnx = left - 2
                            sspawny = top - speed + 2
                    if event.key.keysym.sym == sdl2.SDLK_s:
                        for each in borders:
                            if each[0] < int(left) and each[2] > int(right) and each[1] < int(top) and each[3] > int(bottom):
                                coll_area = each
                                break
                        speed = 6
                        if coll_area[3] - bottom < 6:
                            speed = coll_area[3] - bottom - 1
                        if bottom + speed + 1 <= coll_area[3] and event.key.keysym.sym == sdl2.SDLK_s:
                            spawx = left
                            spawy = top + speed
                            sspawnx = left - 2
                            sspawny = top + speed + 2
                    if event.key.keysym.sym == sdl2.SDLK_a:
                        for each in borders:
                            if each[0] < int(left) and each[2] > int(right) and each[1] < int(top) and each[3] > int(bottom):
                                coll_area = each
                        speed = 6
                        if left - coll_area[0] < 6:
                            speed = left - coll_area[0] - 1
                        if left - speed - 1 >= coll_area[0] and event.key.keysym.sym == sdl2.SDLK_a:
                            spawx = left - speed
                            spawy = top
                            sspawnx = left - 2 - speed
                            sspawny = top + 2
                    if event.key.keysym.sym == sdl2.SDLK_d:
                        for each in borders:
                            if each[0] < int(left) and each[2] > int(right) and each[1] < int(top) and each[3] > int(bottom):
                                coll_area = each
                        speed = 6
                        if coll_area[2] - right < 6:
                            speed = coll_area[2] - right - 1
                        if right + speed + 1 <= coll_area[2] and event.key.keysym.sym == sdl2.SDLK_d:
                            spawx = left + speed
                            spawy = top
                            sspawnx = left - 2 + speed
                            sspawny = top + 2
                window.refresh()
        sdl2.SDL_Delay(1)
        world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())



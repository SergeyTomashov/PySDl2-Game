from random import randint


def RandomMaze():
    random = randint(1, 2)
    maze1 = [[70, 70, 57, 258], [70, 338, 57, 191], [70, 539, 57, 191], [137, 70, 57, 124], [204, 70, 57, 124],
             [271, 70, 57, 191], [137, 271, 57, 124], [137, 405, 57, 191], [137, 606, 57, 124], [204, 204, 57, 124],
             [204, 338, 57, 191], [271, 472, 57, 191], [338, 137, 57, 124], [338, 338, 57, 124], [338, 472, 57, 191],
             [405, 271, 57, 191], [405, 606, 57, 124], [472, 70, 57, 124], [472, 204, 57, 191], [472, 405, 57, 191],
             [472, 606, 57, 124], [539, 204, 57, 124], [539, 338, 57, 191], [539, 539, 57, 191], [606, 137, 57, 191],
             [606, 338, 57, 191], [606, 606, 57, 124], [673, 70, 57, 325], [673, 405, 57, 325], [70, 70, 124, 57],
             [204, 70, 258, 57], [472, 70, 258, 57], [137, 137, 124, 57], [338, 137, 191, 57], [539, 137, 124, 57],
             [70, 204, 191, 57], [271, 204, 191, 57], [472, 204, 124, 57], [70, 271, 124, 57], [204, 271, 258, 57],
             [539, 271, 124, 57], [70, 338, 124, 57], [204, 338, 191, 57], [472, 338, 124, 57], [606, 338, 124, 57],
             [271, 405, 191, 57], [70, 472, 124, 57], [204, 472, 124, 57], [338, 472, 191, 57], [539, 472, 124, 57],
             [70, 539, 191, 57], [338, 539, 124, 57], [472, 539, 258, 57], [137, 606, 191, 57], [405, 606, 124, 57],
             [606, 606, 124, 57], [137, 673, 325, 57], [472, 673, 124, 57]]
    maze2 = [[]]
    maze = maze1
    if random == 2:
        maze = maze2
    return maze1
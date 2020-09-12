import pygame
import math

from pygame.locals import (
    K_SPACE,
    K_LEFT,
    K_RIGHT,
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    USEREVENT
)

SCREEN_WIDTH = 870
SCREEN_HEIGHT = 800

BLACK = (0, 0, 0)
CLEAR = (255, 255, 255, 0)

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent's constructor
        super().__init__()
        self.pWidth = 50
        self.pHeight = 40
        self.image = pygame.image.load("ship.png")
        self.surf = pygame.Surface((self.pWidth, self.pHeight))
        # Get the dimensions of the image
        self.rect = self.image.get_rect()
        # set start position of the the ship
        self.rect.x = SCREEN_WIDTH//2
        self.rect.y = math.floor(SCREEN_HEIGHT*.90)

    def update(self):
        global pressed_keys
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


"""
class CreatePlayer:
    def __init__(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
"""


class Enemy(pygame.sprite.Sprite):
    def __init__(self, version):
        """Instantiate the correct alien type, set its values and create an index to be
        used when updating the image"""
        super().__init__()

        self.version = version
        if self.version == 1:
            """Top enemy"""
            self.images = []
            self.images.append(pygame.transform.scale(pygame.image.load("enemy1_1.png"), (40, 40)))
            self.images.append(pygame.transform.scale(pygame.image.load("enemy1_2.png"), (40, 40)))
            self.rect = pygame.Rect(0, 0, 40, 40)
        elif self.version == 2:
            """Middle enemy"""
            self.images = []
            self.images.append(pygame.transform.scale(pygame.image.load("enemy2_1.png"), (50, 50)))
            self.images.append(pygame.transform.scale(pygame.image.load("enemy2_2.png"), (50, 50)))
            self.rect = pygame.Rect(0, 0, 50, 50)
        elif self.version == 3:
            """Bottom enemy"""
            self.images = []
            self.images.append(pygame.transform.scale(pygame.image.load("enemy3_1.png"), (50, 50)))
            self.images.append(pygame.transform.scale(pygame.image.load("enemy3_2.png"), (50, 50)))
            self.rect = pygame.Rect(0, 0, 50, 50)
        else:
            print("Input is not one of the enemies")
            return
        self.index = 0
        self.image = self.images[self.index]
        # print("ADDED")
        # alive will be used to determine if an alien should exist on the board
        self.alive = True

    def update(self):
        """switches between images of the sprite. Uses a timer to slow down the switched"""
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def is_alive(self):
        """Tells if the alien is alive or destroyed"""
        return self.alive

    def hit(self):
        print('hit')
        pass


class CreateAlienGrid(object):
    def __init__(self):
        self.enemies = pygame.sprite.Group()

        self.margin = 5
        self.width = 50
        self.height = 50
        self.grid = []
        # 2 dimensional array
        # put an enemy in every spot on the grid
        self.rows = 0
        self.row = 0
        self.column = 0
        for self.row in range(1):
            self.grid.append([])
            self.rows += 1
            for self.column in range(11):
                self.grid[self.row].append(Enemy(1))

        for self.row in range(2):
            self.grid.append([])
            self.rows += 1
            for self.column in range(11):
                self.grid[self.row+1].append(Enemy(2))

        for self.row in range(2):
            self.grid.append([])
            self.rows += 1
            for self.column in range(11):
                self.grid[self.row+3].append(Enemy(3))

        # Add sprites that were put into the grid into a group
        for self.row in range(5):
            for self.column in range(11):
                self.enemies.add(self.grid[self.row][self.column])

        # value for space between sprites
        self.margin = 10
        # value for moving the whole grid
        self.yOffset = 0
        self.xOffset = 0
        # value for determining the move direction
        self.lm = 'r'
        self.maxCol = 0
        self.arrayWidth = 0

        # DEBUGGING
        # print(rows)
        # print(self.enemies)

    def enemy_collide(self, projectile):
        for self.row in range(5):
            for self.column in range(11):
                if projectile.colliderect(self.grid[self.row][self.column].rect):
                    self.grid[self.row][self.column].alive = False
                    #print(self.grid[self.row][self.column].alive)
                    # incrememnt the score here

    def draw_grid(self):
        """
        FIXME I need to figure out how to put one of enemies into the grid and then
        determine if the enemy is alive and put it in that grid spot if it exists
        """
        for row in range(5):
            for column in range(11):
                # check if the enemy should be there
                # print(self.grid[row][column])
                if self.grid[row][column].alive:
                    # this if statement deals with the 5 extra pixels needed for the top level of sprites
                    if self.grid[row][column].version == 1:
                        SCREEN.blit(self.grid[row][column].image,
                                    ((self.margin + 50) * column + self.margin + self.xOffset + 5,
                                     (self.margin + 50) * row + self.margin + self.yOffset)
                                    )
                    else:
                        SCREEN.blit(self.grid[row][column].image,
                                    ((self.margin + 50) * column + self.margin + self.xOffset,
                                     (self.margin + 50) * row + self.margin + self.yOffset)
                                    )
                else:
                    pass
                    """
                    pygame.draw.rect(SCREEN,
                                     pygame.Surface((50, 50)).fill(CLEAR),
                                     ((self.margin + 50) * column + self.margin + self.xOffset,
                                      (self.margin + 50) * row + self.margin + self.yOffset, 50, 50)
                                     )
                    """

    def move_grid(self):
        """ Move the grid every second based on where it is
        SUDO:
        lm = r          # lm is last move and the values are:
                        # r = last move was right
                        # l = last move was left
                        # dr = last move was down on the right side
                        # dl = last move was down on the left side
        if far right is touching the right edge of the screen
            move down
            lm = l
        elif far left is touching the left edge of the screen
            move down
            lm = r
        elif lm == r
            move right
        elif lm == l
            move left

        The move should send an offset to the draw method which will place
        the array is the correct spot
        xOffset should add 20 if moving right and subtract 20 if moving right
        yOffset should add 50 everytime it is called

        You know the grid reaches the right depending on if any aliens exist
        at the far right column of the grid, if not the the second to the
        far right
        Go through the 2-di array and find the max number of columns,
        once the max is found mult by a constant that represents the width of each column
        if the self.xOffset + the determined width is >= SCREEN_WIDTH
        the move it down
        """
        self.maxCol = 0
        for row in range(5):
            for column in range(11):
                if self.grid[row][column].alive:
                    if column > self.maxCol:
                        self.maxCol = column
        self.maxCol = self.maxCol + 1

        self.arrayWidth = (self.margin + 50) * self.maxCol + self.margin

        if self.lm == 'r' and self.xOffset + self.arrayWidth >= SCREEN_WIDTH:
            self.yOffset += 50
            self.lm = 'l'
        elif self.lm == 'l' and self.xOffset <= 0:
            self.yOffset += 50
            self.lm = 'r'
        elif self.lm == 'r':
            self.xOffset += 30
        elif self.lm == 'l':
            self.xOffset -= 30


class PMissile(object):
    def __init__(self):
        self.image = pygame.image.load("laser.png")
        self.vel = -8
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 25 - 2
        self.rect.y = player.rect.y

    def draw(self):
        SCREEN.blit(self.image, self.rect)
        # print("Draw")

    def update(self):
        global pMissiles
        if self.rect.y > 0:
            self.rect.move_ip(0, self.vel)
            # print("moving")
        else:
            pMissiles.clear()
            # print("clear")
        # print("update")


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

bg = pygame.image.load("bg.jpg")

clock = pygame.time.Clock()
# set timer for switching alien images
pygame.time.set_timer(USEREVENT+1, 500)

# Instantiate player
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Build the grid structure
grid = CreateAlienGrid()


def redraw_game_window():
    # cover previous movement so the player and everything else appears to be moving
    SCREEN.blit(bg, (0, 0))

    # display the player
    for entity in all_sprites:
        SCREEN.blit(entity.image, entity.rect)

    for missile in pMissiles:
        missile.draw()

    grid.draw_grid()
    pygame.display.flip()


running = True
pMissiles = []
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                if len(pMissiles) < 1:
                    pMissiles.append(PMissile())
        elif event.type == QUIT:
            running = False
        elif event.type == USEREVENT+1:
            for enemy in grid.enemies:
                enemy.update()
            grid.move_grid()
    # print(len(pMissiles))
    # print(pMissiles)

    # make the pressed keys move the player left or right
    pressed_keys = pygame.key.get_pressed()
    player.update()

# FIXME

    for missile in pMissiles:
        CreateAlienGrid.enemy_collide(grid, missile.rect)
        missile.update()

    redraw_game_window()

    clock.tick(60)

pygame.quit()

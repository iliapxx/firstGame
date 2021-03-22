import pygame, random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screenWidth = 3840
screenHeight = 2160
fullscreen = True

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('platformer1')

tile_size = 75

bg_img = pygame.image.load('img/bg1.png').convert()
bg = pygame.transform.scale(bg_img, (screenWidth, screenHeight))

scroll = [0, 0]

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.music.load('bgmusic.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.03)
grass_sounds = [pygame.mixer.Sound('grass1.wav'), pygame.mixer.Sound('grass2.wav')]
grass_sounds[0].set_volume(0.03)
grass_sounds[1].set_volume(0.02)
grass_sound_timer = 0

class Player:

    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 9):
            img_right = pygame.image.load(f'img/player{num}.png').convert_alpha()
            img_right = pygame.transform.scale(img_right, (tile_size, (tile_size * 2)))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.isJump = False
        self.direction = 0
        self.old_direction = 1
        self.ground = True
        self.standing_right = pygame.image.load('img/player0.png').convert_alpha()
        self.standing_left = pygame.transform.flip(self.standing_right, True, False)
        self.dx = 0
        self.dy = 0
        self.walk_cooldown = 3

    def key_left_pressed(self):
        return keys[pygame.K_a] or keys[pygame.K_LEFT]

    def key_right_pressed(self):
        return keys[pygame.K_d] or keys[pygame.K_RIGHT]

    def update_inputs(self):
        global grass_sound_timer

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.ground is True:
            self.vel_y = -18
            self.ground = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dx += 10
            self.counter += 1
            self.direction = 1
            self.old_direction = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dx -= 10
            self.counter += 1
            self.direction = -1
            self.old_direction = -1
        if keys[pygame.K_a] and self.ground is True:
            if grass_sound_timer == 0:
                grass_sound_timer = 18
                random.choice(grass_sounds).play()
        if keys[pygame.K_d] and self.ground is True:
            if grass_sound_timer == 0:
                grass_sound_timer = 18
                random.choice(grass_sounds).play()
        if not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.counter = 0
            self.index = 0
            if self.old_direction == 1:
                self.image = pygame.transform.scale(self.standing_right, (tile_size, (tile_size * 2)))
            if self.old_direction == -1:
                self.image = pygame.transform.scale(self.standing_left, (tile_size, (tile_size * 2)))
        if keys[pygame.K_a] and keys[pygame.K_d]:
            self.counter = 0
            self.index = 0
            if self.old_direction == 1:
                self.image = pygame.transform.scale(self.standing_right, (tile_size, (tile_size * 2)))
            if self.old_direction == -1:
                self.image = pygame.transform.scale(self.standing_left, (tile_size, (tile_size * 2)))
        if keys[pygame.K_1]:
            load_level(1)


    def update(self):
        self.dx = 0
        self.dy = 0

        self.update_inputs()

        if self.counter > self.walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index > 6:
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        self.vel_y += 1
        if self.vel_y > 20:
            self.vel_y = 20
        self.dy += self.vel_y

        for tile in world.tile_list:
            if world.tile != 5:
                if tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                    self.dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                    if self.vel_y < 0:
                        self.dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        self.dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.ground = True
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight
            self.dy = 0
        screen.blit(self.image, (self.rect.x + scroll[0], self.rect.y + scroll[1]))
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)

def drawGrid():
    for line in range(0, 16):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screenWidth, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screenHeight))


class World:
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('img/dirt.png').convert()
        grass_img = pygame.image.load('img/grass0.png').convert()
        stone_img = pygame.image.load('img/stone.png').convert()
        vines_img = pygame.image.load('img/vines.png').convert_alpha()
        back_img = pygame.image.load('img/backstonetest.png').convert()
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(vines_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 5:
                    img = pygame.transform.scale(back_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            tx = tile[1].x
            ty = tile[1].y
            screen.blit(tile[0], (tx + scroll[0], ty + scroll[1]))
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 1)


class MapData:
    def __init__(self, world_data, player_x, player_y):
        self.world_data = world_data
        self.player_x = player_x
        self.player_y = player_y


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data[1:]:
        game_map.append(list(map(int, row)))

    [player_x_str, player_y_str] = data[0].split(' ')

    return MapData(world_data=game_map, player_x=int(player_x_str), player_y=int(player_y_str))

def load_level(level):
    global world, world_data

    map_data = load_map(f'level{level}')
    world_data = map_data.world_data
    world = World(world_data)
    player.rect.x = map_data.player_x
    player.rect.y = map_data.player_y

player = Player(300, -1000)
load_level(0)

run = True
while run:

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    scroll[0] += (-player.rect.x - scroll[0] + (screenWidth / 2) - (player.rect.width / 2)) / 30
    scroll[1] += (-player.rect.y - scroll[1] + (screenHeight / 2) - (player.rect.height / 2)) / 30

    clock.tick(fps)

    screen.blit(bg, (0, 0))
    world.draw()
    player.update()
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_F4] and fullscreen is True:
    #     fullscreen = False
    # elif keys[pygame.K_F4] and fullscreen is False:
    #     fullscreen = True
    # if fullscreen is True:
    #     screenWidth = 3840
    #     screenHeight = 2160
    #     screen = pygame.display.set_mode((3840, 2160))
    # if fullscreen is False:
    #     screenWidth = 1920
    #     screenHeight = 1080
    #     screen = pygame.display.set_mode((1920, 1080))
    # drawGrid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()


# add sounds
# add water
# add caves
# add falling and looping back to the top
# add mining
# add better player sprites
# add full screen
# add more blocks
# make the array bigger
# randomly generating blocks?
# pseudo-infinite world
# running?

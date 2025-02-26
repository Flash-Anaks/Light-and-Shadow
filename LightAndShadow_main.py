import pygame
import pyganim

TILE_SIZE = 51

def load_image(name):
    return pygame.image.load(name).convert_alpha()

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((650, 650))
    pygame.display.set_caption("Light and Shadow")
    return screen

def load_resources():
    ShadowIdleAnimation = load_image("textures/Idel Animation 48x48.png")
    ShadowRunAnimation = load_image("textures/Run Animation 48x48.png")
    ShadowJumpAnimation = load_image("textures/Jump Animation 48x48.png")
    LightIdleAnimation = load_image("textures/LightIdleAnimation.png")
    LightJumpAnimation = load_image("textures/LightJumpAnimation.png")
    LightRunAnimation = load_image("textures/LightRunAnimation.png")
    wall_texture = pygame.image.load("textures/wall.png").convert_alpha()
    floor_texture = pygame.image.load("textures/floor.png").convert_alpha()
    corner_texture = pygame.image.load("textures/corner.png").convert_alpha()

    def create_animation(sheet, columns, rows, duration=100, flip_x=False):
        """Разрезает спрайт-лист и создаёт анимацию"""
        frames = []
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height() // rows
        for i in range(columns):
            frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            if flip_x:
                frame = pygame.transform.flip(frame, True, False)
            frames.append((frame, duration))
        return pyganim.PygAnimation(frames)

    shadow_sprites = {
        "idle": create_animation(ShadowIdleAnimation, 10, 1),
        "run_right": create_animation(ShadowRunAnimation, 8, 1),
        "run_left": create_animation(ShadowRunAnimation, 8, 1, flip_x=True),
        "jump_right": create_animation(ShadowJumpAnimation, 6, 1, duration=140),
        "jump_left": create_animation(ShadowJumpAnimation, 6, 1, duration=140, flip_x=True)
    }
    light_sprites = {
        "idle": create_animation(LightIdleAnimation, 4, 1),
        "run_right": create_animation(LightRunAnimation, 4, 1),
        "run_left": create_animation(LightRunAnimation, 4, 1, flip_x=True),
        "jump_right": create_animation(LightJumpAnimation, 4, 1, duration=140),
        "jump_left": create_animation(LightJumpAnimation, 4, 1, duration=140, flip_x=True)
    }

    # Запускаем анимации сразу, но будем переключать их в коде
    for anim in shadow_sprites.values():
            anim.play()

    for anim in light_sprites.values():
            anim.play()

    return {
        "shadow": shadow_sprites,
        "light": light_sprites,
        "wall": wall_texture,
        "floor": floor_texture,
        "corner": corner_texture
    }

def load_map(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

class Player:
    def __init__(self, x, y, animations, controls):
        self.animations = animations
        self.current_anim = animations["idle"]
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_force = -11
        self.move_speed = 3.5
        self.on_ground = False
        self.controls = controls

    def switch_animation(self, state):
        if self.current_anim != self.animations[state]:
            self.current_anim = self.animations[state]
            self.current_anim.play()

    def update(self, walls):
        prev_y = self.rect.y
        self.velocity_y += self.gravity

        self.rect.x += self.velocity_x
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.velocity_x > 0:
                    self.rect.right = wall.left
                elif self.velocity_x < 0:
                    self.rect.left = wall.right
                self.velocity_x = 0

        self.rect.y += self.velocity_y
        self.on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall):
                if prev_y + self.rect.height <= wall.y:
                    self.rect.bottom = wall.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif prev_y >= wall.bottom:
                    self.rect.top = wall.bottom
                    self.velocity_y = 0

    def draw(self, screen):
        self.current_anim.blit(screen, self.rect.center)

def game_loop(screen, resources, level_map):
    clock = pygame.time.Clock()
    FPS = 60
    walls = []
    players = []

    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            if tile == '/' or tile == '\\' or tile == '_' or tile == 'q' or tile == 'w' or tile == 'e' or tile == 'r' or tile == '-':
                walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == '@':
                players.append(Player(x * TILE_SIZE, y * TILE_SIZE, resources["shadow"],
                                      {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w}))
            elif tile == '*':
                players.append(Player(x * TILE_SIZE, y * TILE_SIZE, resources["light"],
                                      {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP}))


    running = True
    while running:
        screen.fill((60, 60, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        for player in players:
            if keys[player.controls["left"]]:
                player.velocity_x = -player.move_speed
                if not player.on_ground:
                    player.switch_animation("jump_left")
                else:
                    player.switch_animation("run_left")
            elif keys[player.controls["right"]]:
                player.velocity_x = player.move_speed
                if not player.on_ground:
                    player.switch_animation("jump_right")
                else:
                    player.switch_animation("run_right")
            elif not player.on_ground:
                player.switch_animation("jump_right")
            else:
                player.velocity_x = 0
                player.switch_animation("idle")

            if keys[player.controls["jump"]] and player.on_ground:
                player.velocity_y = player.jump_force

            player.update(walls)

        for y, row in enumerate(level_map):
            for x, tile in enumerate(row):
                if tile == '/':
                    screen.blit(resources["wall"], (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == '\\':
                    screen.blit(pygame.transform.flip(resources["wall"], True, False), (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == '_':
                    screen.blit(resources["floor"], (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 'e':
                    screen.blit(resources["corner"], (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 'r':
                    screen.blit(pygame.transform.flip(resources["corner"], True, False), (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 'w':
                    screen.blit(pygame.transform.flip(resources["corner"], True, True), (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 'q':
                    screen.blit(pygame.transform.flip(resources["corner"], False, True), (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == '-':
                    screen.blit(pygame.transform.flip(resources["floor"], False, True), (x * TILE_SIZE, y * TILE_SIZE))

        for player in players:
            player.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    screen = init_game()
    resources = load_resources()
    level_map = load_map("map.txt")
    game_loop(screen, resources, level_map)
    pygame.quit()

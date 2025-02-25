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
    idle_sheet = load_image("textures/Idel Animation 48x48.png")
    run_sheet = load_image("textures/Run Animation 48x48.png")
    jump_sheet = load_image("textures/Jump Animation 48x48.png")
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

    player_sprites = {
        "idle": create_animation(idle_sheet, 10, 1),
        "run_right": create_animation(run_sheet, 8, 1),
        "run_left": create_animation(run_sheet, 8, 1, flip_x=True),
        "jump_right": create_animation(jump_sheet, 6, 1, duration=140),
        "jump_left": create_animation(jump_sheet, 6, 1, duration=140, flip_x=True)
    }

    # Запускаем анимации сразу, но будем переключать их в коде
    for anim in player_sprites.values():
        anim.play()

    return {
        "player": player_sprites,
        "wall": wall_texture,
        "floor": floor_texture,
        "corner": corner_texture
    }

def load_map(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

class ShadowPlayer:
    def __init__(self, x, y, animations):
        self.animations = animations
        self.current_anim = animations["idle"]
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_force = -11
        self.move_speed = 3.5
        self.on_ground = False

    def switch_animation(self, state):
        """Переключает анимацию"""
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

        self.rect.y += self.velocity_y
        self.on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall):
                if prev_y + self.rect.height <= wall.y:
                    self.rect.y = wall.y - self.rect.height
                    self.velocity_y = 0
                    self.on_ground = True

    def draw(self, screen):
        self.current_anim.blit(screen, self.rect.center)

def game_loop(screen, resources, level_map):
    clock = pygame.time.Clock()
    FPS = 60
    walls = []
    #player = ShadowPlayer(48, 48, resources["player"])
    player = None

    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            if tile == '/' or tile == '\\' or tile == '_' or tile == 'q' or tile == 'w' or tile == 'e' or tile == 'r' or tile == '-':
                walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == '@':
                player = ShadowPlayer(x * TILE_SIZE, y * TILE_SIZE, resources["player"])
    running = True
    while running:
        screen.fill((60, 60, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.velocity_x = -player.move_speed
            if not player.on_ground:
                player.switch_animation("jump_left")
            else:
                player.switch_animation("run_left")
        elif keys[pygame.K_d]:
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

        if keys[pygame.K_w] and player.on_ground:
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


        player.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    screen = init_game()
    resources = load_resources()
    level_map = load_map("map.txt")
    game_loop(screen, resources, level_map)
    pygame.quit()

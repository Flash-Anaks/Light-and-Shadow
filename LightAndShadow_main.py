import pygame
import pyganim
import pytmx
import finalw
import time

TILE_SIZE = 16
ORIGINAL_TILE_SIZE = 8
SCALE_FACTOR = TILE_SIZE // ORIGINAL_TILE_SIZE
GRAVITY = 0.6
JUMP_FORCE = -12
MOVE_SPEED = 4

pygame.init()
screen = pygame.display.set_mode((1920, 1060))
pygame.display.set_caption("Light and Shadow")
clock = pygame.time.Clock()
FPS = 60


def load_image(name):
    return pygame.image.load(name).convert_alpha()


def create_animation(sheet, columns, rows, duration=100, flip_x=False):
    frames = []
    frame_width = sheet.get_width() // columns
    frame_height = sheet.get_height() // rows
    for row in range(rows):
        for col in range(columns):
            frame = sheet.subsurface(pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height))
            if flip_x:
                frame = pygame.transform.flip(frame, True, False)
            frames.append((frame, duration))
    return pyganim.PygAnimation(frames)


def load_resources():
    ShadowIdleAnimation = load_image("textures/Idel Animation 48x48.png")
    ShadowRunAnimation = load_image("textures/Run Animation 48x48.png")
    ShadowJumpAnimation = load_image("textures/Jump Animation 48x48.png")
    LightIdleAnimation = load_image("textures/LightIdleAnimation.png")
    LightJumpAnimation = load_image("textures/LightJumpAnimation.png")
    LightRunAnimation = load_image("textures/LightRunAnimation.png")

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
    for anim in shadow_sprites.values():
        anim.play()
    for anim in light_sprites.values():
        anim.play()
    return {"shadow": shadow_sprites, "light": light_sprites}


def load_map(filename):
    tmx_data = pytmx.load_pygame(filename)
    walls = []
    player_positions = {"player1": (0, 0), "player2": (0, 0)}
    map_width = tmx_data.width * TILE_SIZE
    map_height = tmx_data.height * TILE_SIZE

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup):
            for obj in layer:
                if obj.name in player_positions:
                    player_positions[obj.name] = (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR)
                else:
                    walls.append(pygame.Rect(obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR,
                                             obj.width * SCALE_FACTOR, obj.height * SCALE_FACTOR))

        elif isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                if gid != 1:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    walls.append(pygame.Rect(0, 0, map_width, TILE_SIZE))
    walls.append(pygame.Rect(0, 0, TILE_SIZE, map_height))
    return tmx_data, walls, player_positions



def draw_map(screen, tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    scaled_tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
                    screen.blit(scaled_tile, (x * TILE_SIZE, y * TILE_SIZE))

    # Отобразить стены для отладки
    # for wall in walls:
    #     pygame.draw.rect(screen, (255, 0, 0), wall, 2)


class Player:
    def __init__(self, x, y, animations, name):
        self.animations = animations
        self.current_anim = animations["idle"]
        self.rect = pygame.Rect(x, y, TILE_SIZE + 16, TILE_SIZE + 24)
        self.start_pos = (x, y)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.start_time = time.time()
        self.finished = True
        self.name = name

    def switch_animation(self, state):
        if self.current_anim != self.animations[state]:
            self.current_anim = self.animations[state]
            self.current_anim.play()

    def update(self, walls, tmx_data):
        self.velocity_y += GRAVITY
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
                if self.velocity_y > 0:
                    self.rect.bottom = wall.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = wall.bottom
                    self.velocity_y = 0

        if self.rect.bottom >= tmx_data.height * TILE_SIZE:
            self.rect.topleft = self.start_pos
            self.velocity_y = 0

        if self.rect.right >= tmx_data.width * TILE_SIZE:
            pygame.quit()
            self.finished = True
            elapsed_time = time.time() - self.start_time
            player_name = self.name
            finalw.fin_screen(player_name, elapsed_time)


    def draw(self, screen):
        self.current_anim.blit(screen, self.rect.topleft)

def draw_exit_button(screen):
    font = pygame.font.SysFont("Arial", 30)
    text_surface = font.render("Выход", True, (255, 255, 255))  # Белый текст
    button_rect = pygame.Rect(10, 10, text_surface.get_width() + 10, text_surface.get_height() + 10)  # Прямоугольник под текстом
    pygame.draw.rect(screen, (0, 0, 0), button_rect)  # Черный фон для кнопки
    screen.blit(text_surface, (button_rect.x + 5, button_rect.y + 5))  # Рисуем текст на кнопке
    return button_rect


def game_loop(screen, resources, tmx_data, walls, player_positions):
    player1 = Player(*player_positions["player1"], resources["shadow"], name="Shadow")
    player2 = Player(*player_positions["player2"], resources["light"], name="Light")
    running = True
    while running:
        screen.fill((50, 50, 50))
        draw_map(screen, tmx_data)
        player1.update(walls, tmx_data)
        player2.update(walls, tmx_data)
        player1.draw(screen)
        player2.draw(screen)

        exit_button_rect = draw_exit_button(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    running = False
        keys = pygame.key.get_pressed()
        player1.velocity_x = (-MOVE_SPEED if keys[pygame.K_a] else MOVE_SPEED if keys[pygame.K_d] else 0)
        player1.switch_animation("run_left" if keys[pygame.K_a] else "run_right" if keys[pygame.K_d] else "idle")
        if keys[pygame.K_w] and player1.on_ground:
            player1.velocity_y = JUMP_FORCE
        player2.velocity_x = (-MOVE_SPEED if keys[pygame.K_LEFT] else MOVE_SPEED if keys[pygame.K_RIGHT] else 0)
        player2.switch_animation("run_left" if keys[pygame.K_LEFT] else "run_right" if keys[pygame.K_RIGHT] else "idle")
        if keys[pygame.K_UP] and player2.on_ground:
            player2.velocity_y = JUMP_FORCE

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    resources = load_resources()
    tmx_data, walls, player_positions = load_map("map1.tmx")
    game_loop(screen, resources, tmx_data, walls, player_positions)

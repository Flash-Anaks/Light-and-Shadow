import pygame
import pyganim

TIMER = 60

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

    for anim in player_sprites.values():
        anim.play()

    platform_image = pygame.image.load("textures/texture_1.png").convert_alpha()
    return {
        "player": player_sprites,
        "platform": pygame.transform.scale(platform_image, (150, 150))
    }

class Player:
    def __init__(self, x, y, animations):
        self.animations = animations
        self.current_anim = animations["idle"]
        self.rect = pygame.Rect(x, y, 65, 80)
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

    def update(self, platforms):
        prev_y = self.rect.y
        self.velocity_y += self.gravity

        self.rect.x += self.velocity_x
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_x > 0:
                    self.rect.right = platform.left
                elif self.velocity_x < 0:
                    self.rect.left = platform.right

        self.rect.y += self.velocity_y
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if prev_y + self.rect.height <= platform.y:
                    self.rect.y = platform.y - self.rect.height
                    self.velocity_y = 0
                    self.on_ground = True

    def draw(self, screen):
        self.current_anim.blit(screen, self.rect.center)

def game_loop(screen, resources):
    clock = pygame.time.Clock()
    FPS = 60

    player = Player(48, 48, resources["player"])
    platforms = [
        pygame.Rect(300, 550, 100, 150),
        pygame.Rect(430, 500, 100, 150),
        pygame.Rect(100, 550, 100, 150),
        pygame.Rect(200, 480, 100, 150)
    ]

    running = True
    while running:
        screen.fill((255, 255, 255))

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

        player.update(platforms)

        for platform in platforms:
            screen.blit(resources["platform"], (platform.x, platform.y))

        player.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    screen = init_game()
    resources = load_resources()
    game_loop(screen, resources)
    pygame.quit()

import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_image(name):
    return pygame.image.load(name).convert_alpha()


def init_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Light and Shadow")
    return screen


def load_resources():
    sprite_sheet = load_image("textures/Idel Animation 48x48.png")
    player_sprite = AnimatedSprite(sprite_sheet, 10, 1, 48, 48)
    platform_image = pygame.image.load("textures/texture_1.png").convert_alpha()
    return {
        "player": player_sprite,
        "platform": pygame.transform.scale(platform_image, (150, 150))
    }


def update_player(player, velocity_x, velocity_y, platforms, gravity, jump_force):
    on_ground = False

    velocity_y += gravity

    player.rect.x += velocity_x
    player.rect.y += velocity_y

    if player.rect.x < 0:
        player.rect.x = 0
    elif player.rect.x + player.rect.width > 800:
        player.rect.x = 800 - player.rect.width

    for platform in platforms:
        if player.rect.colliderect(platform) and velocity_y > 0:
            player.rect.y = platform.y - player.rect.height
            velocity_y = 0
            on_ground = True

    return velocity_y, on_ground


def draw_objects(screen, resources, player, platforms):
    screen.fill((255, 255, 255))
    for platform in platforms:
        screen.blit(resources["platform"], (platform.x, platform.y))
    screen.blit(player.image, player.rect.topleft)
    pygame.display.flip()


def game_loop(screen, resources):
    clock = pygame.time.Clock()
    FPS = 60

    player = resources["player"]
    platforms = [
        pygame.Rect(50, 550, 150, 150),
        pygame.Rect(200, 400, 150, 150),
        pygame.Rect(400, 300, 150, 150)
    ]

    gravity = 0.8
    jump_force = -15
    velocity_x = 0
    velocity_y = 0
    move_speed = 5
    on_ground = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            velocity_x = -move_speed
        elif keys[pygame.K_RIGHT]:
            velocity_x = move_speed
        else:
            velocity_x = 0

        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = jump_force

        velocity_y, on_ground = update_player(
            player, velocity_x, velocity_y, platforms, gravity, jump_force
        )

        player.update()

        draw_objects(screen, resources, player, platforms)

        clock.tick(FPS)


if __name__ == "__main__":
    screen = init_game()
    resources = load_resources()
    game_loop(screen, resources)
    pygame.quit()
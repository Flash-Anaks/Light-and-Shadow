import pygame
import sys
import os

FPS = 50
pygame.init()

def load_image(name, colorkey=None):
    fullname = os.path.join('textures', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def fin_screen(time):
    fon = pygame.transform.scale(load_image('3.png'), (650, 650))
    screen.blit(fon, (0, 0))
    star = pygame.transform.scale(load_image('star.png'), (60, 50))
    star_coord = [(300, 150), (250, 200), (350, 200)]
    for i in range(3):
        screen.blit(star, (star_coord[i][0], star_coord[i][1]))
    font = pygame.font.Font(None, 50)
    text_coord = [(270, 170), (405, 264), (340, 220), (270, 300)]
    intro_text = ["Время:", "Заново", "Поздравляю!", time]
    for i in range(len(intro_text)):
        string_rendered = font.render(intro_text[i], 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.y = text_coord[i][0]
        intro_rect.x = text_coord[i][1]
        screen.blit(string_rendered, intro_rect)
    button_rect = pygame.Rect(260, 390, 130, 70)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print(1)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    screen = pygame.display.set_mode((650, 650))
    clock = pygame.time.Clock()
    fin_screen("11:56")
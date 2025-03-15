import pygame
import sys
import os

FPS = 60
pygame.init()

def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, colorkey=None):
    fullname = os.path.join('textures', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def show_help_window():
    help_screen = pygame.Surface((400, 300))
    help_screen.fill((200, 200, 200))
    font = pygame.font.Font(None, 30)
    text = ["Добро пожаловать в игру!", "Цель игры: дойти до правой стороны быстрее соперника.", "Управление:", "WAD - Движения Shadow", "стрелочки - Движения Light", "При падении вы появляетесь", " на исходной позиции"]

    y = 20
    for line in text:
        render_text = font.render(line, True, pygame.Color('black'))
        help_screen.blit(render_text, (20, y))
        y += 40

    screen.blit(help_screen, (125, 150))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False
    screen.fill((0, 0, 0))
    start_screen()

def start_screen():
    pygame.font.init()
    font = pygame.font.Font(None, 50)
    pygame.display.set_caption("Light and Shadow")
    fon = pygame.transform.scale(load_image('zastavka.jpg'), (650, 650))
    screen.blit(fon, (0, 0))
    text_ex_rect = pygame.Rect(195, 250, 275, 150)
    exit_b = font.render("Выход", 1, pygame.Color('black'))
    exit_rect = exit_b.get_rect()
    exit_rect.y = 570
    exit_rect.x = 500
    screen.blit(exit_b, exit_rect)
    push_exit_rect = pygame.Rect(500, 570, 120, 50)

    help_b = font.render("Помощь", 1, pygame.Color('black'))
    help_rect = exit_b.get_rect()
    help_rect.y = 10
    help_rect.x = 20
    screen.blit(help_b, help_rect)
    push_help_rect = pygame.Rect(10, 20, 120, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_ex_rect.collidepoint(event.pos):
                    pygame.quit()
                    return os.system('python LightAndShadow_main.py')
                elif push_exit_rect.collidepoint(event.pos):
                    pygame.quit()
                elif push_help_rect.collidepoint(event.pos):
                    show_help_window()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    screen = pygame.display.set_mode((650, 650))
    clock = pygame.time.Clock()
    start_screen()
    pygame.quit()

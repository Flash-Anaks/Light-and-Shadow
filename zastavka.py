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

def start_screen():
    pygame.display.set_caption("Light and Shadow")
    fon = pygame.transform.scale(load_image('zastavka.jpg'), (650, 650))
    screen.blit(fon, (0, 0))
    button_rect = pygame.Rect(195, 250, 275, 150)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.quit()
                    return os.system('python LightAndShadow_main.py')

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    screen = pygame.display.set_mode((650, 650))
    clock = pygame.time.Clock()
    start_screen()
    pygame.quit()

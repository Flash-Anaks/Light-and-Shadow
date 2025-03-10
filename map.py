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

class Button():
    def __init__(self, x, y, width, height, onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',}
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        # self.buttonSurf = pygame.transform.scale(load_image('but.png'), (50, 50))
        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            self.buttonSurface.fill(self.fillColors['pressed'])
            if self.onePress:
                print(1)
            elif not self.alreadyPressed:
                print(2)
                self.alreadyPressed = True
        else:
            self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurface, [
            self.buttonRect.width / 2 - self.buttonSurface.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurface.get_rect().height / 2])
        screen.blit(self.buttonSurface, self.buttonRect)

    def myFunction(self):
        print('Button Pressed')


def draw_exit_button(screen):
    font = pygame.font.SysFont("Arial", 30)
    text_surface = font.render("Выход", True, (255, 255, 255))  # Белый текст
    button_rect = pygame.Rect(10, 10, text_surface.get_width() + 10, text_surface.get_height() + 10)  # Прямоугольник под текстом
    pygame.draw.rect(screen, (0, 0, 0), button_rect)  # Черный фон для кнопки
    screen.blit(text_surface, (button_rect.x + 5, button_rect.y + 5))  # Рисуем текст на кнопке
    return button_rect

if __name__ == "__main__":
    screen = pygame.display.set_mode((650, 650))
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('form.png'), (650, 650))
    screen.blit(fon, (0, 0))
    objects = []
    font = pygame.font.SysFont('Arial', 40)
    all_sprites = pygame.sprite.Group()
    a = [[180, 200], [380, 200], [280, 350]]
    exit_button_rect = draw_exit_button(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    running = False
        for object in objects:
            object.process()
        pygame.display.flip()
        clock.tick(FPS)
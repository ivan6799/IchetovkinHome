import pygame, sys, random, os
from pygame.locals import *
from Util.loads import load_image


class Road:
    image = None
    image2 = None
    image_jungle = None
    def __init__(self, coords):
        if not self.image:
            Road.image = load_image("pdn_road_example.png", alpha_cannel=True, path='../Images/road parts')
        if not self.image2:
            Road.image2 = load_image("pdn_road_example.png", alpha_cannel=True, path='../Images/road parts')
            Road.image2 = pygame.transform.rotate(Road.image2, 180)
        if not self.image_jungle:
            Road.image_jungle = load_image('jungle.png', path='../Images')
        self.pos = coords
        self.rect = self.image.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect.topleft = self.pos
        self.rect2.topleft = self.rect.topright
        self.jungle_rect = self.image_jungle.get_rect()
        self.jungle_rect2 = self.image_jungle.get_rect()
        self.jungle_rect.topleft = ((0, 0))
        self.jungle_rect2.topleft =((self.rect2.right, 0))



    def update(self, speed):
        self.rect.y += speed
        self.rect2.y += speed
        self.jungle_rect.y += speed
        self.jungle_rect2.y += speed

    def render(self, screen):
        if -500 <= self.rect.y <= 1000:
            screen.blit(self.image, self.rect)
            screen.blit(self.image2, self.rect2)
        screen.blit(self.image_jungle, self.jungle_rect)
        screen.blit(self.image_jungle, self.jungle_rect2)



if __name__ == '__main__':

    FPS = 40
    clock = pygame.time.Clock()
    pygame.init()
    display = pygame.display.set_mode((750, 650))
    screen = pygame.display.get_surface()
    test = Road((200, 0))

    done = False
    while not done:
        # i = 0
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                done = True

            if e.type == pygame.KEYDOWN:
                if e.key == K_ESCAPE:
                    done = True

        dt = clock.tick(FPS)
        test.update(50)  # обновляем состояние объекта
        screen.fill((0, 0, 0))
        test.render(screen)
        pygame.display.flip()
import pygame, sys, random, os
from pygame.locals import *
from Util.loads import load_image


class Jungle:
    image = None
    def __init__(self, coords):
        if not self.image:
            Jungle.image = load_image('jungle.png', path='../Images')
        self.rect = self.image.get_rect()
        self.rect2 = self.image.get_rect()
        self.rect.topleft = (0,coords[1])
        self.rect2.topleft = (coords)




    def update(self, speed):
        self.rect.y += speed
        self.rect2.y += speed

    def render(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect2)



if __name__ == '__main__':

    FPS = 40
    clock = pygame.time.Clock()
    pygame.init()
    display = pygame.display.set_mode((750, 650))
    screen = pygame.display.get_surface()
    test = Jungle((800,-500))

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

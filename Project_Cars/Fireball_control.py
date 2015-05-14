import pygame, sys, random, os
from pygame.locals import *
from Util.loads import load_image
from Project_Cars.Fireball import  Fireball

class Fireball_Controll:
    def __init__(self):
        self.fireballs = []
        self.check = False

    def remove(self,i):
        self.fireballs.remove(i)

    def add_fireball(self, angle_of_rotate, pos):
        fireball = Fireball((pos),angle_of_rotate)
        self.fireballs.append(fireball)

    def event(self,event):
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.check = True


    def update(self,angle_of_rotate, pos):
        if self.check:
            self.add_fireball(angle_of_rotate, pos)
            self.check = False
        for i in self.fireballs:
            if i.rect.y<=-500:
                self.remove(i)
        for i in self.fireballs:
            i.update()



    def render(self,screen):
        for i in self.fireballs:
            i.render(screen)

if __name__=='__main__':

    FPS = 40
    clock = pygame.time.Clock()
    pygame.init()
    display = pygame.display.set_mode((750,650))
    screen = pygame.display.get_surface()
    test = Road_Control()

    done = False
    while not done:
        # i = 0
        for e in pygame.event.get():

            if e.type == pygame.QUIT :
                done = True

            if e.type == pygame.KEYDOWN:
                if e.key == K_ESCAPE:
                    done = True

        dt = clock.tick(FPS)
        test.update(50)            #обновляем состояние объекта
        screen.fill((0,0,0))
        test.render(screen)
        pygame.display.flip()


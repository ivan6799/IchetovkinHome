import pygame, sys, random, os
from pygame.locals import *
from Util.loads import load_image
from Project_Cars.road_part import  Road
from Project_Cars.jungle import Jungle


OPTIMAL_LEN = 297



class Road_Control:
    def __init__(self, road_x=200, road_w=299, road_h = 297):
        self.roads = []
        self.jungles = []
        self.x1 = road_x
        self.w = road_w
        self.x2 = road_x+road_w
        self.h = road_h


    def add_road(self):
        if not self.roads:
            a = Road((self.x1, self.h*-1))
            b = Road((self.x1, a.rect.y + self.h))
            c = Road((self.x1, b.rect.y + self.h))
            d= Road((self.x1, c.rect.y + self.h))
            e = Road((self.x1, self.h*-2))
            self.roads.append(e)
            self.roads.append(a)
            self.roads.append(b)
            self.roads.append(c)
            self.roads.append(d)

        else:
            if self.roads[len(self.roads)-1].rect.y + self.h>=self.h*4:
                a = Road((self.x1, self.h*-1))
                b = Road((self.x1, a.rect.y + self.h))
                c = Road((self.x1, b.rect.y + self.h))
                d= Road((self.x1, c.rect.y + self.h))
                e = Road((self.x1, self.h*-2))
                self.roads.append(e)
                self.roads.append(a)
                self.roads.append(b)
                self.roads.append(c)
                self.roads.append(d)

    def add_jungle(self):
        if not self.jungles:
            a = Jungle((self.x2+self.w, 0))
            b = Jungle((self.x2+self.w, -1000))
            self.jungles.append(a)
            self.jungles.append(b)
        else:
            if self.jungles[len(self.jungles)-1].rect.y >=0:
                a = Jungle((self.x2+self.w, 0))
                b = Jungle((self.x2+self.w, -1000))
                self.jungles.append(a)
                self.jungles.append(b)




    def update(self, speed):
        self.add_road()
        self.add_jungle()
        for i in self.roads:
            i.update(speed)
        for i in self.jungles:
            i.update(speed)

    def get_static_rect(self):
        self.staticrect = pygame.Rect((0,0), (self.x1, self.h*5))
        return self.staticrect

    def get_static_rect2(self):
        self.staticrect2 = pygame.Rect((self.x2+self.w, 0), (self.x1, self.h*5))
        return self.staticrect2



    def render(self,screen):
        for i in self.roads:
            i.render(screen)
        for i in self.jungles:
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

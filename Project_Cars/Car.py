import math

import pygame
from pygame.locals import *

from Classes.Vector import Vector
from Util.loads import load_image
from Project_Cars.road_control import Road_Control
from Project_Cars.Barrier_control import Barrel_Control
from Project_Cars.Fireball_control import Fireball_Controll

MOVE = 0
TURN_LEFT = 1
TURN_RIGHT = 2
STOP = 3
ACCEL_UP = 4
ACCEL_DOWN = 5


class Car:
    K_ACCELERATE = 24
    K_FRICTION = -5

    def __init__(self, pos):
        self.image = load_image('racecar.png', alpha_cannel=True, path='../Images')
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (75, 50))
        self.rect = self.image.get_rect()
        self.pos = Vector(pos)
        self.start_pos = Vector(pos)
        self.rect.topleft = pos
        self.accel = Vector((0, 0))
        self.rect_img = self.image.get_rect()
        self.speed = Vector((0, -10))
        # self.friction = self.speed.normalize()*-5
        self.angle_speed = 40
        self.status_accel = MOVE
        self.status_turn = MOVE
        self.fire = False
        self.max_speed = Vector((181, 0))
        self.change_move_func = False
        self.angle_of_rotate = 0
        self.points = 0


    def friction(self):
        return self.speed.normalize()*self.K_FRICTION

    def text_render(self, screen):
        a = str(int(self.speed.len()))
        b = str(self.points)
        b = 'Очки:' + b
        font = pygame.font.Font(None, 30)
        font2 = pygame.font.Font(None, 40)
        text = font.render(a, True, (255,255,255),None)
        text2 = font2.render(b, True, (255,255,255), None)
        textRect = text.get_rect()
        textRect2 = text2.get_rect()
        textRect.topleft = (67,180)
        textRect2.topleft = (50, 600)
        screen.blit(text, textRect)
        screen.blit(text2, textRect2)

    def event(self, event):
        """
        Обрабатываем события
        """
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.status_accel = ACCEL_UP
                self.accel = self.speed.normalize()*self.K_ACCELERATE + self.friction()
            if event.key == K_DOWN:
                self.status_accel = ACCEL_DOWN
                self.accel = self.speed.normalize()*-self.K_ACCELERATE + self.friction()
            if event.key == K_LEFT:
                self.status_turn = TURN_LEFT
            if event.key == K_RIGHT:
                self.status_turn = TURN_RIGHT
            if event.key == K_SPACE:
                self.fire = True


        elif event.type == KEYUP:
            if event.key == K_LEFT:
                self.status_turn = MOVE
            elif event.key == K_RIGHT:
                self.status_turn = MOVE
            elif event.key == K_UP or event.key == K_DOWN:
                self.accel = self.friction()
                self.status_accel = MOVE



    def aclerate(self, dt):

        if self.speed < (self.accel*(dt/700)):
            if self.status_accel == ACCEL_UP:
                self.speed = self.speed + self.accel*(dt/700)
            else:
                self.accel = Vector((0, 0))
        else:
            speed_temp = self.speed
            self.speed = self.speed + self.accel*(dt/700)
            if self.speed > self.max_speed:
                self.speed = speed_temp

    def speed_metr(self, screen):
        speedometer = load_image("speedometer.png", alpha_cannel=True, path='../Images')
        speedometer = pygame.transform.scale(speedometer, (113, 56))
        rectSpeedMetr = speedometer.get_rect()
        rectSpeedMetr.topleft = (20,120)
        a = (rectSpeedMetr.midtop[0]-rectSpeedMetr.bottomleft[0])/90
        b = (rectSpeedMetr.midtop[1]-rectSpeedMetr.bottomleft[1])/90
        c = (rectSpeedMetr.bottomright[1]-rectSpeedMetr.midtop[1])/90
        d = (rectSpeedMetr.bottomright[0]-rectSpeedMetr.midtop[0])/90
        if self.speed.len()<=90:
            pygame.draw.lines(screen, (255,0,0), False, [(rectSpeedMetr.midbottom[0], rectSpeedMetr.midbottom[1]),  (rectSpeedMetr.bottomleft[0]+a*self.speed.len(),rectSpeedMetr.bottomleft[1]+b*self.speed.len())])
        elif self.speed.len()>=90:
            pygame.draw.lines(screen, (255,0,0), False, [(rectSpeedMetr.midbottom[0], rectSpeedMetr.midbottom[1]),  (rectSpeedMetr.midtop[0]+d*(self.speed.len()-90),rectSpeedMetr.midtop[1]+c*(self.speed.len()-90))])
        screen.blit(speedometer, rectSpeedMetr)


    def move(self, dt):
        """
        Передвигаем объект
        """
        self.aclerate(dt)
        self.pos.x += self.speed.x*(dt/700)

    def move2(self, dt):
        """
        Нужен для движения машины в последнем блоке дороги
        """
        self.aclerate(dt)
        self.pos += self.speed*(dt/700)

    def update(self, dt):
        """
        Обновляем состояние(местоположение, угол поворота и т.п.) объекта
        Этот метод должен вызываться перед отрисовкой каждого кадра
        Как правило, из данного метода вызываются другие методы, которые изменяют нужное состояние объекта

        """

        if self.status_turn == TURN_RIGHT:
            self.speed.rotate(self.angle_speed/500*dt)
        if self.status_turn == TURN_LEFT:
            self.speed.rotate(-self.angle_speed/500*dt)

        if self.status_accel == MOVE:
            """
            Регулирует движение машины, когда событий нет
            """
            self.accel = self.friction()
            # if self.accel*(dt/700)!=self.friction():
            #     # print(self.accel, "self accel")
            #     # print(self.friction(), "friction")
            if self.speed < (self.accel*(dt/1000)):
                if self.status_accel == ACCEL_UP:
                    self.speed = self.speed + self.accel*(dt/1000)
                else:
                    self.accel = Vector((0, 0))


        if self.change_move_func == False:
            self.move(dt)
        elif self.change_move_func == True:
            self.move2(dt)




    def render(self, screen):
        """
        Отрисовываем объект на поверхность screen
        """
        self.angle_of_rotate = math.degrees(math.acos(self.speed.normalize().x))
        if self.speed.y>0:
            self.angle_of_rotate = 360-self.angle_of_rotate

        rotated_img = pygame.transform.rotate(self.image, self.angle_of_rotate)
        self.rect_img = rotated_img.get_rect()
        self.rect_img.center = self.pos.as_point()
        screen.blit(rotated_img, self.rect_img)
        # pygame.draw.lines(screen, (255,0,0), False, [self.pos.as_point(),  (self.pos.x+self.speed.x, self.pos.y+self.speed.y)])
        self.text_render(screen)
        self.speed_metr(screen)
        # pygame.draw.rect(screen,(255,0,0), self.rect_img)
        # print()

if __name__ == '__main__':

    SCREEN_X = 1000
    SCREEN_Y = 800
    FPS = 40
    clock = pygame.time.Clock()
    pygame.init()
    display = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
    screen = pygame.display.get_surface()
    testRoad = Road_Control()
    testCar = Car((200+ (testRoad.x2-testRoad.x1)/2, 400))
    testBarrel = Barrel_Control()
    testFireball = Fireball_Controll()



    done = False
    while not done:
        # i = 0
        for e in pygame.event.get():

            if e.type == pygame.QUIT :
                done = True

            if e.type == pygame.KEYDOWN:
                if e.key == K_ESCAPE:
                    from Project_Cars.Menu import *
                    break

            testCar.event(e) #Передаем все события объекту
            testFireball.event(e)
        dt = clock.tick(FPS)

        pos1 = testCar.pos
        testCar.update(dt)            #обновляем состояние объекта
        testFireball.update(testCar.angle_of_rotate, testCar.pos.as_point())

        if testCar.rect_img.y + testCar.rect_img.h >= SCREEN_Y: #Проверяет выход за рабочую зону
            if testCar.speed.y>=0:
                testCar.pos = pos1

        """
        Следющий блок отвечает за направление дороги, а так же не позволяет выйти машине за нижний предел
        """
        if testCar.speed.y<0:
            testBarrel.update(int(testCar.speed.y/10*-1),testCar.pos.y)
            testRoad.update(int(testCar.speed.y/3*-1))
            if testCar.pos.y<= testCar.start_pos.y:
                testCar.change_move_func = False
        else:
            if testRoad.roads[3].rect.colliderect(testCar.rect_img):
                testCar.change_move_func = True
                testBarrel.update(0,testCar.pos.y)
                testRoad.update(0)

            else:
                testCar.change_move_func = False
                testBarrel.update(int(testCar.speed.y/10*-1), testCar.speed.y)
                testRoad.update(int(testCar.speed.y/3*-1))
        """
        Проверяет столкновение машины с бочкой
                """

        for barrel in testBarrel.barrels:
            if barrel.rect.colliderect(testCar.rect_img):
                testCar.speed = testCar.speed*0.3
                testBarrel.remove_barrel(barrel)
        """
        Проверяет выход машины за дорогу
                """

        if testRoad.get_static_rect().colliderect(testCar.rect_img) or testRoad.get_static_rect2().colliderect(testCar.rect_img):
            if testRoad.get_static_rect().colliderect(testCar.rect_img) == True:
                if testCar.speed.x>0:
                    testCar.pos.x = testCar.pos.x + testCar.speed.x*dt/700
                elif testRoad.get_static_rect2().colliderect(testCar.rect_img) == True:
                    if testCar.speed.x<0:
                        testCar.pos.x = testCar.pos.x + testCar.speed.x*dt/7000
            testCar.pos.x = testCar.pos.x - testCar.speed.x*dt/700



        screen.fill((0,0,0))
        testRoad.render(screen)
        testCar.render(screen)      #отрисовываем объект
        testBarrel.render(screen)
        testFireball.render(screen)
        pygame.display.flip()
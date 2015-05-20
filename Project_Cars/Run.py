
import pygame
from Util import  load_image
from  Project_Cars.Car import Car
from Project_Cars.Menu import Button
from Project_Cars.Barrier_control import Barrel_Control
from Project_Cars.road_control import Road_Control
from Project_Cars.Fireball_control import Fireball_Controll
import random

pygame.init()
SCREEN_X = 1000
SCREEN_Y = 700
FPS = 40
clock = pygame.time.Clock()
pygame.init()
display = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
screen = pygame.display.get_surface()
testRoad = Road_Control()
testCar = Car((200+ (testRoad.x2-testRoad.x1)/2, 400))
testBarrel = Barrel_Control()
testFireball = Fireball_Controll()
MainBut = Button((180 - 186 / 2, 550), ["button_hover.png", "button_off.png", "button_click.png"], None, "Start")
MainBut2 = Button((500 - 186 / 2, 550), ["button_hover.png", "button_off.png", "button_click.png"], None, "Best score")
MainBut3 = Button((820 - 186 / 2, 550), ["button_hover.png", "button_off.png", "button_click.png"], None, "Exit")
background = load_image("PC.jpg", path='../Images')
background_rect = background.get_rect()
background_rect.topleft = (0,0)

done = True
done2 = False
while not done2:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done2 = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                done2 = True
        MainBut.event(e)
        MainBut2.event(e)
        MainBut3.event(e)
        if MainBut3.event(e):
            done2 = True
        if MainBut.event(e):
            done = False

    screen.fill((0, 0, 0))
    screen.blit(background,background_rect)
    MainBut.render(screen)
    MainBut2.render(screen)
    MainBut3.render(screen)
    pygame.display.flip()

    while not done:
        # i = 0
        for e in pygame.event.get():

            if e.type == pygame.QUIT :
                done = True


            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    testRoad = Road_Control()
                    testCar = Car((200+ (testRoad.x2-testRoad.x1)/2, 400))
                    testBarrel = Barrel_Control()
                    testFireball = Fireball_Controll()
                    done = True


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
            testBarrel.update(int(testCar.speed.y/7*-1),testCar.pos.y)
            testRoad.update(int(testCar.speed.y/7*-1))
            if testCar.pos.y<= testCar.start_pos.y:
                testCar.change_move_func = False
        else:
            if testRoad.roads[3].rect.colliderect(testCar.rect_img):
                testCar.change_move_func = True
                testBarrel.update(0,testCar.pos.y)
                testRoad.update(0)

            else:
                testCar.change_move_func = False
                testBarrel.update(int(testCar.speed.y/7*-1), testCar.pos.y)
                testRoad.update(int(testCar.speed.y/7*-1))
        """
        Проверяет столкновение машины с бочкой
                """

        for barrel in testBarrel.barrels:
            if barrel.rect.colliderect(testCar.rect_img):
                testCar.speed = testCar.speed*0.7
                testBarrel.remove_barrel(barrel)
                testBarrel.barrel_forfeit+=1
                testCar.points += int(testCar.speed.len())*-14
                if testCar.points<0:
                    testCar.points = 0

        for barrel in testBarrel.barrels:
            testCar.points += barrel.test_equal(testCar.pos.y) * (int(testCar.speed.len()) + random.randint(0,15))


        for fire_barrel in testBarrel.fire_bareels:
            if fire_barrel.rect.colliderect(testCar.rect_img):
                testBarrel.remove_fire_barrel(fire_barrel)


        for fireball in testFireball.fireballs:
            for barrel in testBarrel.barrels:
                if barrel.rect.colliderect(fireball.rect_img):
                    testBarrel.remove_barrel(barrel)
                    testFireball.remove(fireball)
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




        print(testCar.speed.x)
        screen.fill((0,0,0))
        testRoad.render(screen)
        testCar.render(screen)
        testBarrel.render(screen)
        testFireball.render(screen)
        pygame.display.flip()

        if testBarrel.barrel_forfeit == 25:
            i = 0
            while True:
                for e in pygame.event.get():
                    if e.type!= pygame.KEYDOWN:

                        a = 'А также набрали ' + str(testCar.points) + ' ' +'очков, а это значит, что вы отправляетесь на доску почета, наверное.'
                        font = pygame.font.Font(None, 30)
                        text = font.render("Игра окончена! Вы сбили 25 ящиков, тем самым разбив машину!", True, (255,255,255),None)
                        text2 = font.render(a, True, (25,255,55),None)
                        text3 = font.render('Помните, что разработчик вами недоволен!', True, (255,25,25),None)
                        textRect = text.get_rect()
                        textRect2 = text.get_rect()
                        textRect3 = text.get_rect()
                        textRect.topleft = (SCREEN_X/6,150)
                        textRect2.topleft = (SCREEN_X/12,200)
                        textRect3.topleft = (SCREEN_X/4,250)
                        screen.blit(text, textRect)
                        screen.blit(text2, textRect2)
                        screen.blit(text3, textRect3)
                        pygame.display.flip()
                    elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                             i = 1
                if i:
                    break

            done = True
            done2 = True

import pygame
from  Project_Cars.Car import Car
from Project_Cars.Menu import Button
from Project_Cars.Barrier_control import Barrel_Control
from Project_Cars.road_control import Road_Control

pygame.init()
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
MainBut = Button((500 - 186 / 2, 150), ["button_hover.png", "button_off.png", "button_click.png"], None, "Start")
MainBut2 = Button((500 - 186 / 2, 250), ["button_hover.png", "button_off.png", "button_click.png"], None, "Best score")
MainBut3 = Button((500 - 186 / 2, 350), ["button_hover.png", "button_off.png", "button_click.png"], None, "Exit")

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
                    done = True

            testCar.event(e) #Передаем все события объекту
        dt = clock.tick(FPS)

        pos1 = testCar.pos
        testCar.update(dt)            #обновляем состояние объекта
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
            if testRoad.roads[3].rect.colliderect(testCar.rect_img) or testRoad.roads[8].rect.colliderect(testCar.rect_img):
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
                testCar.speed = testCar.speed*0.5
                testBarrel.remove_barrel(barrel)
                testBarrel.barrel_forfeit+=1
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
        pygame.display.flip()
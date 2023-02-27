import random
import sys
import time
from venv import create
import pygame
from pygame.locals import *
from collections import deque

from sqlalchemy import false

#基础设置
Screen_Height=480
Screen_Width=600
Size=20#小方格大小
Line_Width=1
#游戏区域的坐标范围
Area_x=(0,Screen_Width//Size-1) #0是左边界，1是右边界 #注：python中//为整数除法；/为浮点数除法
Area_y=(2,Screen_Height//Size-1)
#食物的初步设置
#食物的分值+颜色
Food_Style_List=[(10,(255,100,100)),(20,(100,255,100)),(30,(100,100,255))]
#整体颜色设置
Light=(100,100,100)
Dark=(200,200,200)
Black=(0,0,0)
Red=(200,30,30)
Back_Ground=(40,40,60)

class env():
    def __init__(self) -> None:
        self.screen_height = 480
        self.screen_width = 600
        self.size = 20
        self.line_width = 1
        self.area_x = (0,Screen_Width//Size-1)
        self.area_y = (2,Screen_Height//Size-1)
        self.food_style_list = [(10,(255,100,100)),(20,(100,255,100)),(30,(100,100,255))]
        self.light = (100,100,100)
        self.dark = (200,200,200)
        self.black = (0,0,0)
        self.red = (200,30,30)
        self.back_ground = (40,40,60)

    def Print_Text(screen,font,x,y,text,fcolor=(255,255,255)):
        Text=font.render(text,True,fcolor)
        screen.blit(Text,(x,y))
    def init_snake(self):
        self.snake = deque()
        self.snake.append(Area_x[0]+2,Area_y[0])
        self.snake.append(Area_x[0]+1,Area_y[0])
        self.snake.append(Area_x[0],Area_y[0])
        
    def Creat_food(self):
        self.food_x = random.randint(Area_x[0], Area_x[1])
        self.food_y = random.randint(Area_y[0], Area_y[1])
        while (self.food_x,self.food_y) in  self.snake:
            self.food_x = random.randint(Area_x[0], Area_x[1])
            self.food_y = random.randint(Area_y[0], Area_y[1])
    def Food_Style(self):
        self.food_style = Food_Style_List[random.randint(0,2)]
    def Start(self):
        self.game = pygame
        self.game.init()
        self.screen = self.game.display.set_mode((self.screen_width,self.screen_height))
        self.game.display.set_caption('snake game')
        self.font1 = pygame.font.SysFont('SimHei',24)
        self.font2 = pygame.font.SysFont(None, 72)
        self.fwidth, self.fheight = self.font2.size('GAME OVER')
        self.flag = True
        self.snake = self.init_snake()
        self.food = self.Creat_food(snake = self.snake)
        self.Food_Style()
        self.pos = (0,1)
        self.game_over = True
        self.game_start = False
        self.score = 0
        self.orispeed = 0.3

        





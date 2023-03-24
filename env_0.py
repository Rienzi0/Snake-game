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
        print("successfully initialized")

    def Print_Text(self,screen,font,x,y,text,fcolor=(255,255,255)):
        Text=font.render(text,True,fcolor)
        screen.blit(Text,(x,y))

    def init_snake(self):
        snake = deque()
        # snake.append((self.area_x[0]+2,self.area_y[0]))
        # snake.append((self.area_x[0]+1,self.area_y[0]))
        # snake.append((self.area_x[0],self.area_y[0]))
        snake.append((13,10))
        snake.append((12,10))
        snake.append((11,10))
        snake.append((10,10))


        return snake
        
        
    def Creat_food(self):
        food_x = random.randint(self.area_x[0], self.area_x[1])
        food_y = random.randint(self.area_y[0], self.area_y[1])
        while (food_x,food_y) in  self.snake:
            food_x = random.randint(self.area_x[0], self.area_x[1])
            food_y = random.randint(self.area_y[0], self.area_y[1])
        return food_x,food_y
        
    def Food_Style(self):
        food_style = self.food_style_list[random.randint(0,2)]
        return food_style

    def Ready(self):
        self.game = pygame
        self.game.init()
        self.screen = self.game.display.set_mode((self.screen_width,self.screen_height))
        self.game.display.set_caption('snake game')
        self.font1 = pygame.font.SysFont('SimHei',24)
        self.font2 = pygame.font.SysFont(None, 72)
        self.fwidth, self.fheight = self.font2.size('GAME OVER')
        self.flag = True
        self.snake = self.init_snake()
        self.food = self.Creat_food()
        self.Food_Style()
        self.pos = (1,0)
        self.game_over = True
        self.game_start = False
        self.score = 0
        self.orispeed = 0.03
        self.speed = self.orispeed
        self.last_move_time = None
        self.pause = False
        

    def Start(self):
        if self.game_over:
            self.game_start = True
            self.game_over = False
            self.snake = self.init_snake()
            self.food_style = self.Food_Style()
            self.pos = (1,0)
            self.score = 0
            self.score_list = [0]
            self.dis_list = []
            self.last_move_time = time.time()
        self.screen.fill(self.back_ground)
        for x in range(self.size,self.screen_width,self.size):
            self.game.draw.line(self.screen,self.black,(x, self.area_y[0] * self.size),(x,self.screen_height),self.line_width)
        for y in range(Area_y[0] * self.size, self.screen_height, self.size):
            self.game.draw.line(self.screen, self.black, (0, y), (self.screen_width, y), self.line_width)
        
    # def action_trans(self,pos,move):
    #     if pos == (1,0): #right
    #         if move[0] == 1:
    #             pos = (0,-1)
    #         elif move[1] == 1:
    #             pos = pos
    #         elif move[2] == 1:
    #             pos = (0,1)
    #     elif pos == (-1,0): #left
    #         if move[0] == 1:
    #             pos = (0,1)
    #         elif move[1] == 1:
    #             pos = pos
    #         elif move[2] == 1:
    #             pos = (0,-1)
    #     elif pos == (0,1): #down
    #         if move[0] == 1:
    #             pos = (1,0)
    #         elif move[1] == 1:
    #             pos = pos
    #         elif move[2] == 1:
    #             pos = (-1,0)
    #     elif pos == (0,-1): #up
    #         if move[0] == 1:
    #             pos = (-1,0)
    #         elif move[1] == 1:
    #             pos = pos
    #         elif move[2] == 1:
    #             pos = (1,0)
    #     return pos
    def action_trans(self,pos,move):
        if pos == (1,0): #right
            if move[0] == 0:
                pos = (0,-1)
            elif move[0] == 1:
                pos = pos
            elif move[0] == 2:
                pos = (0,1)
        elif pos == (-1,0): #left
            if move[0] == 0:
                pos = (0,1)
            elif move[0] == 1:
                pos = pos
            elif move[0] == 2:
                pos = (0,-1)
        elif pos == (0,1): #down
            if move[0] == 0:
                pos = (1,0)
            elif move[0] == 1:
                pos = pos
            elif move[0] == 2:
                pos = (-1,0)
        elif pos == (0,-1): #up
            if move[0] == 0:
                pos = (-1,0)
            elif move[0] == 1:
                pos = pos
            elif move[0] == 2:
                pos = (1,0)
        return pos
    def Step(self,move): # move = [1,0,0] or [0,1,0] or [0,0,1]
        self.screen.fill(self.back_ground)
        for x in range(self.size,self.screen_width,self.size):
            self.game.draw.line(self.screen,self.black,(x, self.area_y[0] * self.size),(x,self.screen_height),self.line_width)
        for y in range(Area_y[0] * self.size, self.screen_height, self.size):
            self.game.draw.line(self.screen, self.black, (0, y), (self.screen_width, y), self.line_width)
        
        if not self.game_over:
            curTime = time.time()
            if curTime - self.last_move_time > self.speed:
                self.pos = self.action_trans(self.pos,move)
                self.last_move_time = curTime
                next_s = (self.snake[0][0] + self.pos[0], self.snake[0][1] + self.pos[1])
                if next_s == self.food:
                    self.snake.appendleft(next_s)
                    self.score += self.food_style[0]
                    self.score_list.append(self.score)
                    self.speed = self.orispeed - 0.03 * (self.score//100)
                    self.food = self.Creat_food()
                    self.food_style = self.Food_Style()
                else:
                    
                    if self.area_x[0]<=next_s[0]<=self.area_x[1] and self.area_y[0]<=next_s[1]<=self.area_y[1] and next_s not in self.snake:
                        self.snake.appendleft((next_s))
                        self.snake.pop()
                    else:
                        self.game_over = True
        head = self.snake[0]
        food = self.food
        dis = (head[0]-food[0]) ** 2 + (head[1]-food[1]) ** 2
        self.dis_list.append(dis)
        if not self.game_over:
            self.game.draw.rect(self.screen, self.food_style[1], (self.food[0] * Size, self.food[1] * Size, Size, Size), 0)
        for s in self.snake:
            self.game.draw.rect(self.screen, self.dark, (s[0] * self.size + self.line_width, s[1] * self.size + self.line_width, self.size - self.line_width * 2, self.size - self.line_width * 2), 0)
        self.Print_Text(self.screen, self.font1, 30, 7, f'speed: {self.score // 100}')
        self.Print_Text(self.screen, self.font1, 450, 7, f'score: {self.score}')  
        self.game.display.update()
        #print("steped")
        if self.game_over == True:
            self.game.quit()
            return self.game_over

        return self.game_over
    def get_state(self):
        score = self.score 
        direction_x, direction_y = self.pos[0],self.pos[1]
        _body = [s for s in self.snake]
        snake_body = [i for i in range(20)]
        for i,pos in enumerate (_body):
            snake_body[i] = pos[0]
            snake_body[2*i] = pos[1]
            # snake_body.append(i[0])
            # snake_body.append(i[1]) 

        speed = self.speed
        food_x,food_y =self.food
        state = [score,direction_x,direction_y,speed,food_x,food_y] + snake_body

        #self.game.display.update()
        return state
   

    
        
if __name__ == "__main__":
    en = env()
    en.Ready()
    en.Start()
    game_over = False
    num = 4000
    while num > 1:
        game_over = en.Step([1,0,0])
        body = en.get_state()
        print(body)
        print(en.pos)
        num -= 1
        if game_over == 1:
            del en

    
    







    
    

        


            

        



 

        

    




        





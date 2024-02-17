import sys
import pygame
from pygame.sprite import Group
import numpy as np
import cv2
import time
import random
from random import random as rnd
from base import Base
from collectible import Collectible

#__resources library

random.seed(5)


# f = open('team.txt','r')
# TL = [F.strip() for F in f.readlines()]
# f.close()
# f = open('list.txt')
# ML = [F.strip() for F in f.readlines()]
# LM = []
# for m in ML:
#     x = m.split(',')
#     LM.append((x[0],(int(x[1]),int(x[2])),(int(x[3]),int(x[4]))))
# x2 = int(input('Enter a number between 0 and 39?'))



class Game():

        
    def __init__(self, dim, map_img, redt, bluet):
        pygame.init()
        self.redt = redt
        self.bluet = bluet
        self.__dim = dim
        self.screen = pygame.display.set_mode((self.__dim[0]*20+400,self.__dim[1]*20))
        self.fps_controller = pygame.time.Clock()
        
        # self.redbasepos = red_pos
        # self.bluebasepos= blue_pos
        [flag1, flag2, flag3] = self.getPositions()

        island1 = []
        island2 = []
        island3 = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                island1.append((flag1[0] + i, flag1[1] + j))
                island2.append((flag2[0] + i, flag2[1] + j))
                island3.append((flag3[0] + i, flag3[1] + j))

        self.flag1 = flag1
        self.flag2 = flag2
        self.flag3 = flag3

        self.island1 = island1
        self.island2 = island2
        self.island3 = island3

        self.__rum = Group()
        self.__gunpowder = Group()
        self.__rum = Group()

        self.__resources, self.__rum, self.__gunpowder, self.__wood = self.create_map(map_img)
        # self.__resources[self.redbasepos[1]][self.redbasepos[0]] = 0
        # self.__resources[self.bluebasepos[1]][self.bluebasepos[0]] = 0
        self.GlobalPirateCount = 0
        self.explosion = pygame.image.load("explode.png")
        self.rate = 8

        self.__collectibles = []
        
        self.__PositionToPirate = {} #???????????????????????????

        for i in range(self.__dim[0]):
            Z = []
            for j in range(self.__dim[1]):
                Z.append(Collectible(self.screen, i*20, j*20, self.__resources[j][i]))
            self.__collectibles.append(Z)
        
        

        self.__bluebots = Group()
        self.__redbots = Group()
        self.__Pirates = np.zeros((self.__dim[1], self.__dim[0]))
        # 0 in self.Pirates means no Pirates
        # 1 means one Pirate of red team
        # 2 means one Pirate of blue team
        # 3 means base for team red
        # 4 means base for team blue

        self.__redbase = Base(self.screen, self.redbasepos[0]*20, self.redbasepos[1]*20, 'red', self.__redbots, self.__Pirates,self)
        self.__bluebase = Base(self.screen, self.bluebasepos[0]*20, self.bluebasepos[1]*20, 'blue', self.__bluebots, self.__Pirates,self)
        self.__PositionToPirate[self.redbasepos] = {self.__redbase:True}
        self.__PositionToPirate[self.bluebasepos] = {self.__bluebase:True}
        self.update_score()

    def getPositions(self):
        excluded = random.randint(0, 3)        
        l = []
        for i in range(4):
            if i == excluded:
                continue
            if i == 0:
                x = random.randint(80, self.__dim[0]*20/2 - 80)/20
                y = random.randint(80, self.__dim[1]*20/2 - 80)/20
                l.append((x, y))
            elif i == 1:
                x = random.randint(self.__dim[0]*20/2 + 80, self.__dim[0]*20 - 80)/20
                y = random.randint(80, self.__dim[1]*20/2 - 80)/20
                l.append((x, y))
            elif i == 2:
                x = random.randint(80, self.__dim[0]*20/2 - 80)/20
                y = random.randint(self.__dim[1]*20/2 + 80, self.__dim[1]*20 - 80)/20
                l.append((x, y))
            else:
                x = random.randint(self.__dim[0]*20/2 + 80, self.__dim[0]*20 - 80)/20
                y = random.randint(self.__dim[1]*20/2 + 80, self.__dim[1]*20 - 80)/20
                l.append((x, y))
        return l
        


    def run_game(self):
        iter = 0
        while True:
            iter+=1
            if iter > 1500:
                self.game_over_iter()
                self.check_events()
                continue
            self.screen.fill((60,60,60))
            print(np.sum((self.__resources > 50).astype('int')))
            moves = {}
            if (rnd()>0.5):
                try:
                    scriptblue.ActBase(self.__bluebase)
                except:
                    print("Bluebase error")
                try:
                    scriptred.ActBase(self.__redbase)
                except:
                    print("Redbase error")
                
                for robo in self.__redbots:
                    try:
                        n = scriptred.ActPirate(robo)
                    except:
                        n=0
                        print("Redbot error")
                    moves[robo] = n
                for robo in self.__bluebots:
                    try:
                        n = scriptblue.ActPirate(robo)
                    except:
                        n=0
                        print("Blubot error")
                    moves[robo] = n
            else:
                try:
                    scriptred.ActBase(self.__redbase)
                except:
                    print("Redbase error")
                try:
                    scriptblue.ActBase(self.__bluebase)
                except:
                    print("Bluebase error")

                for robo in self.__bluebots:
                    try:
                        n = scriptblue.ActPirate(robo)
                    except:
                        n=0
                        print("Blue bot error")
                    moves[robo] = n

                for robo in self.__redbots:
                    try:
                        n = scriptred.ActPirate(robo)
                    except:
                        n=0
                        print("Redbot error")
                    moves[robo] = n
            
            
            for robo, n in moves.items():
                if n == 1:
                    robo.move_up()
                elif n == 2:
                    robo.move_right()
                elif n == 3:
                    robo.move_down()
                elif n == 4:
                    robo.move_left()  
            collisions  = self.check_collisions()
            self.updateRoboMap()
            self.collect()
            for i in range(0,self.__dim[0]):
                for j in range(0,self.__dim[1]):
                    self.__collectibles[i][j].blitme()
            # self.__bluebase.blitme()
            # self.__redbase.blitme()
            
            # self.__bluebots.draw(self.screen)
            # self.__redbots.draw(self.screen)

            self.flag1.blitme()
            self.flag2.blitme()
            self.flag3.blitme()

            self.__rum.draw(self.screen)
            self.__gunpowder.draw(self.screen)
            self.__wood.draw(self.screen)

            for b in collisions.keys():
                self.screen.blit(self.explosion, b.rect)
            self.update_score()
            self.buttons()
            pygame.display.flip()
            self.__redbase._Base__MovingAverage = (self.__redbase._Base__MovingAverage*(0.9)) + (self.__redbase._Base__TotalTeamElixir*(0.1))
            
            self.__bluebase._Base__MovingAverage = (self.__bluebase._Base__MovingAverage*(0.9)) + (self.__bluebase._Base__TotalTeamElixir*(0.1))
            if iter % 10 == 0:
                self.replenish()
            self.check_events()
            self.fps_controller.tick(self.rate)
            #pygame.display.iconify()
            self.game_over()
       

    def game_over_iter(self):
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__bluebase._Base__MovingAverage > self.__redbase._Base__MovingAverage:
            print( "Blue Wins")
            game_over = game_over_font.render(self.bluet + " Wins", True, (100,100,255), (230,230,230))
            
        else:
            
            print( "Red Wins")
            game_over = game_over_font.render(self.redt+ " Wins", True, (255,100,100), (230,230,230))
        self.screen.blit(game_over, ((self.__dim[0])*10,(self.__dim[1])*10))
        pygame.display.flip()

    def updateRoboMap(self):
        for i in range(0,self.__dim[1]):
            for j in range(0,self.__dim[0]):
                self.__Pirates[i][j] = 0
        for key in self.__PositionToPirate.keys():
            value = self.__PositionToPirate[key]
            entr = 0
            for v in value:
                if v==self.__redbase:
                    entr = 3
                    break
                if v==self.__bluebase:
                    entr = 4
                    break
                if v.type=="red":
                    entr = 1
                else:
                    entr = 2
            self.__Pirates[key[1]][key[0]] = entr

    def buttons(self):
        button_font = pygame.font.SysFont(None, 36)
        slow_down = button_font.render("Slower", True, (230,230,230))
        self.slow_rect = slow_down.get_rect()
        self.slow_rect.center = ((self.__dim[0])*20+60, self.__dim[1]*18 + 5)
        self.slow_rect.width += 20
        self.slow_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.slow_rect)
        self.screen.blit(slow_down, ((self.__dim[0])*20+30, self.__dim[1]*18))

        speed_up = button_font.render("Faster", True, (230,230,230))
        self.fast_rect = speed_up.get_rect()
        self.fast_rect.center = ((self.__dim[0])*20+258, self.__dim[1]*18 +5)
        self.fast_rect.width += 20
        self.fast_rect.height += 20
        pygame.draw.rect(self.screen, (20,20,20),  self.fast_rect)
        self.screen.blit(speed_up, ((self.__dim[0])*20+230, self.__dim[1]*18))

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.slow_rect.x <= mouse[0] <= self.slow_rect.x + self.slow_rect.width and self.slow_rect.y <= mouse[1] <= self.slow_rect.y + self.slow_rect.height and self.rate>2:
                        self.rate -= 2
                    elif self.fast_rect.x <= mouse[0] <= self.fast_rect.x + self.fast_rect.width and self.fast_rect.y <= mouse[1] <= self.fast_rect.y + self.slow_rect.height:
                        self.rate += 2
    
    def check_collisions(self):
        removals = pygame.sprite.groupcollide(self.__bluebots, self.__redbots, False, False)
        #print(removals)
        to_kill = set()
        for b, r_list in removals.items():
            #print(id(b))
            for r in r_list:
                #print(id(r))
                if b._Pirate__selfElixir > r._Pirate__selfElixir:
                    b._Pirate__selfElixir -= r._Pirate__selfElixir
                    self.__Pirates[r.rect.y//20][r.rect.x//20] = 2
                    to_kill.add(r)
                    self.__redbase._Base__TotalTeamElixir -= r._Pirate__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= r._Pirate__selfElixir
                    r._Pirate__selfElixir = 0
                elif b._Pirate__selfElixir < r._Pirate__selfElixir:
                    self.__Pirates[r.rect.y//20][r.rect.x//20] = 1
                    r._Pirate__selfElixir -= b._Pirate__selfElixir
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= b._Pirate__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Pirate__selfElixir
                    b.__Pirate_selfElixir = 0
                else:
                    self.__Pirates[r.rect.y//20][r.rect.x//20] = 0
                    to_kill.add(r)
                    to_kill.add(b)
                    self.__redbase._Base__TotalTeamElixir -= r._Pirate__selfElixir
                    self.__bluebase._Base__TotalTeamElixir -= b._Pirate__selfElixir
                    r._Pirate__selfElixir = 0
                    b._Pirate__selfElixir = 0
        redbase_collisions = pygame.sprite.spritecollide(self.__redbase, self.__bluebots, False)
        bluebase_collisions = pygame.sprite.spritecollide(self.__bluebase, self.__redbots, False)

        for b in redbase_collisions:
            if b._Pirate__selfElixir >= self.__redbase._Base__SelfElixir:
                b._Pirate__selfElixir -= self.__redbase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__redbase._Base__SelfElixir
                self.__redbase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Pirate__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Pirate__selfElixir
                self.__redbase._Base__SelfElixir -= b._Pirate__selfElixir
                b._Pirate__selfElixir = 0

        for b in bluebase_collisions:
            if b._Pirate__selfElixir >= self.__bluebase._Base__SelfElixir:
                b._Pirate__selfElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__redbase._Base__TotalTeamElixir -= self.__bluebase._Base__SelfElixir
                self.__bluebase._Base__SelfElixir = 0
            else:
                to_kill.add(b)
                self.__redbase._Base__TotalTeamElixir -= b._Pirate__selfElixir
                self.__bluebase._Base__TotalTeamElixir -= b._Pirate__selfElixir
                self.__bluebase._Base__SelfElixir -= b._Pirate__selfElixir
                b._Pirate__selfElixir = 0
                

        for a in to_kill:
                del self.__PositionToPirate[(a.rect.x//20, a.rect.y//20)][a]
                a.kill()
        return removals


    def create_map(self, img_path):
        """Take info about __collectibles and create the map"""
        # im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        # im = cv2.resize(im, self.__dim)
        # im = np.array(im)
        # # im = im - np.full((self.__dim[1],self.__dim[0]), 127)
        # # im = (im/127)*50

        im = np.zeros((self.__dim))

        size = self.__dim[0] * self.__dim[1]
        frac = size/16
        rum = []
        gunpowder = []
        wood = []

        while len(rum) < frac:
            x = random.randint(0, self.__dim[0]-1)
            y = random.randint(0, self.__dim[1]-1)
            if (x, y) not in rum and (x, y) not in self.island1 and (x, y) not in self.island2 and (x, y) not in self.island3:
                rum.append((x, y))
                im[x][y] = 1 # rum
            
        while len(gunpowder) < frac:
            x = random.randint(0, self.__dim[0]-1)
            y = random.randint(0, self.__dim[1]-1)
            if (x, y) not in gunpowder and (x, y) not in rum and (x, y) not in self.island1 and (x, y) not in self.island2 and (x, y) not in self.island3:
                gunpowder.append((x, y))
                im[x][y] = 2

        while len(wood) < frac:
            x = random.randint(0, self.__dim[0]-1)
            y = random.randint(0, self.__dim[1]-1)
            if (x, y) not in gunpowder and (x, y) not in rum and (x, y) not in wood and (x, y) not in self.island1 and (x, y) not in self.island2 and (x, y) not in self.island3:
                gunpowder.append((x, y))
                im[x][y] = 3    

        
        return im, rum, gunpowder, wood

    def replenish(self):
        for i in range(0,self.__dim[0]):
            for j in range(0,self.__dim[1]):
                # if self.__collectibles[i][j].initPoints > 1e-5:
                #     self.__collectibles[i][j].points = min(self.__collectibles[i][j].initPoints, self.__collectibles[i][j].points*1.3)
                if self.__collectibles[i][j].initPoints < -1e-5:
                    z = self.__collectibles[i][j].points*1.3
                    if z > 0:
                        z = 0
                    self.__collectibles[i][j].points = max(self.__collectibles[i][j].initPoints, z)
                self.__resources[j][i] = self.__collectibles[i][j].points
                self.__collectibles[i][j].setColor()


    def collect(self):
        
        for key in self.__PositionToPirate.keys():
            value = self.__PositionToPirate[key]
            if self.__Pirates[key[1]][key[0]] == 1 or self.__Pirates[key[1]][key[0]] == 2:
                V = self.__resources[key[1]][key[0]]/(2*len(value))
                for v in value:
                    v.addResource(V)
                self.__resources[key[1]][key[0]] /= 2
                self.__collectibles[key[0]][key[1]].points = self.__resources[key[1]][key[0]]
                self.__collectibles[key[0]][key[1]].setColor()

    def update_score(self):
        """Update scores in the scoreboard"""
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("Score Board", True, (255,255,255))
        titlerect = title.get_rect()
        titlerect.x = self.__dim[0]*20+100
        titlerect.y = 40
        self.screen.blit(title, titlerect)
        head_font = pygame.font.SysFont(None, 40)
        norm_font = pygame.font.SysFont(None, 32)
        blue_head = head_font.render(self.bluet, False, (130,130,255))
        self.screen.blit(blue_head, ((self.__dim[0])*20+ 30, self.__dim[1]*2.5))
        blue_total = norm_font.render("Total Elixir :" + str(round(self.__bluebase._Base__TotalTeamElixir,2)), False, (230,230,230))
        blue_self = norm_font.render("Self Elixir : " + str(round(self.__bluebase._Base__SelfElixir,2)), False, (230,230,230))
        blue_Pirates = norm_font.render("No. of Pirates: " +str(len(self.__bluebots)), False, (230,230,230))
        blue_virus = norm_font.render("Total Virus: " + str(round(self.__bluebase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(blue_total, ((self.__dim[0])*20+50, self.__dim[1]*5))
        self.screen.blit(blue_self, ((self.__dim[0])*20+50, self.__dim[1]*5 + 30))
        self.screen.blit(blue_Pirates, ((self.__dim[0])*20+50, self.__dim[1]*5 + 60))
        self.screen.blit(blue_virus, ((self.__dim[0])*20+50, self.__dim[1]*5 + 90))

        red_head = head_font.render(self.redt, False, (255,130,130))
        self.screen.blit(red_head, ((self.__dim[0])*20+30, self.__dim[1]*10))
        red_total = norm_font.render("Total Elixir :" + str(round(self.__redbase._Base__TotalTeamElixir,2)), False, (230,230,230))
        red_self = norm_font.render("Self Elixir : " + str(round(self.__redbase._Base__SelfElixir,2)), False, (230,230,230))
        red_Pirates = norm_font.render("No. of Pirates: " +str(len(self.__redbots)), False, (230,230,230))
        red_virus = norm_font.render("Total Virus: " + str(round(self.__redbase._Base__TotalVirus, 2)), False, (230,230,230))
        self.screen.blit(red_total, ((self.__dim[0])*20+50, self.__dim[1]*12))
        self.screen.blit(red_self, ((self.__dim[0])*20+50, self.__dim[1]*12 + 30))
        self.screen.blit(red_Pirates, ((self.__dim[0])*20+50, self.__dim[1]*12 + 60))
        self.screen.blit(red_virus, ((self.__dim[0])*20+50, self.__dim[1]*12 + 90))
        

    def game_over(self):
        """Check conditions of game over"""
        game_over_font = pygame.font.SysFont(None, 48)
        if self.__redbase._Base__SelfElixir <= 0.1:
            print( "Blue Wins")
            game_over = game_over_font.render(self.bluet+" Wins", True, (100,100,255), (230,230,230))
            self.screen.blit(game_over, ((self.__dim[0])*10,(self.__dim[0])*10))
            
            #time.sleep(5)
            while True:
                pygame.display.flip()
                self.check_events()
            
        elif self.__bluebase._Base__SelfElixir <= 0.1:
            print("Red Wins")
            game_over = game_over_font.render(self.redt+" Wins", True, (255,100,100), (230,230,230))
            self.screen.blit(game_over, ((self.__dim[0])*10,(self.__dim[0])*10))
            pygame.display.flip()
            #time.sleep(5)
            while True:
                pygame.display.flip()
                self.check_events()
            


# for i in range(0,len(TL)):
#     print(i,'.',TL[i])


# team1 = TL[int(input('Team 1 is ?'))]
# team2 = TL[int(input('Team 2 is ?'))]

# import shutil
# import os

# os.remove('scriptred.py')
# os.remove('scriptblue.py')

# shutil.copy('top16/'+team1,'scriptred.py')
# shutil.copy('top16/'+team2,'scriptblue.py')
import scriptblue
import scriptred

G = Game((40,40),(8,28),(31,28),'maps/test_img3.jpg', 'team1', 'team2')
G.run_game()

# import pickle
# import os
# import shutil
# import importlib

# def startmatch(team1,team2,map,dim,rpos,bpos):
#     os.remove('scriptred.py')
#     os.remove('scriptblue.py')
#     shutil.copy(name + '/'+team1,'scriptred.py')
#     shutil.copy(name+'/'+team2,'scriptblue.py')
#     try:
#         importlib.reload(scriptred)
#     except:
#         print('scriptred load failed!')
#     try:
#         importlib.reload(scriptblue)
#     except:
#         print('scriptblue load failed!')
#     g = Game(dim,rpos,bpos,map)
#     return g.run_game()


# name = 'challengers'
# f = open(name + 'teamnum.pic','rb')
# TN = pickle.load(f)

# g = open(name + 'status.pic','rb')
# S = pickle.load(g)
# g.close()

# si = S['starti']
# sj = S['startj']

# for i in range(si,21):
#     for j in range(i+1,21):
#         if i==si and j < sj:
#             continue
#         scorei = 0
#         scorej = 0
#         s = startmatch(TN[i],TN[j],'Ved.png',(40,40),(9,19),(29,19))
#         scorei += s
#         scorej += (1-s)
#         s = startmatch(TN[j],TN[i],'spiral.jpg',(40,40),(20,9),(20,29))
#         scorei += (1-s)
#         scorej += s
#         s = startmatch(TN[j],TN[i],'123.jpeg',(40,40),(9,9),(30,30))
#         scorei += (1-s)
#         scorej += s
#         S[i]+=scorei
#         S[j]+=scorej
#         S['startj'] += 1
#         if S['startj']==21:
#             S['startj'] = 0
#             S['starti']+=1
#         if S['starti']==21:
#             print('ALL GAMES COMPLETE!!!')
#         f = open(name + 'status.pic','wb')
#         pickle.dump(S,f)
#         f.close()
#         print('Match between',TN[i],'and',TN[j],'culminates!')





# name = 'league2'
# f = open(name + 'teamnum.pic','rb')
# TN = pickle.load(f)

# g = open(name + 'status.pic','rb')
# S = pickle.load(g)
# g.close()



# si = S['starti']
# sj = S['startj']



# for i in range(si,23):
#     for j in range(i+1,23):
#         if i==si and j < sj:
#             continue
#         scorei = 0
#         if i==2 or j ==2 or i==7 or j ==7 or i==12 or j ==12:
#             continue
#         scorej = 0
#         s = startmatch(TN[i],TN[j],'Ved.png',(40,40),(9,19),(29,19))
#         scorei += s
#         scorej += (1-s)
#         s = startmatch(TN[j],TN[i],'spiral.jpg',(40,40),(20,9),(20,29))
#         scorei += (1-s)
#         scorej += s
#         s = startmatch(TN[j],TN[i],'123.jpeg',(40,40),(9,9),(30,30))
#         scorei += (1-s)
#         scorej += s
#         S[i]+=scorei
#         S[j]+=scorej
#         S['startj'] += 1
#         if S['startj']==23:
#             S['startj'] = 0
#             S['starti']+=1
#         if S['starti']==23:
        #     print('ALL GAMES COMPLETE!!!')
        # f = open(name + 'status.pic','wb')
        # pickle.dump(S,f)
        # f.close()
        # print('Match between',TN[i],'and',TN[j],'culminates!')



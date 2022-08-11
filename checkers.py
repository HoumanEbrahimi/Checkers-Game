import pygame
from sys import exit
import os
import copy


SOUTH_EAST=[1,1]
SOUTH_WEST=[-1,1]

SOUTH_MOVES=[[1,1],[-1,1]]

NORTH_EAST=[1,-1]
NORTH_WEST=[-1,-1]

NORTH_MOVES=[[1,-1],[-1,-1]]

ROWS=8
COLS=8

pygame.init()

ScreenWidth=700
ScreenHeight=700

screen=pygame.display.set_mode((ScreenWidth,ScreenHeight))
blackorWhite=[]
clock = pygame.time.Clock()

red_image=pygame.image.load('red.png')
red_resize=pygame.transform.scale(red_image,(50,50))

white_image=pygame.image.load('white.png')
white_resize=pygame.transform.scale(white_image,(50,50))

 
grid=int(ScreenWidth/8)
Red=(220,20,60)
White=(255,255,255)

BLUE=(0,255,0)

board=[]
board2=[]

class Piece:
    def __init__(self,row,col,color):
        self.row=row
        self.col=col
        self.color=color
        self.direction=1

        if self.color==Red:
            self.direction-=1

        else:
            self.direction=1

        self.x=grid*self.col+grid//2
        self.y=grid*self.row+grid//2

    def draw(self):
        
        radius=10-5//2
        pygame.draw.circle(screen,self.color,(self.x,self.y),radius)
        pygame.display.update()

            
        
class Board:
    def __init__(self):
        self.board=[]
        self.boardGUI()
        self.createBoard()
        self.draw_pieces()
        
        self.selected_piece=None
        isWhite=1

    def initialize(self,x,y,is_white):

            grid_width=ScreenWidth/8
            grid_height=ScreenHeight/8
            x_coordinate=x*grid_width
            y_coordinate=y*grid_height

            return (x_coordinate,y_coordinate)
    

    def createBoard(self):
        for i in range(ROWS):
            self.board.append([])
            for j in range(COLS):
                if j%2==((i+1)%2):
                    if i<3:
                        self.board[i].append(Piece(i,j,Red))
                    elif i>4:
                        self.board[i].append(Piece(i,j,White))
                    else:
                        self.board[i].append(0)
                else:
                    self.board[i].append(0)

    def boardGUI(self):
        color=(255,255,255)
        grid=int (ScreenWidth/8)
        counter=0
        isWhite=1
        for i in range(8):
            for j in range(8):

                if(isWhite==1):
                    color=(255,255,255)
                else :
                    color=(0,0,0)
                    
                isWhite*=-1
                pygame.draw.rect(screen,color,pygame.Rect(i*grid,j*grid,grid,grid))
                pygame.display.update()
            isWhite*=-1

    def draw_pieces(self):
        self.boardGUI()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece!=0:
                    piece.draw()
                    print(piece.color,piece.x,piece.y)
                    
                



clock.tick(60)
s=Board()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        (x,y)=pygame.mouse.get_pos()
        
        if event.type==pygame.MOUSEBUTTONDOWN:
            print(x,y)
            
                


pygame.quit()


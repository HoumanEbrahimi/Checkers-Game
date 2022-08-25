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
black=(0,0,0)
blue=(0,0,255)


BLUE=(0,255,0)

board=[]
board2=[]


class Piece:
    def __init__(self,row,col,color):
        self.row=row
        self.col=col
        self.color=color
        self.direction=1
        self.radius=10-5//2


        self.shadow_color=blue
        self.black=black

        if self.color==Red:
            self.direction-=1

        else:
            self.direction=1

        self.x=grid*self.col+grid//2
        self.y=grid*self.row+grid//2

    def calc_pos(self):
        self.x=grid*self.col+grid//2
        self.y=grid*self.row+grid//2


    def draw(self):
        
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)
        pygame.display.update()

    def draw_directions_right(self,valid):
        if valid==True:
            pygame.draw.circle(screen,self.shadow_color,(self.x+grid,self.y+grid),self.radius)
        else:
            pygame.draw.circle(screen,self.black,(self.x+grid,self.y+grid),self.radius)
            pygame.draw.circle(screen,self.black,(self.x-grid,self.y+grid),self.radius)
        pygame.display.update()

    def draw_directions_left(self,valid):
        if valid==True:
            pygame.draw.circle(screen,self.shadow_color,(self.x-grid,self.y+grid),self.radius)
        else:
            pygame.draw.circle(screen,self.black,(self.x+grid,self.y+grid),self.radius)
            pygame.draw.circle(screen,self.black,(self.x-grid,self.y+grid),self.radius)
        pygame.display.update()

    def both_directions(self,valid):

            
        if valid==True:
            pygame.draw.circle(screen,self.shadow_color,(self.x+grid,self.y+grid),self.radius)
            pygame.draw.circle(screen,self.shadow_color,(self.x-grid,self.y+grid),self.radius)
        else:
            pygame.draw.circle(screen,self.black,(self.x+grid,self.y+grid),self.radius)
            pygame.draw.circle(screen,self.black,(self.x-grid,self.y+grid),self.radius)

        pygame.display.update()

        
    def move(self,row,col):
        self.row=row
        self.col=col
        self.calc_pos()
        
class Board:
    def __init__(self):
        self.board=[]
        self.createBoard()
        self.selected_piece=None
        isWhite=1


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

                    
    def valid_moves(self,piece,rows,cols,start):
        valid=0

        validMoves=[]
        try:

            if start==1:
                valid=True
            
            elif start==-1:
                valid=False

            if self.board[rows+1][cols+1]==0 and self.board[rows+1][cols-1]==0:
                piece.both_directions(valid)
                validMoves.append((rows+1,cols+1))
                validMoves.append((rows+1,cols-1))

                print(validMoves[0],validMoves[1])
                

            elif self.board[rows+1][cols+1]==0 and self.board[rows+1][cols-1]!=0:
                piece.draw_directions_right(valid)
                validMoves.append((rows+1,cols+1))
            
            elif self.board[rows+1][cols+1]!=0 and self.board[rows+1][cols-1]==0:
                piece.draw_directions_left(valid)
                validMoves.append((rows+1,cols+1))

        except:
            rows*100+100>=ScreenHeight or cols*100+100>=ScreenWidth

            if cols*100+100>=ScreenWidth:
                piece.draw_directions_left(valid)

                validMoves.append((rows+1,cols+1))
        return validMoves

    
    def move(self,piece,rows,cols):
        moved=False

        try:
            
            self.board[piece.row][piece.col], self.board[rows][cols] = self.board[rows][cols], self.board[piece.row][piece.col]

            piece.move(rows, cols)
            moved=True

        except:
            self.get_piece(rows,cols)!=0 

        self.draw_pieces()

        return moved



    def selectPlace(self,piece,x,y):
        self.move(piece,x,y)
            

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


    def get_piece(self,row,col):
        if self.board[row][col]!=None:
            return self.board[row][col]

    
    def draw_pieces(self):
        self.boardGUI()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece!=0:
                    piece.draw()


class Game:
    def __init__(self):
        self.selected=None
        self.board=Board()
        self.turn=Red
        self.valid_moves={}
        
    def update(self):
        self.board.draw()
        pygame.display.update()

    def reset(self):
        self.selected=None

    def select(self,row,col):
        if self.selected:
            result=self.move(row,col)
            if not result:
                self.selected=None
        else:
            piece=self.board.get_piece(row,col)
            if piece!=0 and piece.color==self.turn:
                self.selected=piece
                self.valid_moves=self.board.valid_moves(piece,row,col,True)
                print(self.valid_moves)
                return True
            return False
        

    def move(self,row,col):
        piece=self.board.get_piece(row,col)
        if self.selected and piece==0 and (row,col) in self.valid_moves:
            self.board.move(self.selected,row,col)
         
        else:
            return False
        return True

    def change_turn(self):
        if self.turn==Red:
            self.turn=White
        else:
            self.turn=Red
        
         
        
clock.tick(60)
board=Board()
board.boardGUI()
board.draw_pieces()
game=Game()


clicked=-1

piece=board.get_piece(0,0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()

        (x,y)=pygame.mouse.get_pos()
        (rel1,rel2)=0,0

        if event.type==pygame.MOUSEBUTTONDOWN:
            clicked*=-1
            piece=board.get_piece(y//grid,x//grid)
            first,second=y//grid,x//grid
            #board.valid_moves(piece,first,second,clicked)
            game.select(first,second)
            game.move(first,second)

pygame.quit()

  


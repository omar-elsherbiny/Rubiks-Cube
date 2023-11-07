#Imports
import pygame as pyg
from sys import exit as syexit
from math import sin, cos, radians
from MatrixObj import Matrix, Basis
from CubeObjs import *

pyg.init()

#Globals
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BG_COLOR=(20,20,20)
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pyg.font.Font("freesansbold.ttf", 20)

def draw_text(text,x,y,c):
    txt=FONT.render(text,True,c)
    SCREEN.blit(txt,(x,y))

#Main
def main():
    clock = pyg.time.Clock()

    Ax,Ay,Az=config['init_angles']

    pieces=[
        Piece(Matrix('3x1',[[cube_scale],[cube_scale],[cube_scale]]),'wgrboy','urf'),
        Piece(Matrix('3x1',[[0],[cube_scale],[cube_scale]]),'wgrboy','umf'),
        Piece(Matrix('3x1',[[-cube_scale],[cube_scale],[cube_scale]]),'wgrboy','ulf'),
        Piece(Matrix('3x1',[[cube_scale],[cube_scale],[0]]),'wgrboy','urs'),
        Piece(Matrix('3x1',[[0],[cube_scale],[0]]),'wgrboy','ums'),
        Piece(Matrix('3x1',[[-cube_scale],[cube_scale],[0]]),'wgrboy','uls'),
        Piece(Matrix('3x1',[[cube_scale],[cube_scale],[-cube_scale]]),'wgrboy','urb'),
        Piece(Matrix('3x1',[[0],[cube_scale],[-cube_scale]]),'wgrboy','umb'),
        Piece(Matrix('3x1',[[-cube_scale],[cube_scale],[-cube_scale]]),'wgrboy','ulb'),
        Piece(Matrix('3x1',[[cube_scale],[0],[cube_scale]]),'wgrboy','erf'),
        Piece(Matrix('3x1',[[0],[0],[cube_scale]]),'wgrboy','emf'),
        Piece(Matrix('3x1',[[-cube_scale],[0],[cube_scale]]),'wgrboy','elf'),
        Piece(Matrix('3x1',[[cube_scale],[0],[0]]),'wgrboy','ers'),
        Piece(Matrix('3x1',[[-cube_scale],[0],[0]]),'wgrboy','els'),
        Piece(Matrix('3x1',[[cube_scale],[0],[-cube_scale]]),'wgrboy','erb'),
        Piece(Matrix('3x1',[[0],[0],[-cube_scale]]),'wgrboy','emb'),
        Piece(Matrix('3x1',[[-cube_scale],[0],[-cube_scale]]),'wgrboy','elb'),
        Piece(Matrix('3x1',[[cube_scale],[-cube_scale],[cube_scale]]),'wgrboy','drf'),
        Piece(Matrix('3x1',[[0],[-cube_scale],[cube_scale]]),'wgrboy','dmf'),
        Piece(Matrix('3x1',[[-cube_scale],[-cube_scale],[cube_scale]]),'wgrboy','dlf'),
        Piece(Matrix('3x1',[[cube_scale],[-cube_scale],[0]]),'wgrboy','drs'),
        Piece(Matrix('3x1',[[0],[-cube_scale],[0]]),'wgrboy','dms'),
        Piece(Matrix('3x1',[[-cube_scale],[-cube_scale],[0]]),'wgrboy','dls'),
        Piece(Matrix('3x1',[[cube_scale],[-cube_scale],[-cube_scale]]),'wgrboy','drb'),
        Piece(Matrix('3x1',[[0],[-cube_scale],[-cube_scale]]),'wgrboy','dmb'),
        Piece(Matrix('3x1',[[-cube_scale],[-cube_scale],[-cube_scale]]),'wgrboy','dlb')
    ]

    #MAIN LOOP
    run = True
    while run:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                syexit()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    pass
        
        #Ay += 1
        rotX=Matrix('3x3',[[1,0,0],[0,cos(radians(Ax)),-sin(radians(Ax))],[0,sin(radians(Ax)),cos(radians(Ax))]])
        rotY=Matrix('3x3',[[cos(radians(Ay)),0,-sin(radians(Ay))],[0,1,0],[sin(radians(Ay)),0,cos(radians(Ay))]])
        rotZ=Matrix('3x3',[[cos(radians(Az)),-sin(radians(Az)),0],[sin(radians(Az)),cos(radians(Az)),0],[0,0,1]])
        rot=rotX@rotY@rotZ

        SCREEN.fill(BG_COLOR)

        Basis.draw_basis(Basis,screen=SCREEN,matrix=rot,scale=150)
        
        for piece in sorted(pieces,key=lambda x:(rot@x.center).matrix[2][0]):
            piece.draw_piece(SCREEN,(0,100,200),rot)
        for piece in sorted(pieces,key=lambda x:(rot@x.center).matrix[2][0]):
            draw_text(piece.grps,(rot@piece.center).matrix[0][0]+250,-(rot@piece.center).matrix[1][0]+250,(10,10,10))


        clock.tick(60)
        pyg.display.set_caption(f'Rendering--{int(clock.get_fps())}')
        pyg.display.update()

if __name__=='__main__':
    main()
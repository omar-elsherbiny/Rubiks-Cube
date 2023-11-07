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
    grps=config['groups']
    ops=config['operations']
    current_operation=None

    pieces=[
        Piece(Matrix('3x1',[[cube_scale],[cube_scale],[cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[0],[cube_scale],[cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[-cube_scale],[cube_scale],[cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[cube_scale],[cube_scale],[0]]),'wgrboy'),
        Piece(Matrix('3x1',[[0],[cube_scale],[0]]),'wgrboy'),
        Piece(Matrix('3x1',[[-cube_scale],[cube_scale],[0]]),'wgrboy'),
        Piece(Matrix('3x1',[[cube_scale],[cube_scale],[-cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[0],[cube_scale],[-cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[-cube_scale],[cube_scale],[-cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[cube_scale],[0],[cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[0],[0],[cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[-cube_scale],[0],[cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[cube_scale],[0],[0]]),'wgrboy'),
        Piece(Matrix('3x1',[[-cube_scale],[0],[0]]),'wgrboy'),
        Piece(Matrix('3x1',[[cube_scale],[0],[-cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[0],[0],[-cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[-cube_scale],[0],[-cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[cube_scale],[-cube_scale],[cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[0],[-cube_scale],[cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[-cube_scale],[-cube_scale],[cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[cube_scale],[-cube_scale],[0]]),'wgrboy'),
        Piece(Matrix('3x1',[[0],[-cube_scale],[0]]),'wgrboy'),
        Piece(Matrix('3x1',[[-cube_scale],[-cube_scale],[0]]),'wgrboy'),
        Piece(Matrix('3x1',[[cube_scale],[-cube_scale],[-cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[0],[-cube_scale],[-cube_scale]]),'wgrboy'),
        Piece(Matrix('3x1',[[-cube_scale],[-cube_scale],[-cube_scale]]),'wgrboy')
    ]

    def sort_pieces():
        pieces.sort(key=lambda x:(x.get_personal_matrix()@x.center).matrix[1][0],reverse=True)
        pieces[:9]=sorted(pieces[:9],key=lambda x:(x.get_personal_matrix()@x.center).matrix[2][0],reverse=True)
        pieces[9:17]=sorted(pieces[9:17],key=lambda x:(x.get_personal_matrix()@x.center).matrix[2][0],reverse=True)
        pieces[17:]=sorted(pieces[17:],key=lambda x:(x.get_personal_matrix()@x.center).matrix[2][0],reverse=True)
        for i in range(4):
            pieces[i*3:i*3+3]=sorted(pieces[i*3:i*3+3],key=lambda x:(x.get_personal_matrix()@x.center).matrix[0][0],reverse=True)
        pieces[12:14]=sorted(pieces[12:14],key=lambda x:(x.get_personal_matrix()@x.center).matrix[0][0],reverse=True)
        for i in range(4):
            pieces[i*3+14:i*3+17]=sorted(pieces[i*3+14:i*3+17],key=lambda x:(x.get_personal_matrix()@x.center).matrix[0][0],reverse=True)

    def do_operation(operation,reverse=False):
        for i in range(26):
            if operation in grps[i]:
                if reverse:
                    pieces[i].angs[ops[operation]['ax']]-=90 * ops[operation]['s']
                else:
                    pieces[i].angs[ops[operation]['ax']]+=90 * ops[operation]['s']
                pieces[i].angs[ops[operation]['ax']]=pieces[i].angs[ops[operation]['ax']]%360
        sort_pieces()

    #MAIN LOOP
    run = True
    while run:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                syexit()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:      
                    Ay+=30
                elif event.button == 3:
                    do_operation('r')

        rotX=Matrix('3x3',[[1,0,0],[0,cos(radians(Ax)),-sin(radians(Ax))],[0,sin(radians(Ax)),cos(radians(Ax))]])
        rotY=Matrix('3x3',[[cos(radians(Ay)),0,-sin(radians(Ay))],[0,1,0],[sin(radians(Ay)),0,cos(radians(Ay))]])
        rotZ=Matrix('3x3',[[cos(radians(Az)),-sin(radians(Az)),0],[sin(radians(Az)),cos(radians(Az)),0],[0,0,1]])
        rot=rotX@rotY@rotZ

        SCREEN.fill(BG_COLOR)
        
        for piece in sorted(pieces,key=lambda x:(x.get_personal_matrix([Ax,Ay,Az])@x.center).matrix[2][0]):
            piece.draw_piece(SCREEN,(0,100,200),piece.get_personal_matrix([Ax,Ay,Az]))

        Basis.draw_basis(Basis,screen=SCREEN,matrix=rot,scale=150)

        clock.tick(60)
        pyg.display.set_caption(f'Rendering--{int(clock.get_fps())}')
        pyg.display.update()

if __name__=='__main__':
    main()
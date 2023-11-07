#Imports
import pygame as pyg
from sys import exit as syexit
from random import choice
from math import sin, cos, radians
from MatrixObj import Matrix, identity3, Basis
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
    current_operation=0
    operation_progress=0

    pieces=[
        Piece(Matrix('3x1',[[cube_scale],[cube_scale],[cube_scale]]),'wgr000'),
        Piece(Matrix('3x1',[[0],[cube_scale],[cube_scale]]),'wg0000'),
        Piece(Matrix('3x1',[[-cube_scale],[cube_scale],[cube_scale]]),'wg00o0'),
        Piece(Matrix('3x1',[[cube_scale],[cube_scale],[0]]),'w0r000'),
        Piece(Matrix('3x1',[[0],[cube_scale],[0]]),'w00000'),
        Piece(Matrix('3x1',[[-cube_scale],[cube_scale],[0]]),'w000o0'),
        Piece(Matrix('3x1',[[cube_scale],[cube_scale],[-cube_scale]]),'w0rb00'),
        Piece(Matrix('3x1',[[0],[cube_scale],[-cube_scale]]),'w00b00'),
        Piece(Matrix('3x1',[[-cube_scale],[cube_scale],[-cube_scale]]),'w00bo0'),
        Piece(Matrix('3x1',[[cube_scale],[0],[cube_scale]]),'0gr000'),
        Piece(Matrix('3x1',[[0],[0],[cube_scale]]),'0g0000'),
        Piece(Matrix('3x1',[[-cube_scale],[0],[cube_scale]]),'0g00o0'),
        Piece(Matrix('3x1',[[cube_scale],[0],[0]]),'00r000'),
        Piece(Matrix('3x1',[[-cube_scale],[0],[0]]),'0000o0'),
        Piece(Matrix('3x1',[[cube_scale],[0],[-cube_scale]]),'00rb00'),
        Piece(Matrix('3x1',[[0],[0],[-cube_scale]]),'000b00'),
        Piece(Matrix('3x1',[[-cube_scale],[0],[-cube_scale]]),'000bo0'),
        Piece(Matrix('3x1',[[cube_scale],[-cube_scale],[cube_scale]]),'0gr00y'),
        Piece(Matrix('3x1',[[0],[-cube_scale],[cube_scale]]),'0g000y'),
        Piece(Matrix('3x1',[[-cube_scale],[-cube_scale],[cube_scale]]),'0g00oy'),
        Piece(Matrix('3x1',[[cube_scale],[-cube_scale],[0]]),'00r00y'),
        Piece(Matrix('3x1',[[0],[-cube_scale],[0]]),'00000y'),
        Piece(Matrix('3x1',[[-cube_scale],[-cube_scale],[0]]),'0000oy'),
        Piece(Matrix('3x1',[[cube_scale],[-cube_scale],[-cube_scale]]),'00rb0y'),
        Piece(Matrix('3x1',[[0],[-cube_scale],[-cube_scale]]),'000b0y'),
        Piece(Matrix('3x1',[[-cube_scale],[-cube_scale],[-cube_scale]]),'000boy')
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

    #MAIN LOOP
    run = True
    while run:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                syexit()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if current_operation == 0:
                        current_operation=[choice(list(ops.keys())),choice([0,1])]

        if current_operation != 0:
            for i in range(26):
                if current_operation[0] in grps[i]:
                    if current_operation[1]:
                        pieces[i].add=pieces[i].get_step(ops[current_operation[0]]['ax'],-90*ops[current_operation[0]]['s']*operation_progress/100)
                    else:
                        pieces[i].add=pieces[i].get_step(ops[current_operation[0]]['ax'],90*ops[current_operation[0]]['s']*operation_progress/100)
            operation_progress+=3
        if operation_progress >= 100:
            for i in range(26):
                if current_operation[0] in grps[i]:
                    pieces[i].add=identity3
                    if current_operation[1]:
                        pieces[i].steps.append(pieces[i].get_step(ops[current_operation[0]]['ax'],-90*ops[current_operation[0]]['s']))
                    else:
                        pieces[i].steps.append(pieces[i].get_step(ops[current_operation[0]]['ax'],90*ops[current_operation[0]]['s']))
            sort_pieces()
            operation_progress=0
            current_operation=0

        rotX=Matrix('3x3',[[1,0,0],[0,cos(radians(Ax)),-sin(radians(Ax))],[0,sin(radians(Ax)),cos(radians(Ax))]])
        rotY=Matrix('3x3',[[cos(radians(Ay)),0,-sin(radians(Ay))],[0,1,0],[sin(radians(Ay)),0,cos(radians(Ay))]])
        rotZ=Matrix('3x3',[[cos(radians(Az)),-sin(radians(Az)),0],[sin(radians(Az)),cos(radians(Az)),0],[0,0,1]])
        rot=rotX@rotY@rotZ

        SCREEN.fill(BG_COLOR)
        
        #pyg.draw.polygon(SCREEN,(10,10,10),[(196,22),(49,100),(49,408),(302,477),(450,353),(450,95)])

        for piece in sorted(pieces,key=lambda x:(x.get_personal_matrix(rot)@x.center).matrix[2][0]):
            piece.draw_piece(SCREEN,(0,100,200),piece.get_personal_matrix(rot))

        #Basis.draw_basis(Basis,screen=SCREEN,matrix=rot,scale=150)

        clock.tick(60)
        pyg.display.set_caption(f'Rendering--{int(clock.get_fps())}')
        pyg.display.update()

if __name__=='__main__':
    main()
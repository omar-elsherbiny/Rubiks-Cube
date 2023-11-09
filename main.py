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

def get_sign(a,b):
    if a<0 and b>=0:
        return 1
    elif a>=0 and b>=0:
        return -1
    elif a<0 and b<0:
        return -1
    elif a>=0 and b<0:
        return 1

#Main
def main():
    clock = pyg.time.Clock()

    Ax,Ay,Az=config['init_angles']
    grps=config['groups']
    ops=config['operations']
    current_operation=0
    operation_progress=0
    panning=False
    coords=(0,0)
    prev_coords=(0,0)
    drag_vector=(0,0)
    dragging=False
    f_selec=False
    f_selec_c=''

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

    def get_closest_piece(crds):
        dists=[dist_3d_mp(piece.get_personal_matrix(rot)@piece.center, (crds[0]-250,-crds[1]+250,max(0,(piece.get_personal_matrix(rot)@piece.center)[2][0]))) for piece in pieces]
        return dists.index(min(dists))

    def get_operation(f,l):
        opl=[[grps[f][i],i] for i in range(3) if grps[f][i]==grps[l][i]]
        if len(opl)==0: return 0
        operation=opl[0][0]
        if opl[0][1]==0:
            rev=get_sign((pieces[l].center.matrix[0][0]-pieces[f].center.matrix[0][0]),(pieces[l].center.matrix[2][0]+pieces[f].center.matrix[2][0]))
        elif opl[0][1]==1:
            rev=get_sign((pieces[l].center.matrix[1][0]-pieces[f].center.matrix[1][0]),(pieces[l].center.matrix[2][0]+pieces[f].center.matrix[2][0]))
        elif opl[0][1]==2:
            rev=get_sign((pieces[l].center.matrix[0][0]-pieces[f].center.matrix[0][0]),(pieces[l].center.matrix[1][0]+pieces[f].center.matrix[1][0]))
        print([operation,rev])
        return [operation,abs(rev-1)]

    #MAIN LOOP
    run = True
    while run:
        coords=pyg.mouse.get_pos()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                syexit()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging=True
                    f_selec=get_closest_piece(event.pos)
                    f_selec_c=pieces[f_selec].colors
                    pieces[f_selec].set_side_colors('rrrrrr')
                if event.button == 3:
                    panning=True
                    prev_coords=event.pos
                if event.button == 2 and current_operation == 0: current_operation=[choice(list(ops.keys())),choice([0,1])]
            elif event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    if current_operation == 0:
                        dragging=False
                        pieces[f_selec].set_side_colors(f_selec_c)
                        l_selec=get_closest_piece(event.pos)
                        current_operation=get_operation(f_selec,l_selec)

                if event.button == 3:
                    panning=False
                    Ax+=drag_vector[1]
                    Ay-=drag_vector[0]

        if dragging:
            tmp_i=get_closest_piece(coords)
            tmp_c=pieces[tmp_i].colors
            pieces[tmp_i].set_side_colors('bbbbbb')
            
        if panning:
            drag_vector=[max(-360,min(360,(coords[0]-prev_coords[0])/2)),max(-360,min(360,(coords[1]-prev_coords[1])/2))]
            Ax=Ax%360
            if Ax>90 and Ax<270: drag_vector[0]*=-1
        else:
            drag_vector=(0,0)

        if current_operation != 0:
            for i in range(26):
                if current_operation[0] in grps[i]:
                    if current_operation[1]:
                        pieces[i].add=pieces[i].get_step(ops[current_operation[0]]['ax'],-90*ops[current_operation[0]]['s']*operation_progress/100)
                    else:
                        pieces[i].add=pieces[i].get_step(ops[current_operation[0]]['ax'],90*ops[current_operation[0]]['s']*operation_progress/100)
            operation_progress+=4
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

        rotX=Matrix('3x3',[[1,0,0],[0,cos(radians(Ax+drag_vector[1])),-sin(radians(Ax+drag_vector[1]))],[0,sin(radians(Ax+drag_vector[1])),cos(radians(Ax+drag_vector[1]))]])
        rotY=Matrix('3x3',[[cos(radians(Ay-drag_vector[0])),0,-sin(radians(Ay-drag_vector[0]))],[0,1,0],[sin(radians(Ay-drag_vector[0])),0,cos(radians(Ay-drag_vector[0]))]])
        rotZ=Matrix('3x3',[[cos(radians(Az)),-sin(radians(Az)),0],[sin(radians(Az)),cos(radians(Az)),0],[0,0,1]])
        rot=rotX@rotY@rotZ

        SCREEN.fill(BG_COLOR)
        
        #pyg.draw.polygon(SCREEN,(10,10,10),[(196,22),(49,100),(49,408),(302,477),(450,353),(450,95)])

        for piece in sorted(pieces,key=lambda x:(x.get_personal_matrix(rot)@x.center).matrix[2][0]):
            piece.draw_piece(SCREEN,(0,100,200),piece.get_personal_matrix(rot))

        Basis.draw_basis(Basis,SCREEN,rot,30,450,450)
        pyg.draw.circle(SCREEN,(220,220,220),(450,450),35,2)

        if dragging:
            pieces[tmp_i].set_side_colors(tmp_c)

        clock.tick(60)
        pyg.display.set_caption(f'Rendering--{int(clock.get_fps())}')
        pyg.display.update()

if __name__=='__main__':
    main()
#Imports
import pygame as pyg
from sys import exit as syexit
from random import choice, randint
from math import sin, cos, radians
from MatrixObj import Matrix, identity3, Basis
from CubeObjs import *

pyg.init()

#Globals
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BG_COLOR=(20,20,20)
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pyg.font.Font(resource_path("Comfortaa-Bold.ttf"), 20)
FONT2 = pyg.font.Font(resource_path("Comfortaa-Bold.ttf"), 13)

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
    is_acw=True
    cw_outline=pyg.Rect(15,450,57,30)
    correct=False

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
        pieces.sort(key=lambda x:(x.personal_matrix@x.center).matrix[1][0],reverse=True)
        pieces[:9]=sorted(pieces[:9],key=lambda x:(x.personal_matrix@x.center).matrix[2][0],reverse=True)
        pieces[9:17]=sorted(pieces[9:17],key=lambda x:(x.personal_matrix@x.center).matrix[2][0],reverse=True)
        pieces[17:]=sorted(pieces[17:],key=lambda x:(x.personal_matrix@x.center).matrix[2][0],reverse=True)
        for i in range(4):
            pieces[i*3:i*3+3]=sorted(pieces[i*3:i*3+3],key=lambda x:(x.personal_matrix@x.center).matrix[0][0],reverse=True)
        pieces[12:14]=sorted(pieces[12:14],key=lambda x:(x.personal_matrix@x.center).matrix[0][0],reverse=True)
        for i in range(4):
            pieces[i*3+14:i*3+17]=sorted(pieces[i*3+14:i*3+17],key=lambda x:(x.personal_matrix@x.center).matrix[0][0],reverse=True)

    def get_closest_piece(crds):
        dists=[dist_3d_mp(rot@piece.get_personal_matrix()@piece.center, (crds[0]-250,-crds[1]+250,max(0,(rot@piece.get_personal_matrix()@piece.center)[2][0]))) for piece in pieces]
        return dists.index(min(dists))

    def get_operation(f,l):
        opl=[grps[f][i] for i in range(3) if grps[f][i]==grps[l][i]]
        if len(opl)==0: return 0
        return [opl[0],not is_acw if opl[0]=='u' or opl[0]=='d' else is_acw]
    
    def update_matricies():
        for p in pieces:
            p.personal_matrix=p.get_personal_matrix()

    if scramble['set_scramble']:
        scr=scramble['scramble'].lower().split(' ')
        if scr[0]!= '':
            for op in scr:
                for i in range(26):
                    if op[0] in grps[i]:
                        if '`'in op:
                            pieces[i].steps.append(pieces[i].get_step(ops[op[0]]['ax'],-90*ops[op[0]]['s']))
                        else:
                            pieces[i].steps.append(pieces[i].get_step(ops[op[0]]['ax'],90*ops[op[0]]['s']))
                update_matricies()
                sort_pieces()
        shuffle_str=scramble['scramble'].upper()
    else:
        n_rando=randint(15,32)
        rando=[[choice(list(ops.keys())[:6]),choice([0,1])] for i in range(n_rando)]
        for r in rando:
            for i in range(26):
                if r[0] in grps[i]:
                    if r[1]:
                        pieces[i].steps.append(pieces[i].get_step(ops[r[0]]['ax'],-90*ops[r[0]]['s']))
                    else:
                        pieces[i].steps.append(pieces[i].get_step(ops[r[0]]['ax'],90*ops[r[0]]['s']))
            update_matricies()
            sort_pieces()
        shuffle_str=' '.join([o[0].upper()+'`' if o[1] else o[0].upper() for o in rando])

    txt_renders=[FONT2.render(shuffle_str,True,(80, 130, 160)),FONT.render('ACW',True,(255,145,145)),
                 FONT.render('CW',True,(145,255,145)),FONT.render('Solved!',True,(145,255,145))]
    #MAIN LOOP
    run = True
    while run:
        coords=pyg.mouse.get_pos()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                syexit()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1 and event.pos[1]>29 and current_operation == 0:
                    dragging=True
                    f_selec=get_closest_piece(event.pos)
                    f_selec_c=pieces[f_selec].colors
                    pieces[f_selec].set_side_colors('rrrrrr')
                if event.button == 3:
                    panning=True
                    prev_coords=event.pos
                if event.button == 4: is_acw=True
                if event.button == 5: is_acw=False
                if event.button == 2 and current_operation == 0: current_operation=[choice(list(ops.keys())),choice([0,1])]
            elif event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    if current_operation == 0 and dragging:
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
            tmp_o=get_operation(f_selec,tmp_i)
            tmp_c=[0 for i in range(26)]
            tmp_c[tmp_i]=pieces[tmp_i].colors
            if tmp_o != 0:
                for i in range(26):
                    if tmp_o[0] in grps[i]:
                        tmp_c[i]=pieces[i].colors
                        pieces[i].set_side_colors('bbbbbb')
            pieces[tmp_i].set_side_colors('gggggg')
            pieces[f_selec].set_side_colors('rrrrrr')
            
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
            update_matricies()
            operation_progress+=5
        if operation_progress >= 100:
            for i in range(26):
                if current_operation[0] in grps[i]:
                    pieces[i].add=identity3
                    if current_operation[1]:
                        pieces[i].steps.append(pieces[i].get_step(ops[current_operation[0]]['ax'],-90*ops[current_operation[0]]['s']))
                    else:
                        pieces[i].steps.append(pieces[i].get_step(ops[current_operation[0]]['ax'],90*ops[current_operation[0]]['s']))
            update_matricies()
            sort_pieces()
            operation_progress=0
            current_operation=0
            #check
            correct=True
            for i in range(26):
                res=identity3
                for j in range(len(pieces[i].steps)):
                    res @= pieces[i].steps[j]
                if res.matrix != identity3.matrix:
                    correct = False

        rotX=Matrix('3x3',[[1,0,0],[0,cos(radians(Ax+drag_vector[1])),-sin(radians(Ax+drag_vector[1]))],[0,sin(radians(Ax+drag_vector[1])),cos(radians(Ax+drag_vector[1]))]])
        rotY=Matrix('3x3',[[cos(radians(Ay-drag_vector[0])),0,-sin(radians(Ay-drag_vector[0]))],[0,1,0],[sin(radians(Ay-drag_vector[0])),0,cos(radians(Ay-drag_vector[0]))]])
        rotZ=Matrix('3x3',[[cos(radians(Az)),-sin(radians(Az)),0],[sin(radians(Az)),cos(radians(Az)),0],[0,0,1]])
        rot=rotX@rotY@rotZ

        SCREEN.fill(BG_COLOR)

        for piece in sorted(pieces,key=lambda x:(rot@x.personal_matrix@x.center).matrix[2][0]):
            piece.draw_piece(SCREEN,(0,100,200),rot@piece.personal_matrix)

        Basis.draw_basis(Basis,SCREEN,rot,30,450,450)
        pyg.draw.circle(SCREEN,(220,220,220),(450,450),35,2)

        pyg.draw.rect(SCREEN,(220,220,220),cw_outline,2)
        if is_acw:
            SCREEN.blit(txt_renders[1],(20,456))
        else:
            SCREEN.blit(txt_renders[2],(26,456))

        SCREEN.blit(txt_renders[0],(15,10))

        if correct: SCREEN.blit(txt_renders[3],(210,456))

        if dragging:
            if tmp_o != 0:
                for i in range(26):
                    if tmp_o[0] in grps[i]:
                        pieces[i].set_side_colors(tmp_c[i])
            pieces[tmp_i].set_side_colors(tmp_c[tmp_i])

        clock.tick(60)
        pyg.display.set_caption(f'Rubiks Cube--{int(clock.get_fps())}')
        pyg.display.update()

if __name__=='__main__':
    main()
from math import sqrt
from MatrixObj import Matrix
from pygame import draw

side_colors={'w':(220, 220, 220),
             'r':(255, 40, 40),
             'b':(100, 185, 225),
             'o':(255, 165, 25),
             'g':(110, 235, 90),
             'y':(255, 240, 60)}

sides_pnt_i = [[4,0,1,5],
               [5,1,3,7],
               [0,1,3,2],
               [0,2,6,4],
               [4,5,7,6],
               [2,3,7,6]]

cube_scale=100
piece_scale=30

def dist_3d_m(pnt1,pnt2):
    return sqrt((pnt1.matrix[0][0]-pnt2.matrix[0][0])**2+(pnt1.matrix[1][0]-pnt2.matrix[1][0])**2+(pnt1.matrix[2][0]-pnt2.matrix[2][0])**2)
def dist_3d_p(pnt1,pnt2):
    return sqrt((pnt1[0]-pnt2[0])**2+(pnt1[1]-pnt2[1])**2+(pnt1[2]-pnt2[2])**2)
def dist_3d_mp(pntm,pntp):
    return sqrt((pntm.matrix[0][0]-pntp[0])**2+(pntm.matrix[1][0]-pntp[1])**2+(pntm.matrix[2][0]-pntp[2])**2)

def get_color(dist,color):
    #c=71000/(dist+279)
    l=50/(dist+50)
    return (l*color[0],l*color[1],l*color[2])

class Piece:
    def __init__(self,center,sides):
        self.center=center
        self.sides=sides
        self.points=[]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    self.points.append(Matrix('3x1',[[center.matrix[0][0]+piece_scale*(-2*i+1)],[center.matrix[1][0]+piece_scale*(-2*j+1)],[center.matrix[2][0]+piece_scale*(-2*k+1)]]))

    def draw_piece(self,screen,light_center,matrix):
        d=dist_3d_mp(matrix@self.center,light_center)
        c=get_color(d,side_colors['r'])
        rp=[]
        for point in self.points:
            p=matrix@point
            draw.circle(screen,c,(int(p.matrix[0][0]+250),int(-p.matrix[1][0]+250)),5)
            rp.append((int(p.matrix[0][0]+250),int(-p.matrix[1][0]+250)))
        for s in range(6):
            if self.sides[s] != 0:
                draw.polygon(screen,get_color(d,side_colors[self.sides[s]]),[rp[i] for i in sides_pnt_i[s]])

if __name__=='__main__':
    p=Piece((0,0,0),0)

#   order
#top
#front
#right
#behind
#left
#bottom

# 1 1 1
# 1 1 -1
# 1 -1 1
# 1 -1 -1
# -1 1 1
# -1 1 -1
# -1 -1 1
# -1 -1 -1
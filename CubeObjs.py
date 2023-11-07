from math import sqrt
from MatrixObj import Matrix
from pygame import draw

side_colors={'w':(220, 220, 220),
             'g':(110, 235, 90),
             'r':(255, 40, 40),
             'b':(100, 185, 225),
             'o':(255, 165, 25),
             'y':(255, 240, 60)}

sides_pnt_index = [[4,0,1,5],
                   [0,2,6,4],
                   [0,1,3,2],
                   [5,1,3,7],
                   [4,5,7,6],
                   [2,3,7,6]]

sides_relative_coords=[[0,1,0],
                       [0,0,1],
                       [1,0,0],
                       [0,0,-1],
                       [-1,0,0],
                       [0,-1,0]]

verticies_relative_coords=[[1,1,1],
                           [1,1,-1],
                           [1,-1,1],
                           [1,-1,-1],
                           [-1,1,1],
                           [-1,1,-1],
                           [-1,-1,1],
                           [-1,-1,-1]]

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
    l=100/(dist+50)
    return (min(255,l*color[0]),min(255,l*color[1]),min(255,l*color[2]))

class Piece:
    def __init__(self,center,side_colors):
        self.center=center
        self.points=[]
        for v in verticies_relative_coords:
            self.points.append(Matrix('3x1',[[center.matrix[0][0]+piece_scale*(v[0])],[center.matrix[1][0]+piece_scale*(v[1])],[center.matrix[2][0]+piece_scale*(v[2])]]))
        self.sides=[]
        for i,s in enumerate(sides_relative_coords):
            self.sides.append({
                'id':i,
                's':Matrix('3x1',[[center.matrix[0][0]+piece_scale*(s[0])],[center.matrix[1][0]+piece_scale*(s[1])],[center.matrix[2][0]+piece_scale*(s[2])]]),
                'c':side_colors[i]
            })

    def get_side_order(self,matrix):
        res=[]
        for s in self.sides:
            r=s.copy()
            r['s']=matrix@s['s']
            res.append(r)
        res.sort(key=lambda x: x['s'].matrix[2][0])
        return res[3:]
        
    def draw_piece(self,screen,light_center,matrix):
        rp=[]
        for point in self.points:
            p=matrix@point
            rp.append((int(p.matrix[0][0]+250),int(-p.matrix[1][0]+250)))
        r=self.get_side_order(matrix)
        for s in r:
            if s['c'] != 0:
                d=dist_3d_mp(s['s'],light_center)
                c=get_color(d,side_colors[s['c']])
                draw.polygon(screen,c,[rp[i] for i in sides_pnt_index[s['id']]])       

if __name__=='__main__':
    p=Piece((0,0,0),0)

#   order
#top
#front
#right
#behind
#left
#bottom
import json
from math import sin, cos, radians, sqrt
from MatrixObj import Matrix, identity3
from pygame import draw

f=open('config.json','r')
config=json.load(f)
f.close()

cube_scale=config['cube_scale']
piece_scale=config['piece_scale']
side_colors = config['side_colors']
sides_pnt_index = config['sides_pnt_index']
sides_relative_coords = config['sides_relative_coords']
verticies_relative_coords=config['verticies_relative_coords']

def dist_3d_m(pnt1,pnt2):
    return sqrt((pnt1.matrix[0][0]-pnt2.matrix[0][0])**2+(pnt1.matrix[1][0]-pnt2.matrix[1][0])**2+(pnt1.matrix[2][0]-pnt2.matrix[2][0])**2)
def dist_3d_p(pnt1,pnt2):
    return sqrt((pnt1[0]-pnt2[0])**2+(pnt1[1]-pnt2[1])**2+(pnt1[2]-pnt2[2])**2)
def dist_3d_mp(pntm,pntp):
    return sqrt((pntm.matrix[0][0]-pntp[0])**2+(pntm.matrix[1][0]-pntp[1])**2+(pntm.matrix[2][0]-pntp[2])**2)
def dist_2d_mp(pntm,pntp):
    return sqrt((pntm.matrix[0][0]-pntp[0])**2+(pntm.matrix[1][0]-pntp[1])**2)

def get_color(dist,color):
    #l=100/(dist+50)
    l=200/(dist+100)
    return (min(255,l*color[0]),min(255,l*color[1]),min(255,l*color[2]))

class Piece:
    def __init__(self,center,side_colors):
        self.center=center
        self.colors=side_colors
        self.add=identity3
        self.steps=[]
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

    def set_side_colors(self,new_colors):
        self.colors=new_colors
        for i in range(6):
            self.sides[i]['c']=new_colors[i]

    def get_step(self,axis,angle):
        if axis == 0:
            return Matrix('3x3',[[1,0,0],[0,cos(radians(angle)),-sin(radians(angle))],[0,sin(radians(angle)),cos(radians(angle))]])
        elif axis == 1:
            return Matrix('3x3',[[cos(radians(angle)),0,-sin(radians(angle))],[0,1,0],[sin(radians(angle)),0,cos(radians(angle))]])
        elif axis == 2:
            return Matrix('3x3',[[cos(radians(angle)),-sin(radians(angle)),0],[sin(radians(angle)),cos(radians(angle)),0],[0,0,1]])


    def get_personal_matrix(self,base=None):
        res=self.add
        if base != None:
            res = base@self.add
        for i in range(len(self.steps)):
            res @= self.steps[len(self.steps)-i-1]
        return res

    def get_side_order(self,matrix):
        res=[]
        for s in self.sides:
            r=s.copy()
            r['s']=matrix@s['s']
            res.append(r)
        res.sort(key=lambda x: x['s'].matrix[2][0])
        return res[3:]
        ## return res
        
    def draw_piece(self,screen,light_center,matrix):
        rp=[]
        for point in self.points:
            p=matrix@point
            rp.append((int(p.matrix[0][0]+250),int(-p.matrix[1][0]+250)))
        r=self.get_side_order(matrix)
        for s in r:
            if s['c'] != '0':
                d=dist_3d_mp(s['s'],light_center)
                c=get_color(d,side_colors[s['c']])
                draw.polygon(screen,c,[rp[i] for i in sides_pnt_index[s['id']]])  

if __name__=='__main__':
    pass

#   order
#top
#front
#right
#behind
#left
#bottom

# ops
#eg: urf
#    yxz
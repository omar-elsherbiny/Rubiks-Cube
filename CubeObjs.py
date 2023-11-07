import json
from math import sin, cos, radians, sqrt
from MatrixObj import Matrix
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

def get_color(dist,color):
    l=100/(dist+50)
    return (min(255,l*color[0]),min(255,l*color[1]),min(255,l*color[2]))

class Piece:
    def __init__(self,center,side_colors):
        self.angs=[0,0,0]
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

    def get_personal_matrix(self,add=[0,0,0]):
        rotX=Matrix('3x3',[[1,0,0],[0,cos(radians(self.angs[0]+add[0])),-sin(radians(self.angs[0]+add[0]))],[0,sin(radians(self.angs[0]+add[0])),cos(radians(self.angs[0]+add[0]))]])
        rotY=Matrix('3x3',[[cos(radians(self.angs[1]+add[1])),0,-sin(radians(self.angs[1]+add[1]))],[0,1,0],[sin(radians(self.angs[1]+add[1])),0,cos(radians(self.angs[1]+add[1]))]])
        rotZ=Matrix('3x3',[[cos(radians(self.angs[2]+add[2])),-sin(radians(self.angs[2]+add[2])),0],[sin(radians(self.angs[2]+add[2])),cos(radians(self.angs[2]+add[2])),0],[0,0,1]])
        return rotX@rotY@rotZ

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
            if s['c'] != 0:
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
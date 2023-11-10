from math import floor
from pygame import draw

class Matrix:
    class Size:
        def __init__(self, size):
            if type(size)==int:
                self.r, self.c=size, size
            elif type(size)==Matrix.Size:
                self.r, self.c=size.r, size.c
            else:
                s=size.split('x')
                self.r=int(s[0])
                self.c=int(s[1])
        def is_square(self):
            if self.r==self.c:return True
            else: return False
        def __mul__(self, other) -> bool:
            if isinstance(other, Matrix.Size):
                if self.c==other.r: return True
                else: return False
            else:
                raise TypeError(f"unsupported operand type(s) for *: 'Size' and '{type(other).__name__}'")
        def __eq__(self, other) -> bool:
            if isinstance(other, Matrix.Size):
                return self.r==other.r and self.c==other.c
            else: return False
        def __str__(self) -> str:
            return f'{self.r}x{self.c}'


    def __init__(self, size , matrix):
        self.size=Matrix.Size(size)
        self.matrix=self._format_matrix(matrix)

    def identity(self):
        return Matrix(self.size.r,[[1 if i==j else 0 for j in range(self.size.r)]for i in range(self.size.r)])
    
    def transpose(self):
        m=[[0 for j in range(self.size.r)]for i in range(self.size.c)]
        for r in range(len(self.matrix)):
            for i in range(len(self.matrix[r])):
                m[i][r]=self.matrix[r][i]
        return Matrix(f'{self.size.c}x{self.size.r}',m)

    def determinant(self):
        det=None
        if self.size.is_square():
            if self.size==Matrix.Size('1x1'):
                det=self.matrix[0][0]
            elif self.size==Matrix.Size('2x2'):
                det=self.matrix[0][0]*self.matrix[1][1]-self.matrix[0][1]*self.matrix[1][0]
            elif self.size==Matrix.Size('3x3'):
                a,b,c,d,e,f,g,h,i = self.matrix[0][0],self.matrix[0][1],self.matrix[0][2],self.matrix[1][0],self.matrix[1][1],self.matrix[1][2],self.matrix[2][0],self.matrix[2][1],self.matrix[2][2]
                det=a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
        return det

    def inverse(self):
        inv=None
        if self.size.is_square():
            if self.size==Matrix.Size('1x1'):
                inv=1/self.matrix[0][0]
            elif self.size==Matrix.Size('2x2'):
                m=self._flatten(self.matrix)
                m[0],m[3]=m[3],m[0]
                m[2]*=-1
                m[1]*=-1
                m=self._rearrange(m)
                inv=Matrix(self.size,m)*(1/self.determinant())
        return inv

    def __add__(self, other):
        if isinstance(other,Matrix):
            if self.size==other.size:
                a=[]
                s=self._flatten(self.matrix)
                o=self._flatten(other)
                for i in range(len(s)):
                    a.append(s[i]+o[i])
                return Matrix(self.size, self._rearrange(a))
            else:
                raise TypeError(f"cant add matricies of different sizes")
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Matrix' and '{type(other).__name__}'")

    def __sub__(self, other):
        if isinstance(other,Matrix):
            if self.size==other.size:
                a=[]
                s=self._flatten(self.matrix)
                o=self._flatten(other)
                for i in range(len(s)):
                    a.append(s[i]-o[i])
                return Matrix(self.size, self._rearrange(a))
            else:
                raise TypeError(f"cant subtract matricies of different sizes")
        else:
            raise TypeError(f"unsupported operand type(s) for -: 'Matrix' and '{type(other).__name__}'")

    def __matmul__(self, other):
        if isinstance(other, Matrix):
            if self.size*other.size:
                m=[[0 for j in range(other.size.c)]for i in range(self.size.r)]
                for r in range(self.size.r):
                    for c in range(other.size.c):
                        sum=0
                        for i in range(self.size.c):
                            sum+=self.matrix[r][i]*other.matrix[i][c]
                        m[r][c]=sum
                return Matrix(f'{self.size.r}x{other.size.c}', m)
            else:
                raise TypeError(f"cant multiply matricies of incompatible sizes")
        else:
            raise TypeError(f"unsupported operand type(s) for @: 'Matrix' and '{type(other).__name__}'")
    
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Matrix(self.size, self._rearrange([other*i for i in self._flatten(self.matrix)]))
        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Matrix' and '{type(other).__name__}'")

    def __pow__(self, other):
        if isinstance(other, int):
            prod=self
            for i in range(other-1):
                prod=prod@self
            return prod
        else:
            raise TypeError(f"unsupported operand type(s) for **: 'Matrix' and '{type(other).__name__}'")


    def _format_matrix(self, matrix):
        m=matrix
        m=m[:self.size.r] + [[0]*self.size.c]*(self.size.r - len(m))
        for r in range(len(m)):
            m[r]=m[r][:self.size.c] + [0]*(self.size.c - len(m[r]))
        return m
    def _flatten(self, matrix):
        return [i for r in matrix for i in r]
    def _rearrange(self, matrix_list):
        m=[[0 for j in range(self.size.c)]for i in range(self.size.r)]
        for i in range(len(matrix_list)):
            m[floor((i/self.size.c)%self.size.r)][i%self.size.c]=matrix_list[i]
        return m
    def _sub_matrix(matrix, r,c):
        m=[x[:] for x in matrix]
        [row.pop(c-1) for row in m]
        m.pop(r-1)
        return m

    def __round__(self, ndigits=None):
        return Matrix(self.size, self._rearrange([round(i,ndigits) for i in self._flatten(self.matrix)]))
    def __len__(self):
        return len(self.matrix)
    def __getitem__(self, item):
        return self.matrix[item]
    def __iter__(self):
        return iter(self.matrix)
    def __str__(self) -> str:
        return '\n'.join([' '.join([f'{i}' for i in r]) for r in self.matrix]) + '\n'+'-'*(2*self.size.c-1)

class Basis:
    vects=[Matrix('3x1', [[1],[0],[0]]),Matrix('3x1', [[0],[1],[0]]),Matrix('3x1', [[0],[0],[1]])]

    def draw_basis(self,screen,matrix,scale,x,y):
        draw.line(screen,(255, 10, 50),(x,y),((matrix@self.vects[0]*scale).matrix[0][0]+x,-(matrix@self.vects[0]*scale).matrix[1][0]+y),3)
        draw.line(screen,(50, 255, 10),(x,y),((matrix@self.vects[1]*scale).matrix[0][0]+x,-(matrix@self.vects[1]*scale).matrix[1][0]+y),3)
        draw.line(screen,(10, 50, 255),(x,y),((matrix@self.vects[2]*scale).matrix[0][0]+x,-(matrix@self.vects[2]*scale).matrix[1][0]+y),3)

identity3=Matrix('3x3',[[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])

if __name__=='__main__':
    pass
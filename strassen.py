import numpy as np

class Matrix9:
    def __init__(self, data: np.array):
        self.data = data

    def __add__(self, other):
        return Matrix9((self.data + other.data)%9)

    def __radd__(self, other):
        return Matrix9((other.data + self.data)%9)

    def __sub__(self, other):
        return Matrix9((self.data - other.data)%9)

    def __rsub__(self, other):
        return Matrix9((other.data - self.data)%9)

    def __mul__(self, other):
        return Matrix9((other.data * self.data)%9)

    def __rmul__(self, other):
        return Matrix9((other.data * self.data)%9)

    def __getitem__(self, key):
        return Matrix9(self.data[key])

    def __setitem__(self, key, value):
        self.data[key] = value


def matmul(A:Matrix9, B:Matrix9):
    size = A.data.shape[0]
    if size == 2:
        M1 = (A[0][0]+A[1][1])*(B[0][0]+B[1][1])
        M2 = (A[1][0]+A[1][1])*B[0][0]
        M3 = A[0][0]*(B[0][1]-B[1][1])
        M4 = A[1][1]*(B[1][0]-B[0][0])
        M5 = (A[0][0]+A[0][1])*B[1][1]
        M6 = (A[1][0]-A[0][0])*(B[0][0]+B[0][1])
        M7 = (A[0][1]-A[1][1])*(B[1][0]+B[1][1])
        C11 = M1 + M4 - M5 + M7
        C12 = M3 + M5
        C21 = M2 + M4
        C22 = M1 - M2 + M3 + M6
        return Matrix9(np.block([[C11.data,C12.data],[C21.data,C22.data]]))
    A11 = A[:size//2,:size//2]
    A12 = A[:size//2,size//2:]
    A21 = A[size//2:,:size//2]
    A22 = A[size//2:,size//2:]
    B11 = B[:size//2,:size//2]
    B12 = B[:size//2,size//2:]
    B21 = B[size//2:,:size//2]
    B22 = B[size//2:,size//2:]
    M1 = matmul((A11+A22), (B11+B22))
    M2 = matmul((A21+A22), B11)
    M3 = matmul(A11, (B12-B22))
    M4 = matmul(A22, (B21-B11))
    M5 = matmul((A11+A12), B22)
    M6 = matmul((A21-A11), (B11+B12))
    M7 = matmul((A12-A22), (B21+B22))
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    return Matrix9(np.block([[C11.data,C12.data],[C21.data,C22.data]]))


def fastpow9(x:Matrix9, p:int) -> Matrix9:
    if p == 0: 
        return Matrix9(np.eye(x.data.shape[0], x.data.shape[1]).astype(int))
    if ((p%2) == 0):
        c = fastpow9(x, p // 2)
        return (matmul(c, c))
    else:
        return (matmul(fastpow9(x, p-1), x))

def read_input():
    input_m = []
    n = 0
    line = input()
    n = len(line.split())
    input_m.append(line)
    for _ in range(1,n):
        line = input()
        input_m.append(line)
    return input_m, n

def build_matrix9(input_m):
    n = len(input_m)
    if ((n & (n-1) == 0) and n != 0):
        in_matrix = np.array([[int(j) for j in i.split()] for i in input_m])
        return Matrix9(in_matrix)
    else: 
        l = len(bin(n)[2:])
        size = int(2**l) - n
        in_matrix = np.array([[int(j) for j in i.split()] for i in input_m])
        in_matrix = np.insert(in_matrix, n, np.zeros((size,n)).astype(int), 0)
        in_matrix = np.insert(in_matrix, n, np.zeros((size,size+n)).astype(int), 1)
    return Matrix9(in_matrix)

input_m, n = read_input()

if n==1:
    print(1)
else:
    in_matrix9 = build_matrix9(input_m)
    out = fastpow9(in_matrix9, n).data[:n,:n]

# print(out)
    for i in out:
        for j in i:
            print(j, end=" ")
        print()

#Упражнение 1

"""
n = int(input())
def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return (fib(n-1) + fib(n-2))
print (fib(n))
"""

"""
#Упражнение 2

n = int(input())
def divs(n):
    f = []
    d = 2
    while n>1:
        while n % d == 0:
            f.append(d)
            n//=d
        d+=1
    return f
print(divs(n))
"""

#Упражнение 3
"""
def nod(a, b):
    if b == 0:
        return 1, 0, a
    x1, y1, d = nod(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return x, y, d

while True:
    s = input().strip()
    if s == "":
        break
    a, b = map(int, s.split())
    x, y, d = nod(a, b)
    print(x, y, d)

"""

#Упражнение 4

"""
def triangle(size, symb, n=1):
    if n <= size:
        print(symb * n)
        triangle(size, symb, n + 1)
        if n < size:
            print(symb * n)

size, symb = input().split()
triangle(int(size), symb)
"""

# Упражнение 5

"""
import numpy as np

def sm(n, m):
    a = np.zeros((n, m), dtype=int)
    x = 1
    t, b = 0, n - 1
    l, r = 0, m - 1    
    while t <= b and l <= r:
        for j in range(l, r + 1):
            a[t, j] = x
            x += 1
        t += 1        
        for i in range(t, b + 1):
            a[i, r] = x
            x += 1
        r -= 1
        if t <= b:
            for j in range(r, l - 1, -1):
                a[b, j] = x
                x += 1
            b -= 1
        if l <= r:
            for i in range(b, t - 1, -1):
                a[i, l] = x
                x += 1
            l += 1
    return a
n, m = map(int, input().split())
mat = sm(n, m)
for i in range(n):
    mat[i] = mat[i] * (i + 1)
print(mat)
"""

#Упражнение 6

"""
import numpy as np
def lsm(x, y):
    X = np.column_stack((np.ones(len(x)), x))
    return np.linalg.inv(X.T @ X) @ X.T @ y
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])
print(lsm(x, y))

"""

#Упражнение 7

"""
import numpy as np
n, m = map(int, input().split())
d = []
for _ in range(n):
    row = list(map(int, input().split()))
    d.append(row)
mat = np.array(d)
a = mat[:, :-1] 
b = mat[:, -1] 
x = np.linalg.solve(a, b)
print(x)

"""

#Упражнение 8


"""
import numpy as np
import random
def gd(N, a, b, n=1.0):
    x = np.linspace(0, 10, N)
    y_r = a * x + b
    y_e = y_r + np.array([random.gauss(0, n) for _ in range(N)])
    return x, y_e
#я брала N=20, a = 2.5, b=1
N = int(input()) 
a = float(input()) 
b = float(input()) 
x, y = gd(N, a, b, n=2.0)

def lsm(x, y):
    X = np.column_stack((np.ones(len(x)), x))
    return np.linalg.inv(X.T @ X) @ X.T @ y

c = lsm(x, y)
print("Истинные коэффициенты:", a, b)
print("Оцененные коэффициенты:", c[1], c[0])
"""
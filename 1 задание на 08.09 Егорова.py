# Упражнение 1
a, b = map(int, input().split())
print ("Упражнение 1:", a+b, a-b, a*b, sep = '\n')

#Упражнение 2
print ("Упражнение 2:",(int(input()))%10)

#Упражнение 3
l = list(map(int, input().split()))
n = len(l)
k=1
for i in l:
    k*=i
print("Упражнение 3:", k**(1/n))

# Упражнение 4
f1 = open('input.txt','r')
k=list(f1.readline().split())
oper = f1.readline()
nums = []
for i in k:
    nums.append(int(i))
ans = 0
if oper == '+':
    res = sum(nums)
elif oper == '*':
    ans=1
    for s in nums:
        ans*=s
    res = ans
elif oper == '-':
    res = nums[0]
    for i in range(1, len(nums)):
        res -= nums[i]

with open('output.txt', 'w') as f2:
    f2.write(str(res))


#Упражнение 5 
N, b, c = map(int, input().split())
ten = int(str(N), b)
ds = '0123456789'
res = ''
while ten > 0:
    d = ten % c
    res = ds[d] +  res
    ten//=c
print (res)



#Упражнение 6
f1 = open('input.txt','r')
k = list(f1.readline().split())
oper = f1.readline().strip()
ss = int(f1.readline().strip())
nums = []
for i in k:
    nums.append(int(i,ss))
ans = 0
if oper == '+':
    res = sum(nums)
elif oper == '*':
    ans=1
    for s in nums:
        ans*=s
    res = ans
elif oper == '-':
    res = nums[0]
    for i in range(1, len(nums)):
        res -= nums[i]

with open('output.txt', 'w') as f2:
    f2.write(str(res))

#Упражнения с numpy

#1
import numpy as np

#11
import numpy as np
print(np.eye(3))

#21
import numpy as np
i = np.array([[0, 1],[1, 0]])
print(np.tile(i, (4, 4)))

#31
import numpy as np
np.seterr(all="ignore")

#41
import numpy as np
i = np.arange(10)
print (np.add.reduce(i))

#53
import numpy as np
a = np.array([1.1, 1.2, 1.3], dtype=np.float32)
a32 = a.astype(np.int32)

#60
import numpy as np
def func(arr):
    return np.any(np.all(arr == 0, axis=0))
a1= np.array([[1, 0, 3],[4, 0, 6],[7, 0, 9]])
a2 = np.array([[1, 2, 3],[4, 5, 6],[7, 8, 9]])
print("Есть нулевые столбцы в а1:", func(a1), ", есть нулевые столбцы в а2:", func(a2))

#72
import numpy as np
a = np.arange(9).reshape(3,3)
a[[0,1]] = a[[1,0]]
print(a)

#83
import numpy as np
a = np.array([1,2,3,1,2,1,1,1])
print(np.argmax(np.bincount(a)))



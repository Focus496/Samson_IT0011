#part A
n = 5
for x in range(1, n + 1):
    for y in range(n - x):
        print(" ", end="")
    for z in range(1, x + 1):
        print(z, end="")
    print()
#part b

n = [1, 3, 5, 6, 7]
a = 0
while a < 5:  
    b = n[a]  
    c = 0 
    while c < b * 2 - 1:
        print(b, end="")  
        c += 2
    print()
    a += 1

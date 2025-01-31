a = input("Enter string input:")
sum = 0
for b in a:
    if b.isdigit():
        sum += int(b)
print(sum)
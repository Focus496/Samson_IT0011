
A = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
B = {'b', 'c', 'h', 'l', 'm', 'o'}
C = {'c', 'd', 'f', 'h', 'i', 'j', 'k'}

A_intersect_B = A & B
print("Elements in both A and B:", A_intersect_B)


B_not_A_C = B - (A | C)
print("Elements in B that are not in A or C:", B_not_A_C)


subset_1 = {'h', 'i', 'j', 'k'}
subset_2 = {'c', 'd', 'f'}
subset_3 = {'b', 'c', 'h'}
subset_4 = {'d', 'f'}
subset_5 = {'c'}
subset_6 = {'l', 'm', 'o'}


print("i. Elements {h, i, j, k} can be obtained by: C - A")
print("ii. Elements {c, d, f} can be obtained by: C & A")
print("iii. Elements {b, c, h} can be obtained by: B & (A | C)")
print("iv. Elements {d, f} can be obtained by: A & C")
print("v. Element {c} can be obtained by: A & B & C")
print("vi. Elements {l, m, o} can be obtained by: B - (A | C)")
